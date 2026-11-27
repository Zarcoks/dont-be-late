from django import forms
from dont_be_late_management.models import Location, Trip, TripLine, Route, Stop


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


from django import forms
from dont_be_late_management.models import Location, Route, Stop, TripLine


class TripLineForm(forms.ModelForm):
    route = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "Line (e.g. RER A)",
            "list": "route-suggestions",
        })
    )
    origin_stop = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "From stop",
            "list": "stop-suggestions",
        })
    )
    arrival_stop = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-sm",
            "placeholder": "To stop",
            "list": "stop-suggestions",
        })
    )

    class Meta:
        model = TripLine
        fields = ["route", "origin_stop", "arrival_stop"]

    def clean_route(self):
        value = (self.cleaned_data.get("route") or "").strip()
        if not value:
            raise forms.ValidationError("Please enter a line.")

        route = (
            Route.objects.filter(display_name__iexact=value).first()
            or Route.objects.filter(display_name__icontains=value).first()
        )
        if not route:
            raise forms.ValidationError("Unknown line.")

        return route

    def _find_stop_on_route(self, raw_value, route):
        value = (raw_value or "").strip()
        if not value:
            raise forms.ValidationError("Please choose a stop.")

        if not route:
            raise forms.ValidationError("Please select a valid line first.")

        stop = (
            route.stops.filter(name__iexact=value).first()
            or route.stops.filter(name__icontains=value).first() # Again this is not ideal because we may have other stops linked to the line TODO
        )
        if not stop:
            raise forms.ValidationError("This stop is not associated with the selected line.")

        return stop

    def clean_origin_stop(self):
        route = self.cleaned_data.get("route")
        return self._find_stop_on_route(self.cleaned_data.get("origin_stop"), route)

    def clean_arrival_stop(self):
        route = self.cleaned_data.get("route")
        return self._find_stop_on_route(self.cleaned_data.get("arrival_stop"), route)