from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogOut.as_view(), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
]
