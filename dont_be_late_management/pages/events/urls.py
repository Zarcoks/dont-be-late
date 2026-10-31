from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_dashboard, name="event_dashboard"),
    path("calendar/", views.edit_calendar, name="calendar"),
]
