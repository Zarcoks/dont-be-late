from django.contrib import admin

from dont_be_late_management.models import *

# Register your models here.
admin.site.register(Calendar)
admin.site.register(Location)
admin.site.register(CalendarEvent)
admin.site.register(Trip)
admin.site.register(TripLine)
admin.site.register(GuessLog)



@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("display_name", "short_name", "route_type", "route_id")
    search_fields = ("display_name", "short_name", "long_name", "route_id")
    list_filter = ("route_type",)


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ("name", "stop_id", "routes_list")
    search_fields = ("name", "stop_id", "routes__display_name")
    filter_horizontal = ("routes",)

    @admin.display(description="Lignes")
    def routes_list(self, obj):
        return ", ".join(obj.routes.values_list("display_name", flat=True))