from django.urls import path

from . import views

app_name = 'schedule'

urlpatterns = [
    path(
        '',
        views.DispatchStations.as_view(),
        name='dispatch_stations'
    ),
    path(
        'arrive_stations',
        views.ArriveStations.as_view(),
        name='arrive_stations'
    ),
    path(
        'trips_table',
        views.TripsTable.as_view(),
        name='trips_table'
    ),
    path(
        'route_details',
        views.RouteDetails.as_view(),
        name='route_details'
    )
]
