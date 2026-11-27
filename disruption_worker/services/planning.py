from datetime import datetime, time, timedelta

from dont_be_late_management.models import CalendarEvent
from disruption_worker.services.disruption import PARIS
from dont_be_late_management.models import Trip, TripLine

EARLIEST_EVENT_HOUR = 10

#Allows to get the event and match with the disrpution after
def first_events_of_day(day):
    start_of_search = datetime(day.year, day.month, day.day, EARLIEST_EVENT_HOUR, 0, tzinfo=PARIS)
    next_day = day + timedelta(days=1)
    end_of_search = datetime(next_day.year, next_day.month, next_day.day, 0, 0, tzinfo=PARIS)

    #Get the events from the calendar
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

#Return user trip to go to the location
def trip_of_event(event):
    return event.calendar.user.trip

#Return the lines taken by the user for the trip
def line_ids_of_trip(trip):
    line_ids = []

    trip_lines = TripLine.objects.filter(trip=trip)

    for trip_line in trip_lines:
        route = trip_line.route
        route_id = route.route_id
        line_id = "line:" + route_id

        if line_id not in line_ids:
            line_ids.append(line_id)

    return line_ids

def matching_disrupt_to_travel(trip, disruptions, start, end):
    trip_line_ids = line_ids_of_trip(trip)
    result = []

    for disrupt in disruptions:

        #Disrupt touches the line ?
        touches_my_lines = False
        for line_id in trip_line_ids:
            if line_id in disrupt.line_ids:
                touches_my_lines = True
        if not touches_my_lines:
            continue

        #Disrupt active ?
        if not disrupt.is_active_during_user_trip(start, end):
            continue

        result.append(disrupt)

    return result