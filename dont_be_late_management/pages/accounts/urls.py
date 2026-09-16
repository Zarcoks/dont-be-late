from django.urls import path
from . import views

urlpatterns = [
    # https://docs.djangoproject.com/en/6.1/topics/auth/default/#using-the-views
    path("login/", views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
