import celery
from celery.schedules import crontab
import sqlalchemy as sql
import datetime as dt
import app.storage_interaction as si
from database import database as db
import database.models as md
from app import config

REDIS = config.REDIS
celery = celery.Celery('tasks', broker=REDIS)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        clear_database.s(),
        name='every midnight clear db',
        )


@celery.task(queue='clear_db')
def clear_database():
    connect = db.get_connect()
    query = sql.select(md.Paste).where(md.Paste.date_delete < dt.datetime.utcnow())
    response = connect.execute(query)
    items = response.scalars().all()

    storage = si.ObjectStorage()
    result = storage.delete(items)
    print(result)

    stmt = sql.delete(md.Paste).filter(md.Paste.id.in_(items))
    connect.execute(stmt)

    connect.commit()
    connect.close()
