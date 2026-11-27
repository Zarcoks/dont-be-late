from django.db import models
from dont_be_late_management.models import CalendarEvent
# Create your models here.

class AlertAlreadySent(models.Model):
    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    disruption_id = models.CharField(max_length=255)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "disruption_id"], 
                name="unique_alert_per_event_and_disruption"
            )
        ]

    def __str__(self):
        return f"{self.event_id} / {self.disruption_id}"
    