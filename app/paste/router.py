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


router = APIRouter(
    prefix='/paste',
    tags=['Paste']
)


@router.get('/{id_paste}')
async def get_paste(id_paste: str, session: AsyncSession = Depends(db.get_async_session)):
    query = sql.select(md.Paste).where(md.Paste.id == id_paste)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/{id_paste}')
async def add_paste(new_paste: schemas.PasteCreate, session: AsyncSession = Depends(db.get_async_session)):
    response = requests.get(config.GEN_ID_URL).json()

    stmt = sql.insert(md.Paste).values(id=response['id'], url='http', date_creation=new_paste.date, date_delete=new_paste.lifetime)
    await session.execute(stmt)
    await session.commit()
    return {'status': 'ok'}
