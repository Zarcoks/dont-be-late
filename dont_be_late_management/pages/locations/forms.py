from django import forms

from dont_be_late_management.models import Calendar, Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']