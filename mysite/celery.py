import os
from celery import Celery

# Ensure Django is set up
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django

django.setup()

app = Celery("mysite")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60 * 5, run_next_scan_process.s(), name='Process next scan', )


@app.task
def run_next_scan_process():
    from api.tasks import process_next_scan
    process_next_scan()
