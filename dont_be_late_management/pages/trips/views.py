from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def trips_dashboard(request):
    return render(request, 'dont_be_late_management/trips/trips.html')
