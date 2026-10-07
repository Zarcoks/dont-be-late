from django import forms
import requests
from dont_be_late_management.models import Calendar


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['name', 'url', 'default_location']

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["default_location"].queryset = user.locations.all()


    def clean_url(self):
        url = self.cleaned_data["url"].strip()
        try:
            req = requests.get(url, timeout=10, allow_redirects=True)
        except Exception as e:
            raise forms.ValidationError(f"Impossible to fetch the url : {e}") from e
        if not req.ok:
            raise forms.ValidationError(f"Impossible to fetch the url (the server responded {req.status_code})")
        if not req.text.lstrip().startswith("BEGIN:VCALENDAR"):
            raise forms.ValidationError("The url did not fetch a valid ics format.")
        return url