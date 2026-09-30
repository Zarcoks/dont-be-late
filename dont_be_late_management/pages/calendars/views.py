from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect

from dont_be_late_management.models import Calendar
from dont_be_late_management.pages.calendars.forms import CalendarForm


@login_required
# Get the dashboard page for calendars
def calendar_main(request):
    calendars = request.user.calendars.all()
    locations = request.user.locations.all()
    form = CalendarForm(user=request.user) # temp

    return render(request, 'dont_be_late_management/calendars/calendars.html', {"calendars": calendars, "locations": locations, "form": form})


@login_required
class NewCalendar(View):
    def get(self, request):
        form = CalendarForm(user=request.user)
        return render(request, 'dont_be_late_management/calendars/partials/calendars_form.html', {"form": form})

    def post(self, request):
        form = CalendarForm(request.POST, instance=Calendar(user=request.user), user=request.user)
        if form.is_valid():
            form.save()
            return redirect("calendars")
        return render(request, 'dont_be_late_management/calendars/partials/calendars_form.html', {"form": form})