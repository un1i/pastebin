import celery
import requests
from id_generator import config

REDIS = config.REDIS
celery = celery.Celery('tasks', broker=REDIS)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10,
        check.s(),
        name='check ids every 10 seconds'
    )


@celery.task(queue='check_ids')
def check():
    return requests.get(config.CHECK_IDS_URL).json()
