from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from dont_be_late_management.pages.trips.forms import *


def get_active_locations(user):
    return user.locations.all().filter(is_deleted=False).order_by('pk') # This should always return Home first

@login_required
def trips_dashboard(request):
    locations = get_active_locations(request.user)
    trips = Trip.objects.filter(user=request.user).select_related(
        "origin_location", "arrival_location"
    )
    select_form = TripSelectForm(trips=trips)
    selected_trip = select_form.fields["trip"].initial
    if selected_trip:
        selected_trip = trips.filter(pk=selected_trip).first()

    return render(request, "dont_be_late_management/trips/trips.html", {
        "locations": locations,
        "trips": trips,
        "select_form": select_form,
        "selected_trip": selected_trip,
    })


@login_required
def select_trip(request):
    trips = Trip.objects.filter(user=request.user).select_related(
        "origin_location", "arrival_location"
    )
    select_form = TripSelectForm(request.GET or None, trips=trips)
    selected_trip = select_form.cleaned_data.get("trip") if select_form.is_valid() else None
    return render(request, "dont_be_late_management/trips/partials/trip_select.html", {
        "select_form": select_form,
        "selected_trip": selected_trip,
    })


@login_required
def cancel_add_trip_line(request):
    trip_id = request.GET.get("trip_id")
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    return render(request, "dont_be_late_management/trips/partials/trip_line_add_button.html", {
        "trip": trip,
    })


class NewTripLine(LoginRequiredMixin, View):
    def get(self, request):
        trip_id = request.GET.get("trip_id")
        trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
        form = TripLineForm()
        return render(request, "dont_be_late_management/trips/partials/trip_line_form.html", {
            "form": form,
            "trip": trip,
        })

    def post(self, request):
        trip_id = request.POST.get("trip_id")
        trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
        form = TripLineForm(request.POST)

        if form.is_valid():
            trip_line = form.save(commit=False)
            trip_line.trip = trip
            trip_line.save()
            return render(request, "dont_be_late_management/trips/partials/trip_line_item.html", {
                "trip_line": trip_line,
            })

        return render(request, "dont_be_late_management/trips/partials/trip_line_form.html", {
            "form": form,
            "trip": trip,
        }, status=400)


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
        form = TripForm(request.POST, user=request.user)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            response = HttpResponse(status=204)
            return response

        return render(request, "trips/partials/trip_form.html", {
            "form": form,
            "locations": get_active_locations(request.user),
        }, status=400)


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