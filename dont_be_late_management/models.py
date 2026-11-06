# models.py
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


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


class Meteo(models.Model):
    # Où et quand
    postal = models.CharField(max_length=20)  # code postal
    moment = models.DateTimeField() # heure à laquelle cette météo s'applique
    recupere_le = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=50,default="manuel")   # "manuel", plus tard "meteo-france"

    # Mesures
    temperature = models.FloatField()   # °C
    humidite = models.PositiveSmallIntegerField()   # %
    pluie = models.FloatField(default=0)    # mm/h
    rafales = models.PositiveSmallIntegerField(default=0)   #km/h

    #Phénomènes (oui/non)
    neige = models.BooleanField(default=False)
    brouillard = models.BooleanField(default=False)
    orage = models.BooleanField(default=False)
    secheresse = models.BooleanField(default=False)
    soleil_bas = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["postal","moment"],name="meteo_unique_lieu_moment"),
        ]

    #Valeurs calculées, pas stockées
    @property
    def canicule(self):
        return self.temperature > 35

    @property
    def automne(self):
        return 9 <= self.moment.month <= 11

    def en_dictionnaire(self):
        """Format attendu par calculer_retard"""
        return {
            "temperature": self.temperature,
            "humidite": self.humidite,
            "pluie": self.pluie,
            "rafales": self.rafales,
            "neige": self.neige,
            "brouillard": self.brouillard,
            "orage": self.orage,
            "secheresse": self.secheresse,
            "soleil_bas": self.soleil_bas,
            "canicule": self.canicule,
            "automne": self.automne,
        }
    
    def __str__(self):
        return self.postal + "-" + str(self.moment)