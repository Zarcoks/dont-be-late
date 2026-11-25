import requests
from django.core.management.base import BaseCommand
from dont_be_late_management.models import Route, Stop

API_URL = (
    "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/"
    "datasets/arrets-lignes/records"
)

MODES = {
    "Tram": 0,
    "Metro": 1,
    "Rail": 2,
}

class Command(BaseCommand):
    help = "Simple import of RATP stops and routes (excluding buses for now)"

    def handle(self, *args, **options):
        limit = 100

        for mode_api, route_type in MODES.items():
            offset = 0
            self.stdout.write(f"Importing {mode_api}...")

            while True:
                where = f'operatorname like "RATP%" AND mode="{mode_api}"'
                response = requests.get(
                    API_URL,
                    params={"limit": limit, "offset": offset, "where": where},
                    timeout=30,
                )
                response.raise_for_status()
                data = response.json()
                records = data.get("results", [])

                if not records:
                    break

                for item in records:
                    stop_id = item.get("stop_id")
                    stop_name = item.get("stop_name")
                    if stop_id and stop_name:
                        Stop.objects.get_or_create(
                            stop_id=stop_id[:100],
                            defaults={"name": stop_name[:255]},
                        )

                    route_id = item.get("id")
                    if route_id:
                        Route.objects.get_or_create(
                            route_id=route_id[:100],
                            defaults={
                                "short_name": str(item.get("shortname") or "")[:50],
                                "long_name": str(item.get("route_long_name") or "")[:255],
                                "route_type": route_type,
                            },
                        )

                offset += limit
                if offset >= data.get("total_count", 0):
                    break

        self.stdout.write(self.style.SUCCESS("Import completed!"))