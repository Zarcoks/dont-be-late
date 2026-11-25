from datetime import datetime, time, timedelta

from dont_be_late_management.models import CalendarEvent
from disruption_worker.services.disruption import PARIS

EARLIEST_EVENT_HOUR = 10

#Allows to get the event and match with the disrpution after
def first_events_of_day(day):
    start_of_search = datetime(day.year, day.month, day.day, EARLIEST_EVENT_HOUR, 0, tzinfo=PARIS)
    next_day = day + timedelta(days=1)
    end_of_search = datetime(next_day.year, next_day.month, next_day.day, 0, 0, tzinfo=PARIS)

    events_of_the_day = CalendarEvent.objects.filter(
        starting_time__gte=start_of_search,
        starting_time__lt=end_of_search,
    ).order_by("starting_time")

    first_events = []
    calendars_already_seen = []

    for event in events_of_the_day:
        if event.calendar_id not in calendars_already_seen:
            first_events.append(event)
            calendars_already_seen.append(event.calendar_id)

    return first_events