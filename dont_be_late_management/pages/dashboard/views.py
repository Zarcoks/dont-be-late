from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect

from dont_be_late_management.models import Calendar, Location


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        calendars = request.user.calendars.all()
        locations = request.user.locations.all()
        return render(request, 'dont_be_late_management/dashboard/dashboard.html', {"calendars": calendars, "locations": locations})