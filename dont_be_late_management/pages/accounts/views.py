from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views import View
from django.shortcuts import render, redirect, resolve_url

from dont_be_late_management.models import UserPreferences
from dont_be_late_management.pages.locations.forms import LocationForm
from dont_be_late_management.utils.utils import hx_or_http_redirect


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'dont_be_late_management/accounts/login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")

        template = "dont_be_late_management/accounts/partials/login_form.partial.html" if request.headers.get(
            "HX-Request") else "dont_be_late_management/accounts/login.html"
        return render(request, template, {"form": form})


class SignUp(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'dont_be_late_management/accounts/signup.html', {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

        template = "dont_be_late_management/accounts/partials/signup_form.partial.html" if request.headers.get(
            "HX-Request") else "dont_be_late_management/accounts/signup.html"
        return render(request, template, {"form": form})


class LogOut(LogoutView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs) # logout logic
        return hx_or_http_redirect(request, self.get_success_url())


class DefaultLocationForm(LoginRequiredMixin, View):
    def get(self, request):
        if not UserPreferences.objects.filter(user=request.user).exists():
            form = LocationForm(suggested_name="Home")
            return render(request, 'dont_be_late_management/accounts/preferences_form.html', {"form": form})
        return hx_or_http_redirect(request, resolve_url("dashboard"))