from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from dont_be_late_management.models import Trip, Location, TripLine
from dont_be_late_management.pages.trips.forms import LocationForm, TripForm, TripLineForm


def get_active_locations(user):
    return user.locations.all().filter(is_deleted=False).order_by('pk') # This should always return Home first

@login_required
def trips_dashboard(request):
    return render(request, 'dont_be_late_management/trips/trips.html', {"locations": get_active_locations(request.user)})


@login_required
def get_locations(request):
    return render(request, 'dont_be_late_management/trips/partials/locations_list.html', {"locations": get_active_locations(request.user)})

@login_required
def cancel_create_location(request):
    return render(request, 'dont_be_late_management/trips/partials/add_button.html')


class NewLocation(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dont_be_late_management/trips/partials/location_form.html')

    def post(self, request):
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user
            location.save()
            return render(request, "dont_be_late_management/trips/partials/location_created.html",
                          {"locations": get_active_locations(request.user)})
        return render(request, "dont_be_late_management/trips/partials/location_form.html", {"form": form})


class NewTrip(LoginRequiredMixin, View):
    def get(self, request):
        form = TripForm()
        return render(request, "trips/partials/trip_form.html" , {"form": form})

    def post(self, request):
        trip, created = Trip.objects.get_or_create(user=request.user)
        form = TripForm(request.POST, instance=trip)

        if form.is_valid():
            form.save()
            response = HttpResponse(status=204)
            response['HX-Redirect'] = '/trips/new/line/'
            return response

        template = "trips/partials/trip_form.html"
        return render(request, template, {"form": form}, status=400)


class NewTripLine(LoginRequiredMixin, View):
    def get(self, request):
        form = TripLineForm()
        return render(request, "trips/partials/trip_line_form.html", {"form": form})

    def post(self, request):
        trip = get_object_or_404(Trip, user=request.user)
        form = TripLineForm(request.POST)

        if form.is_valid():
            trip_line = form.save(commit=False)
            trip_line.trip = trip
            trip_line.save()

            return render(request, "trips/partials/trip_line_item.html", {"trip_line": trip_line})

        return render(request, "trips/partials/trip_line_form.html", {"form": form}, status=400)