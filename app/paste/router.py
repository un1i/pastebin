import os
import sys
import sqlalchemy as sql
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
from app import database as db
import schemas
import models as md


router = APIRouter(
    prefix='/paste',
    tags=['Paste']
)


@router.get('/{hash_paste}')
async def get_paste(hash_paste: str, session: AsyncSession = Depends(db.get_async_session)):
    query = sql.select(md.Paste).where(md.Paste.hash == hash_paste)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/{hash_paste}')
async def add_paste(new_paste: schemas.PasteCreate, session: AsyncSession = Depends(db.get_async_session)):
    stmt = sql.insert(md.Paste).values(hash='125', url='http', date_creation=new_paste.date, date_delete=new_paste.lifetime)
    await session.execute(stmt)
    await session.commit()
    return {'status': 'ok'}
