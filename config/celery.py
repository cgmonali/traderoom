import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)


app = Celery(
    "traderoom"
)


app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)


app.autodiscover_tasks()


app.conf.beat_schedule = {
    "update-market-prices-every-minute": {
        "task": "rooms.tasks.update_market_prices",
        "schedule": 60.0,
    },
}