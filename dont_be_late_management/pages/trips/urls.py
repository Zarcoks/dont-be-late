from django.urls import path
from . import views

urlpatterns = [
    path("", views.trips_dashboard, name="trips_dashboard"),
    path("select/", views.select_trip, name="trip_select"),
    path("lines/new/", views.NewTripLine.as_view(), name="trip_line_create"),
    path("lines/cancel/", views.cancel_add_trip_line, name="trip_line_cancel"),
    path("locations/", views.get_locations, name="locations_list"),
    path("locations/cancel", views.cancel_create_location, name="cancel_create_location"),
    path("locations/new/", views.NewLocation.as_view(), name="new_location"),
    path("new/", views.NewTrip.as_view(), name="trip_create"),
    path("routes/filter/", views.filter_routes, name="route_filter"),
    path("stops/filter/", views.filter_stops, name="stop_filter"),
]
