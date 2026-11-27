import requests
from django.core.management.base import BaseCommand
from dont_be_late_management.models import Route, Stop

API_URL = (
    "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/"
    "datasets/arrets-lignes/records"
)

MODES = {
    "Tramway": (0, "Tram"),
    "Metro": (1, "Metro"),
    "RapidTransit": (2, "RER"),
}


class Command(BaseCommand):
    help = "Import stops, routes, and stop-route relations"

    def handle(self, *args, **options):
        for mode_api, (route_type, prefix) in MODES.items():
            self.stdout.write(f"Importing {prefix} ({mode_api})...")
            records = self.fetch_records_for_mode(mode_api)

            for row in records:
                stop = self.get_or_create_stop(row)
                route = self.get_or_create_route(row, route_type, prefix)

                if stop and route:
                    stop.routes.add(route)

        self.stdout.write(self.style.SUCCESS("Import completed!"))

    def fetch_records_for_mode(self, mode_api):
        all_records = []
        offset = 0
        limit = 100

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

            page_records = data.get("results", [])
            if not page_records:
                break

            all_records.extend(page_records)
            offset += limit

            if offset >= data.get("total_count", 0):
                break

        return all_records

    def get_or_create_stop(self, row):
        stop_id = row.get("stop_id")
        stop_name = row.get("stop_name")

        if not stop_id or not stop_name:
            return None

        stop, _ = Stop.objects.get_or_create(
            stop_id=stop_id[:100],
            defaults={"name": stop_name[:255]},
        )
        return stop

    def get_or_create_route(self, row, route_type, prefix):
        route_id = row.get("id")
        if not route_id:
            return None

        short_name = str(row.get("shortname") or "").strip()[:50]
        long_name = str(row.get("route_long_name") or "").strip()[:255]

        if short_name:
            display_name = f"{prefix} {short_name}"
        else:
            display_name = prefix

        route, _ = Route.objects.get_or_create(
            route_id=route_id[:100],
            defaults={
                "display_name": display_name[:500],
                "short_name": short_name,
                "long_name": long_name,
                "route_type": route_type,
            },
        )
        return route