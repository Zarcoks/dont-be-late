from django.core.management.base import BaseCommand

from calendar_worker.synchroniser import synchronise_one_calendar
from dont_be_late_management.models import Calendar


class Command(BaseCommand):
    help = "Run a sync of specific calendar (given url)."

    def handle(self, *args, **options):
        synchronise_one_calendar(Calendar.objects.filter(url="https://de.telecom-sudparis.eu/disi__planning/ics_calendars/96e70b84a79ddd9273aaa9dba9f9879b7f00be3a/").first())
