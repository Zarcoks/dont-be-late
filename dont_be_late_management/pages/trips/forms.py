from django import forms
from dont_be_late_management.models import Location, Trip, TripLine


class LocationForm(forms.ModelForm):
  class Meta:
    model = Location
    fields = ["name", "address", "postal", "city"] # TODO upgrade with fields and widgets


class TripForm(forms.ModelForm):
    # TODO Potentially verify if the locations the user gave is him's
    class Meta:
        model = Trip
        fields = ["origin_location", "arrival_location"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            qs = Location.objects.filter(user=user, is_deleted=False)
            self.fields["origin_location"].queryset = qs
            self.fields["arrival_location"].queryset = qs


class TripSelectForm(forms.Form):
    trip = forms.ModelChoiceField(
      queryset=Trip.objects.none(),
      required=False,
      empty_label="No trips yet",
      widget=forms.Select(attrs={"class": "form-select", "aria-label": "Trip"}),
    )

    def __init__(self, *args, trips=None, **kwargs):
      super().__init__(*args, **kwargs)
      if trips is not None:
        self.fields["trip"].queryset = trips
        if not self.is_bound and not self.initial.get("trip"):
          first_trip = trips.first()
          if first_trip:
            self.fields["trip"].initial = first_trip.pk


class TripLineForm(forms.ModelForm):
  class Meta:
    model = TripLine
    fields = ["route", "origin_stop", "arrival_stop"]
    widgets = {
      "route": forms.TextInput(attrs={
        "class": "form-control form-control-sm",
        "placeholder": "Line",
        "list": "lines",
      }),
      "origin_stop": forms.TextInput(attrs={
        "class": "form-control form-control-sm",
        "placeholder": "From",
        "list": "stops",
      }),
      "arrival_stop": forms.TextInput(attrs={
        "class": "form-control form-control-sm",
        "placeholder": "To",
        "list": "stops",
      }),
    }