from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "content_platform.settings")

app = Celery("content_platform")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "renew-user": {
        "task": "accounts.tasks.renew_expired_subscriptions",
        "schedule": crontab(hour=0, minute=0),
    },
    "calculate-ai-score": {
        "task": "content.tasks.calculate_ai_relevance_scores",
        "schedule": crontab(minute="*/10"),
    },
}

app.conf.timezone = "Africa/Lagos"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
