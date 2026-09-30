# models.py
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations",)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calendars",)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=2048)
    last_update = models.DateTimeField(default=timezone.now)
    default_location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class CalendarEvent(models.Model):
    uid = models.CharField(unique=True) # UID from the import (not automatic)
    calendar = models.ForeignKey(
        Calendar,
        on_delete=models.CASCADE,
    )
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True
    )
    event_title = models.CharField(max_length=500)
    contact_name = models.CharField(max_length=255, blank=True)
    raw_location = models.CharField(max_length=500, blank=True)


class Trip(models.Model):
    priority = models.IntegerField(default=0) # The way to order the trips you prefer
    target_duration = models.PositiveIntegerField()
    doubt_calculus = models.PositiveIntegerField(default=0) # Should be calculated by the app (for ex 15mn * nb_transport_changes)
    origin_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="trips_from"
    )
    arrival_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="trips_to"
    )


class Line(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
    )
    line_id = models.CharField(max_length=255)
    origin_stop = models.CharField(max_length=255)
    arrival_stop = models.CharField(max_length=255)


class GuessLog(models.Model):
    event = models.ForeignKey(
        CalendarEvent,
        on_delete=models.CASCADE,
    )
    guessed_delay = models.IntegerField()
    guess_time = models.DateTimeField() # The time when the guess has been done