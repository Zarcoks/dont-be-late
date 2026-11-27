from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from dont_be_late_management.pages.trips.forms import *


def get_active_locations(user):
    return user.locations.all().filter(is_deleted=False).order_by('pk') # This should always return Home first

def get_user_trips(user):
    return (
        Trip.objects.filter(user=user)
        .select_related("origin_location", "arrival_location")
        .prefetch_related(
            Prefetch(
                "transfers",
                queryset=TripLine.objects.select_related(
                    "route", "origin_stop", "arrival_stop"
                ),
                to_attr="ordered_transfers",
            )
        )
    )

@login_required
def trips_dashboard(request):
    return render(
        request,
        "dont_be_late_management/trips/trips.html",
        {
            "locations": get_active_locations(request.user),
            "trips": get_user_trips(request.user),
            "form": TripForm(user=request.user),
        },
    )

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

class NewTrip(LoginRequiredMixin, View):
    def get(self, request):
        form = TripForm()
        return render(request, "dont_be_late_management/trips/partials/trip_form.html" , {"form": form})

    def post(self, request):
        form = TripForm(request.POST, user=request.user)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()

            return render(
                request,
                "dont_be_late_management/trips/partials/trip_detail.html",
                {"trips": get_user_trips(request.user)},
            )

        response = render(
            request,
            "dont_be_late_management/trips/partials/new_trip_card.html",
            {
                "form": form,
                "locations": get_active_locations(request.user),
            },
        )
        response["HX-Retarget"] = "#new-trip-card"
        response["HX-Reswap"] = "outerHTML"
        return response


@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    trip.delete()
    return HttpResponse("", status=200)


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
def delete_trip_line(request, trip_line_id):
    trip_line = get_object_or_404(TripLine, pk=trip_line_id, trip__user=request.user)
    trip_line.delete()
    return HttpResponse("", status=200)


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

@login_required
def delete_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id, user=request.user)
    location.is_deleted = True
    location.save()

    return render(
        request,
        "dont_be_late_management/trips/partials/locations_list.html",
        {"locations": get_active_locations(request.user)},
    )

@login_required
def filter_routes(request):
    query = request.GET.get("q", "").strip()

    routes = Route.objects.order_by("short_name", "long_name")
    if query:
        routes = routes.filter(display_name__icontains=query)
    routes = routes[:100]

    return render(request, "dont_be_late_management/trips/partials/route_suggestions.html", {
        "routes": routes,
    })


@login_required
def filter_stops(request):
    query = request.GET.get("q", "").strip()
    route_query = request.GET.get("route", "").strip()

    if not route_query:
        return render(
            request,
            "dont_be_late_management/trips/partials/stop_suggestions.html",
            {"stops": []},
        )

    matched_route = Route.objects.filter(display_name__iexact=route_query).first()
    if matched_route is None:
        matched_route = Route.objects.filter(display_name__icontains=route_query).first()

    if matched_route is None:
        return render(
            request,
            "dont_be_late_management/trips/partials/stop_suggestions.html",
            {"stops": []},
        )

    stops = matched_route.stops.order_by("name")
    if query:
        stops = stops.filter(name__icontains=query)

    return render(
        request,
        "dont_be_late_management/trips/partials/stop_suggestions.html",
        {"stops": stops[:100]},
    )