from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import View

from .models import Route, RouteDetail, Station, Trip


class DispatchStations(View):

    def get(self, request):
        dispatch_stations = Station.objects.filter(is_dispatch=True)
        return render(
            request,
            'schedule/schedule.html',
            {
                'dispatch_stations': dispatch_stations
            }
        )


class ArriveStations(View):

    def get(self, request):
        _from = request.GET.get('from')
        to = get_object_or_404(Station, system_id=_from).arrive_stations.all()
        to = {station.system_id: station.title for station in to}
        return JsonResponse(to)


class TripsTable(View):

    def get(self, request):
        _from = request.GET.get('from')
        to = request.GET.get('to')
        trips = Trip.objects.filter(
            dispatch_station=get_object_or_404(Station, system_id=_from),
            arrive_station=get_object_or_404(Station, system_id=to)
        ).all()
        context = {'trips': trips}
        rendered = render_to_string('schedule/trips_table.html', context)
        return JsonResponse(rendered, safe=False)


class RouteDetails(View):

    def get(self, request):
        system_id = request.GET.get('system_id')
        route_details = RouteDetail.objects.filter(
            related_route=get_object_or_404(Route, system_id=system_id)
        ).order_by('id').all()
        context = {'route_details': route_details}
        rendered = render_to_string('schedule/route_details.html', context)
        return JsonResponse(rendered, safe=False)
