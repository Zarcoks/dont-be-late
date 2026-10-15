from celery import shared_task

from . import synchroniser


@shared_task(name='calendar_worker.sync_calendars')
def sync_calendars_to_urls():
    return synchroniser.synchronise_calendars()
