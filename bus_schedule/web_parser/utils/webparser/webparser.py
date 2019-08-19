import os
import re
import time

import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError

from schedule.models import *

from .logger import logger


def get_page(url, method='GET', params=None):
    while True:
        try:
            response = requests.request(method, url, params=params)
            if response.status_code == 200:
                page = response.text
                return page
            logger.warning(
                f'{method} request {url} with params: {params} fail'
            )
        except Exception as e:
            logger.error(
                f'Unable to make {method} request {url} with params:\
                {params}, cause: \n{e}'
            )


def add_arriving(src: str, arrive_stations: list):
    src_station = Station.objects.get(system_id=src)
    try:
        src_station.arrive_stations.add(*arrive_stations)
    except Exception as e:
        logger.error(f'Fail to write arrive stations for {src}, cause:\n{e}')
        pass


def parse_stations(page: str, direction='src'):
    page = BeautifulSoup(page, 'lxml')
    selects = page.find_all('select')
    select = selects[-1] if direction == 'dest' else selects[0]
    options = select.find_all('option')
    stations = {option['value']: option.text for option in options}
    return stations


def parse_route_and_trip(page: str, src: Station, dest: Station):
    page = BeautifulSoup(page, 'lxml')
    route = {}
    trip = {}
    table = page.find_all('table')[-1]
    rows = table.find_all('tr')[1:]
    for row in rows:
        try:
            columns = row.find_all('td')
            route['title'] = columns[2].text.strip()
            system_id = columns[2].find('a').get('href').split('=')[-1]
            route['system_id'] = re.split(r'(\d+)', system_id)[1]
            route['schedule'] = columns[-1].text.strip()
            trip['dispatch_station'] = src
            trip['arrive_station'] = dest
            trip['dispatch_time'] = columns[0].text.strip()
            trip['arrive_time'] = columns[1].text.strip()
            trip['cost'] = columns[3].text.strip()
            trip['cost_luggage'] = columns[4].text.strip()
        except Exception as e:
            logger.error(
                f'Fail to parse from {src.title} to {dest.title}, cause:\n{e}'
            )
            continue
        write_route_and_trip(route, trip)


def parse_route_detail(page: str, route: Route):
    page = BeautifulSoup(page, 'lxml')
    table = page.find('table')
    if not table:
        return
    rows = table.find_all('tr')[1:]
    route_detail = {}
    for order, row in enumerate(rows):
        try:
            columns = row.find_all('td')
            dispatch_time = columns[1].text.strip()
            arrive_time = columns[0].text.strip()
            if '&nbsp' not in dispatch_time:
                route_detail['dispatch_time'] = dispatch_time
            if '&nbsp' not in arrive_time:
                route_detail['arrive_time'] = arrive_time
            route_detail['station_order'] = order
            station_title = columns[2].text.strip()
        except Exception as e:
            logger.error(
                f'Fail to parse details for route {route.title}\
                {route.system_id}, cause:\n{e}'
            )
            continue
        write_route_detail(route_detail, station_title, route)


def write_station(station_id: str, title: str, is_dispatch=False):
    try:
        station = Station.objects.create(
            system_id=station_id,
            title=title,
            is_dispatch=is_dispatch
        )
        if not is_dispatch:
            return station
    except IntegrityError:
            station = Station.objects.get(system_id=station_id)
            if is_dispatch:
                station.is_dispatch = True
                station.save()
                return station
            station.title = title
            station.save()
            return station
    except Exception as e:
        logger.error(f'Fail to write station {title}, cause:\n{e}')


def write_route_and_trip(_route: dict, _trip: dict):
    try:
        route = Route.objects.create(**_route)
    except IntegrityError:
        route = Route.objects.get(system_id=_route['system_id'])
    except Exception as e:
        logger.error(f'Fail to write route {_route["system_id"]}, cause:\n{e}')
        return
    try:
        trip = Trip.objects.create(related_route=route, **_trip)
    except Exception as e:
        logger.error(
            f'Fail to write trip for route {_route["system_id"]}, cause:\n{e}'
        )
        return


def write_route_detail(_route_detail: dict, station_title: str, route: Route):
    try:
        station = Station.objects.get(title=station_title)
    except Station.DoesNotExist:
        logger.warning(f'{station_title} does not exists')
        return
    except Exception as e:
        logger.error(f'Error to get {station_title} from DB, cause:\n{e}')
        return
    try:
        route_detail = RouteDetail.objects.create(
            related_station=station,
            related_route=route,
            **_route_detail
        )
    except Exception as e:
        logger.error(
            f'Error to write RouteDetail for {station_title}, cause:\n{e}'
        )
        return


def make_stations(url, page_count=3):
    src_stations = parse_stations(get_page(url=url))
    # add slice [0:page_count] for specific dispatch stations
    for src in list(src_stations.keys()):
        arrive_stations = []
        write_station(src, src_stations[src], True)
        dest_stations = parse_stations(
            get_page(
                url=url,
                params={'from': src}
            ),
            direction='dest'
        )
        for dest in dest_stations.keys():
            arrive_stations.append(
                write_station(
                    dest,
                    dest_stations[dest]
                )
            )
        add_arriving(src, arrive_stations)


def make_route_details(url):
    routes = Route.objects.all()
    for route in routes:
        page = get_page(
            url=url,
            params={'nr': route.system_id}
        )
        parse_route_detail(page, route)


def make_routes_and_trips(url):
    src_stations = Station.objects.filter(is_dispatch=True)
    for src in src_stations:
        for dest in src.arrive_stations.all():
            page = get_page(
                url=url,
                method='POST',
                params={
                    'from': src.system_id,
                    'to': dest.system_id
                }
            )
            parse_route_and_trip(page, src, dest)


def run():
    url = 'http://www.kpas.ru/rasp.php'
    url_routes = 'http://www.kpas.ru/pp_new.php'
    start = time.monotonic()
    make_stations(url, page_count=3)
    make_routes_and_trips(url)
    make_route_details(url_routes)
    logger.info(f'Complete\nScript\'s time: {time.monotonic()-start}')


if __name__ == '__main__':
    run()
