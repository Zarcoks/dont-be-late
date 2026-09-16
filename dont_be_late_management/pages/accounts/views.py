from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.shortcuts import render, redirect

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm(request)
        return render(request, 'dont_be_late_management/accounts/login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(request)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard") # TODO
        # In case of HTMX request, we just want to send the partial:
        template = "dont_be_late_management/accounts/partials/login_form.partial.html" if request.headers.get("HX-Request") else "dont_be_late_management/accounts/login.html"
        return render(request, template, {"form": form})