from django import forms
import requests
from dont_be_late_management.models import Calendar


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ["name", "url"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
        }

    def clean_url(self):
        url = self.cleaned_data["url"]
        try:
            response = requests.get(url, timeout=10)
        except requests.RequestException:
            raise forms.ValidationError("Impossible to reach this url.")
        if not response.text.startswith("BEGIN:VCALENDAR"):
            raise forms.ValidationError("This url does not return an .ics calendar.")
        return url
