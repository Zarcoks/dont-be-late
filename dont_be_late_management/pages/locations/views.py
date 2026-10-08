from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from dont_be_late_management.models import Location, UserPreferences
from dont_be_late_management.pages.locations.forms import LocationForm


@login_required
def get_locations(request):
    locations = request.user.locations.all()
    return render(request, 'dont_be_late_management/locations/partials/locations_list.html', {"locations": locations})


class NewLocation(LoginRequiredMixin, View):
    def get(self, request):
        form = LocationForm()
        return render(request, 'dont_be_late_management/locations/partials/locations_form.html', {"form": form})

    def post(self, request):
        form = LocationForm(request.POST, instance=Location(user=request.user))
        if form.is_valid():
            location = form.save()
            if not UserPreferences.objects.filter(user=request.user).exists():
                UserPreferences.objects.update_or_create(user=request.user, default_location=location)
            locations = request.user.locations.all()
            return render(request, 'dont_be_late_management/locations/partials/locations_list.html', {"locations": locations})
        return render(request, 'dont_be_late_management/locations/partials/locations_form.html', {"form": form})