from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_locations, name="locations_list"),
    path("new/", views.NewLocation.as_view(), name="new_locations"),
]
