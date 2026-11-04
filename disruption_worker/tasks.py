import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def check_upcoming_trips():
    logger.info("tâche check_upcoming_trips lancée")