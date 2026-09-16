from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), # redirect on settings.LOGOUT_REDIRECT_URL
    path("signup/", views.SignUp.as_view(), name="signup"),
]
