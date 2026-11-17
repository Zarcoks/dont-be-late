from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View

from calendar_worker.synchroniser import synchronise_one_calendar
from dont_be_late_management.models import Calendar, CalendarEvent
from dont_be_late_management.pages.events.forms import CalendarForm, EventEditForm


@login_required
def event_dashboard(request):
    calendar = Calendar.objects.filter(user=request.user).first()
    if calendar is None:
        return redirect("calendar")

    events = calendar.events.filter(starting_time__gte=timezone.now()).order_by("starting_time")[:21]
    return render(request, "dont_be_late_management/events/events.html", {"calendar": calendar, "events": events})


@login_required
def edit_calendar(request):
    calendar = Calendar.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = CalendarForm(request.POST, instance=calendar)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.user = request.user
            calendar.save()
            # for the moment re-import the events from scratch, in case the url changed TODO use uid to not re-import each time
            calendar.events.all().delete()
            synchronise_one_calendar(calendar)
            return redirect("event_dashboard")
    else:
        form = CalendarForm(instance=calendar)

    return render(request, "dont_be_late_management/events/calendar.html", {"form": form, "calendar": calendar})


class EventEdit(LoginRequiredMixin, View):
    def get(self, request, pk):
        event = get_object_or_404(CalendarEvent, pk=pk)
        form = EventEditForm(instance=event)
        return render(request, 'dont_be_late_management/events/partials/event_form.html', {
            'event': event,
            'form': form,
        })

    def post(self, request, pk):
        event = get_object_or_404(CalendarEvent, pk=pk)
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return render(request, 'dont_be_late_management/events/partials/event_row.html', {
                'event': event,
            })
        return render(request, 'dont_be_late_management/events/partials/event_form.html', {
            'event': event,
            'form': form,
        })


def cancel_edit_event(request, pk):
    event = get_object_or_404(CalendarEvent, pk=pk)
    return HttpResponse("")