import os
import sys

from celery import Celery
from decouple import config
from django.apps import apps

settings_module = config("DJANGO_SETTINGS_MODULE", default=None)
if settings_module is None:
    print(
        "Error: no DJANGO_SETTINGS_MODULE found. Will NOT start devserver. "
        "Remember to create .env file at project root. "
        "Check README for more info."
    )
    sys.exit(1)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
