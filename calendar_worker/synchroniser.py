import recurring_ical_events
from django.utils import timezone

import dont_be_late_management.utils.utils as utils
from dont_be_late_management.models import Calendar, CalendarEvent


def synchronise_calendars():
    calendars = Calendar.objects.filter()


def synchronise_one_calendar(url):
    calendar = utils.fetch_ics(url)
    events = recurring_ical_events.of(calendar).after(timezone.now())
    for event in events:
        CalendarEvent.objects.update_or_create(
            calendar=calendar,
            uid=event.get("UID"),
            defaults={
                "starting_time": event.get("DTSTART"),
                "ending_time": event.get("DTEND"),
                "event_title": str(event.get("SUMMARY", "")),
                "raw_location": str(event.get("LOCATION", "")),
                "contact_name": contact_name(event)[:255], # TODO je suis en train d'importer les évènements du calendrier
                "location": calendar.default_location,
            },
        )