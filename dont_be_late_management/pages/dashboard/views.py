from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from dont_be_late_management.utils.auth.mixins import DefaultLocationRequiredMixin


class Dashboard(DefaultLocationRequiredMixin, LoginRequiredMixin, View):
    def get(self, request):
        calendars = request.user.calendars.all()
        locations = request.user.locations.all()
        return render(request, 'dont_be_late_management/dashboard/dashboard.html', {"calendars": calendars, "locations": locations})