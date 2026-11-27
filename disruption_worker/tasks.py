import logging
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from disruption_worker.services.idfm import IdfmError, fetch_disruptions
from disruption_worker.services.disruption import parse_disruptions
from disruption_worker.services.planning import first_events_of_day

logger = logging.getLogger(__name__)


@shared_task
def check_upcoming_trips():
    logger.info("tâche check_upcoming_trips lancée")

@shared_task
def worker_for_tomorrow():
    #Get events for tomorrow
    tomorrow = timezone.localdate() + timedelta(days=1)
    events_user = first_events_of_day(tomorrow)
    print(f"{len(events_user)} événement le {tomorrow}")

    #Call Idfm API
    if not events_user : 
        print("Pas d'événements, pas d'appel API")
        return

    data = fetch_disruptions()

    #Transform JSON to Python
    if not data : 
        print("Pas de perturbations")
        return
    
    disruptions = parse_disruptions(data)
    print(f"{len(disruptions)} perturbations récupérées")

    #TODO : search disruption per trip and user estimate_delay_user to get delay_max