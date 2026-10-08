from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from dont_be_late_management.models import UserPreferences


class DefaultLocationRequiredMixin(UserPassesTestMixin):
    """Verify that the current user has registered his default location."""

    def test_func(self):
        return UserPreferences.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        return redirect("setup")
