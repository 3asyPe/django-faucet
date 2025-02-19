import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Optional: define the beat schedule here or in settings.py.
app.conf.beat_schedule = {
    'check-pending-transactions-every-minute': {
         'task': 'faucet.tasks.check_pending_transactions',
         'schedule': crontab(minute='*/1'),
     },
}
