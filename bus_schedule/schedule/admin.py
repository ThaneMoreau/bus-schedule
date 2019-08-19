from django.contrib import admin

from .models import *


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = [
        'system_id',
        'title',
        'system_title',
        'is_dispatch',
        'address',
        'phone'
    ]
    search_fields = ['title', 'system_title']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = [
        'system_id',
        'title',
        'schedule',
    ]
    search_fields = ['title']


@admin.register(RouteDetail)
class RouteDetailAdmin(admin.ModelAdmin):
    list_display = [
        'related_station',
        'related_route',
        'station_order',
        'dispatch_time',
        'arrive_time',
    ]


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        'dispatch_station',
        'arrive_station',
        'cost',
        'cost_luggage',
        'dispatch_time',
        'arrive_time',
        'travel_time',
        'related_route'
    ]
