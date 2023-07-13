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
    storage.download(response.url)

    path = f'data/{response.url}'
    file = open(path, 'r')
    message = file.read()
    file.close()
    os.remove(path)
    result = {
        'id': response.id,
        'message': message,
        'date_creation': response.date_creation,
        'date_delete': response.date_delete
    }
    return result


@router.post('/{id_paste}')
async def add_paste(new_paste: schemas.PasteCreate, session: AsyncSession = Depends(db.get_async_session)):
    response = requests.get(config.GEN_ID_URL).json()
    filename = f'{response["id"]}.txt'
    path = f'data/{filename}'

    file = open(path, 'w')
    file.write(new_paste.message)
    file.close()

    storage = si.ObjectStorage()
    storage.upload(filename)

    os.remove(path)

    stmt = sql.insert(md.Paste).values(id=response['id'], url=filename, date_creation=new_paste.date, date_delete=new_paste.lifetime)
    await session.execute(stmt)
    await session.commit()
    return {'status': 'ok'}
