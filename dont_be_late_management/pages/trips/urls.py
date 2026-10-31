from django.urls import path
from . import views

urlpatterns = [
    path("", views.trips_dashboard, name="trip_dashboard"),
]
