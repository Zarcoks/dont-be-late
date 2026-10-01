from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect

from dont_be_late_management.models import Calendar
from dont_be_late_management.pages.calendars.forms import CalendarForm


@login_required
def calendar_list(request):
    calendars = request.user.calendars.all()
    return render(request, 'dont_be_late_management/calendars/partials/calendars_list.html', {"calendars": calendars})


class NewCalendar(LoginRequiredMixin, View):
    def get(self, request):
        form = CalendarForm(user=request.user)
        return render(request, 'dont_be_late_management/calendars/partials/calendars_form.html', {"form": form})

    def post(self, request):
        form = CalendarForm(request.POST, instance=Calendar(user=request.user), user=request.user)
        if form.is_valid():
            form.save()
            calendars = request.user.calendars.all()
            return render(request, 'dont_be_late_management/calendars/partials/calendars_list.html',
                          {"calendars": calendars})
        return render(request, 'dont_be_late_management/calendars/partials/calendars_form.html', {"form": form})