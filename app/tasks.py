import celery
from celery.schedules import crontab
import sqlalchemy as sql
import datetime as dt
import storage_interaction as si
import database as db
import paste.models as md

celery = celery.Celery('tasks', broker='redis://localhost:6379')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        clear_database.s(),
        name='every midnight clear db')


@celery.task
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
