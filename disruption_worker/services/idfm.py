import requests
from django.conf import settings

DISRUPTIONS_PATH = "/disruptions_bulk/disruptions/v2" 
TIMEOUT_SECONDS = 30

#API which converts idfm response to JSON
def fetch_disruptions():
    
    if not settings.IDFM_API_KEY:
        raise IdfmError("API key error not set")

    url = settings.IDFM_BASE_URL + DISRUPTIONS_PATH
    
    response = requests.get(
        url,
        headers={"apikey": settings.IDFM_API_KEY, "Accept": "application/json"},
        timeout=TIMEOUT_SECONDS,
    )

    if response.status_code != 200:
        raise IdfmError(f"API IDFM : HTTP {response.status_code} {response.text[:200]}")

    data = response.json()

    return data