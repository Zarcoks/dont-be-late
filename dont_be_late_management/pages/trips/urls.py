from django.urls import path
from . import views

urlpatterns = [
    path("", views.trips_dashboard, name="trip_dashboard"),
    path("locations/", views.get_locations, name="locations_list"),
    path("locations/cancel", views.cancel_create_location, name="cancel_create_location"),
    path("locations/new/", views.NewLocation.as_view(), name="new_location"),
]
