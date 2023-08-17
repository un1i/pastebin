from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import app.exception as exc
from database import database as db
from database import models as md
import datetime as dt
import sqlalchemy as sql
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix='/profile',
    tags=['Profile']
)


@router.get('/{user_id}')
async def get_profile(user_id: int, session: AsyncSession = Depends(db.get_async_session)):
    try:
        query = sql.select(md.User).options(selectinload(md.User.pastes)).where(md.User.id == user_id)
        response = await session.execute(query)
        response = response.scalars().all()
        if len(response) == 0:
            raise exc.NotFoundError
        response = response[0]

        user = {
            'id': response.id,
            'username': response.username,
            'date_registration': response.date_registration,
        }

        pastes = list(filter(lambda paste: paste.date_delete > dt.datetime.utcnow(), response.pastes))
        pastes.sort(key=lambda paste: paste.date_creation, reverse=True)

        result = {
            'user': user,
            'pastes': pastes,
        }
        return {
            'status': 'ok',
            'data': result,
            'details': None
        }

    except exc.NotFoundError:
        raise exc.HTTPException(
            status_code=404,
            details='данного пользователя не существует'
        )
    except (OSError, SQLAlchemyError) as e:
        print(e)
        raise exc.HTTPException(
            status_code=500,
            details='Ошибка получения данных из базы даннх'
        )
    except Exception as e:
        print(e)
        raise exc.HTTPException(
            status_code=500,
            details='Ошибка выполнения запроса'
        )
