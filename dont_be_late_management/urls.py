from django.urls import include, path

urlpatterns = [
    path("", include("dont_be_late_management.pages.accounts.urls")),
    path("", include("dont_be_late_management.pages.dashboard.urls")),
]
