from django.shortcuts import render


def index(request):
    return render(request, 'dont_be_late_management/index.html')
