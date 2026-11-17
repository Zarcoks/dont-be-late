from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_dashboard, name="event_dashboard"),
    path("calendar/", views.edit_calendar, name="calendar"),
    path("<int:pk>/edit", views.EventEdit.as_view(), name="edit_event"),
    path("<int:pk>/cancel", views.cancel_edit_event, name="cancel_edit_event"),
]
