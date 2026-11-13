from django import forms
from dont_be_late_management.models import Location


class LocationForm(forms.ModelForm):

  class Meta:
    model = Location
    fields = ["name", "address", "postal", "city"]