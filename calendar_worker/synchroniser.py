import logging

from django.db import transaction
from icalendar import Calendar as ICal
import dont_be_late_management.utils.utils as utils
from dont_be_late_management.models import Calendar, CalendarEvent


def synchronise_calendars():
    calendars = Calendar.objects.all()
    for cal in calendars:
        synchronise_one_calendar(cal)
    logging.info(f"{calendars.count()} calendars updated.")


def synchronise_one_calendar(calendar):
    calendar_bytes = utils.fetch_ics(calendar.url)
    ical = ICal.from_ical(calendar_bytes)

    with transaction.atomic():
        for event in ical.walk("VEVENT"):
            uid = event.get("UID")
            title = str(event["SUMMARY"])
            start = event["DTSTART"].dt
            end = event["DTEND"].dt
            raw_location = str(event.get("LOCATION", ""))

            existing = CalendarEvent.objects.filter(calendar=calendar, uid=uid).first()

            if existing:
                existing.starting_time = start
                existing.ending_time = end
                existing.event_title = title
                existing.raw_location = raw_location
                existing.save()
                return

            CalendarEvent.objects.create(
                calendar=calendar,
                uid=uid,
                event_title=title,
                starting_time=start,
                ending_time=end,
                raw_location=raw_location,
                location=calendar.default_location,
            )