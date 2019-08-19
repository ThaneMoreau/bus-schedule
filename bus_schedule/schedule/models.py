from django.db import models
from django.utils import timezone
from pytils.translit import slugify

from .utils.travel_time import difference


class Station(models.Model):
    system_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=100)
    system_title = models.CharField(max_length=100, blank=True)
    is_dispatch = models.BooleanField(null=True, default=False)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    arrive_stations = models.ManyToManyField(
        'self',
        related_name='Arrive_stations',
        symmetrical=False
    )

    def __str__(self):
        return f'{self.system_id} {self.title}'

    def save(self, *args, **kwargs):
        if not self.system_title:
            self.system_title = slugify(self.title)
        super(Station, self).save(*args, **kwargs)


class Route(models.Model):
    system_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    schedule = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class RouteDetail(models.Model):
    related_station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='routes_info'
    )
    related_route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='stations_info'
    )
    station_order = models.IntegerField()
    dispatch_time = models.TimeField(null=True, default=None)
    arrive_time = models.TimeField(null=True, default=None)


class Trip(models.Model):
    dispatch_station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='Stations_dispatch_trips'
    )
    arrive_station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='Stations_arrive_trips'
    )
    cost = models.CharField(max_length=10, blank=True)
    cost_luggage = models.CharField(max_length=10, blank=True)
    dispatch_time = models.TimeField(null=True, default=None)
    arrive_time = models.TimeField(null=True, default=None)
    travel_time = models.CharField(max_length=100, blank=True)
    related_route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='Trips_routes')

    def save(self, *args, **kwargs):
        self.travel_time = difference(self.dispatch_time, self.arrive_time)
        super(Trip, self).save(*args, **kwargs)
