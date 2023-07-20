import datetime
import os
import sys
import requests
import sqlalchemy as sql
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
from app import database as db, config
import schemas
import models as md
from app import storage_interaction as si
from app.date_calculation import get_date_delete

router = APIRouter(
    prefix='/paste',
    tags=['Paste']
)


@router.get('/{id_paste}')
async def get_paste(id_paste: str, session: AsyncSession = Depends(db.get_async_session)):
    query = sql.select(md.Paste).where(md.Paste.id == id_paste)
    response = await session.execute(query)
    response = response.scalars().all()[0]

    storage = si.ObjectStorage()
    message = storage.get(response.id)

    result = {
        'id': response.id,
        'message': message,
        'date_creation': response.date_creation,
        'date_delete': response.date_delete
    }
    return {
        'status': 'ok',
        'data': result,
        'details': None
    }


@router.post('/')
async def add_paste(new_paste: schemas.PasteCreate, session: AsyncSession = Depends(db.get_async_session)):
    response = requests.get(config.GEN_ID_URL).json()

    storage = si.ObjectStorage()
    storage.put(response['data']['id'], new_paste.message)

    date_creation = datetime.datetime.utcnow()
    date_delete = get_date_delete(date_creation, new_paste.lifetime)

    stmt = sql.insert(md.Paste).values(id=response['data']['id'], date_creation=date_creation, date_delete=date_delete)
    await session.execute(stmt)
    await session.commit()

    result = {
        'id': response['data']['id']
    }
    return {
        'status': 'ok',
        'data': result,
        'details': None
    }
