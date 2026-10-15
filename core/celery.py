import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('dont_be_late')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.autodiscover_tasks(['calendar_worker'], related_name='tasks')

app.conf.timezone = 'Europe/Paris'

app.conf.beat_schedule = {
    'sync_calendars': {
        'task': 'calendar_worker.sync_calendars',
        'schedule': 3600, # in seconds
    },
}
