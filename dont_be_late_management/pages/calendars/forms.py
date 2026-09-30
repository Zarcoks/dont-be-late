from django import forms

from dont_be_late_management.models import Calendar


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['name', 'url', 'default_location']

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["default_location"].queryset = user.locations.all()