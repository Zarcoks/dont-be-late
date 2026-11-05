# models.py
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


# Imported RATP data for stops
class Stop(models.Model):
  stop_id = models.CharField(max_length=100, unique=True)
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name


# Imported RATP data for lines
class Route(models.Model):
  route_id = models.CharField(max_length=100, unique=True) # ex: IDFM:C01742
  short_name = models.CharField(max_length=50) # ex: "A", "1"
  long_name = models.CharField(max_length=255)  # ex: "Cergy-le-Haut <> Marne-la-Vallée"
  route_type = models.IntegerField()  # 0 = tram, 1 = metro, 2 = RER, 3 = bus

  def __str__(self):
      return self.route_id


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations",)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    postal = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "[" + self.user.username + "] " + self.name


class Calendar(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="calendar",)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=2048)
    last_update = models.DateTimeField(default=timezone.now)
    default_location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class CalendarEvent(models.Model):
    uid = models.CharField(max_length=255)
    calendar = models.ForeignKey(
        Calendar,
        on_delete=models.CASCADE,
        related_name="events",
    )
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True
    )
    event_title = models.CharField(max_length=500)
    raw_location = models.CharField(max_length=500, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["calendar", "uid"], name="unique_event_per_calendar")]


class Trip(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="trip")
    origin_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="trips_from",
    )
    arrival_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="trips_to"
    )


class TripLine(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
    )
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    origin_stop = models.ForeignKey(Stop, on_delete=models.DO_NOTHING)
    arrival_stop = models.ForeignKey(Route, on_delete=models.DO_NOTHING)


class GuessLog(models.Model):
    event = models.ForeignKey(
        CalendarEvent,
        on_delete=models.CASCADE,
    )
    guessed_delay = models.IntegerField()
    guess_time = models.DateTimeField() # The time when the guess has been done