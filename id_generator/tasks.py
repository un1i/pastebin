import celery
import requests
import config

celery = celery.Celery('tasks', broker='redis://localhost:6379')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10,
        check.s(),
        name='check ids every 10 seconds'
    )


@celery.task
def check():
    return requests.get(config.CHECK_IDS_URL).json()
