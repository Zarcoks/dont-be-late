from django import forms
from dont_be_late_management.models import Location, Trip, TripLine


class LocationForm(forms.ModelForm):
  class Meta:
    model = Location
    fields = ["name", "address", "postal", "city"] # TODO upgrade with fields and widgets


class TripForm(forms.ModelForm):
  class Meta:
    model = Trip
    fields = ['origin_location', 'arrival_location']


class TripLineForm(forms.ModelForm):
  class Meta:
    model = TripLine
    fields = ['route', 'origin_stop', 'arrival_stop']