from django.contrib import admin

from dont_be_late_management.models import *

# Register your models here.
admin.site.register(Calendar)
admin.site.register(Location)
admin.site.register(CalendarEvent)
admin.site.register(Trip)
admin.site.register(Line)
admin.site.register(GuessLog)