from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from dont_be_late_management.pages.trips.forms import LocationForm


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