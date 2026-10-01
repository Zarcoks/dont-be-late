from django.urls import path
from . import views

urlpatterns = [
    path("", views.calendar_list, name="calendars_list"),
    path("new", views.NewCalendar.as_view(), name="new_calendars"),
]
