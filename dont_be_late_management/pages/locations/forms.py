from django import forms

from dont_be_late_management.models import Calendar, Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'city', 'postal']

    def __init__(self, *args, suggested_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        if suggested_name is not None:
            self.fields["name"].initial = suggested_name