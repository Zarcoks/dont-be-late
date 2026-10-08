from django.contrib.auth.decorators import user_passes_test

from dont_be_late_management.models import UserPreferences


# Send back to the default location form page
def default_location_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: UserPreferences.objects.filter(user=u).exists(),
        login_url="setup", # TODO generalize into env ?
    )
    return actual_decorator(view_func)