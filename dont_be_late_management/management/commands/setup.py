import requests
from django.core.management.base import BaseCommand
from dont_be_late_management.models import Route, Stop

API_URL = (
    "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/"
    "datasets/arrets-lignes/records"
)

# Exact IDFM mode values -> (route_type, display_name prefix)
MODES = {
    "Tramway": (0, "Tram"),
    "Metro": (1, "Metro"),
    "RapidTransit": (2, "RER"),
}


class Command(BaseCommand):
    help = "Simple import of stops and routes for Tramway, Metro, and RER"

    def handle(self, *args, **options):
        limit = 100

        for mode_api, (route_type, transport_label) in MODES.items():
            offset = 0
            self.stdout.write(f"Importing {mode_api} ({transport_label})...")

            while True:
                response = requests.get(
                    API_URL,
                    params={
                        "limit": limit,
                        "offset": offset,
                        "where": f'mode="{mode_api}"',
                    },
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
                        short_name = str(item.get("shortname") or "").strip()[:50]
                        long_name = str(item.get("route_long_name") or "").strip()[:255]
                        display_name = (
                            f"{transport_label} {short_name}".strip()
                            if short_name
                            else transport_label
                        )[:500]

                        Route.objects.get_or_create(
                            route_id=route_id[:100],
                            defaults={
                                "display_name": display_name,
                                "short_name": short_name,
                                "long_name": long_name,
                                "route_type": route_type,
                            },
                        )

                offset += limit
                if offset >= data.get("total_count", 0):
                    break

        self.stdout.write(self.style.SUCCESS("Import completed!"))