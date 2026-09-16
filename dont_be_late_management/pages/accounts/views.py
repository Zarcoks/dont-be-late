from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'dont_be_late_management/accounts/login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
        # In case of HTMX request, we just want to send the partial:
        template = "dont_be_late_management/accounts/partials/login_form.partial.html" if request.headers.get("HX-Request") else "dont_be_late_management/accounts/login.html"
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
            "HX-Request") else "dont_be_late_management/accounts/login.html"
        return render(request, template, {"form": form})


class LogOut(LogoutView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs) # logout logic
        if request.headers.get("HX-Request"):
            return HttpResponse(headers={"HX-Redirect": self.get_success_url()}) # Takes next if given, LOGOUT_REDIRECT_UTL else
        return redirect(self.get_success_url())