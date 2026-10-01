from django import forms
import requests
from dont_be_late_management.models import Calendar


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['name', 'url', 'default_location']

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["default_location"].queryset = user.locations.all()


    def clean_url(self):
        url = self.cleaned_data["url"]
        try:
            req = requests.get(url, timeout=10, allow_redirects=True)
            if not req.ok:
                forms.ValidationError(f"Impossible to fetch the url (the server responded {req.status_code})")
            if not req.text.lstrip().startswith("BEGIN:VCALENDAR"): # ics hardcoded for the moment TODO test this
                forms.ValidationError("The url did not fetch a valid ics format.")
        except Exception as e:
            raise forms.ValidationError(f"Impossible to fetch the url : {e}") from e
        # raise forms.ValidationError("Unknown calendar url formal.")
        #
        # for available_extension in Calendar.AVAILABLE_URL_EXTENSIONS:
        #     if url.split('.')[-1] == available_extension:
        # # the url here has a valid format