import datetime as dt
import os
import sys
import requests
from requests.exceptions import RequestException, ConnectionError
import sqlalchemy as sql
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from botocore.exceptions import BotoCoreError, ClientError
from sqlalchemy.exc import SQLAlchemyError

sys.path.append('..')
sys.path.append(os.path.dirname(__file__))
import schemas
from app import storage_interaction as si, config
from database import database as db, models as md
from app.date_calculation import get_date_delete
from app.auth.auth import fastapi_users
import app.exception as exc

router = APIRouter(
    prefix='/paste',
    tags=['Paste'],
)

current_user = fastapi_users.current_user(optional=True)
current_user_authenticated = fastapi_users.current_user()


@router.get('/{id_paste}')
async def get_paste(id_paste: str, session: AsyncSession = Depends(db.get_async_session)):
    try:
        if len(id_paste) != 8:
            raise exc.LengthError

        query = sql.select(md.Paste).options(selectinload(md.Paste.author)).where(md.Paste.id == id_paste)
        response = await session.execute(query)
        response = response.scalars().all()

        if len(response) == 0 or response[0].date_delete < dt.datetime.utcnow():
            raise exc.LifeTimeError

        response = response[0]

        storage = si.ObjectStorage()
        message = storage.get(response.id)

        if response.author is not None:
            author = {
                'id': response.author.id,
                'username': response.author.username,
            }
        else:
            author = None

        result = {
            'id': response.id,
            'message': message,
            'date_creation': response.date_creation,
            'date_delete': response.date_delete,
            'author': author,
        }
        return {
            'status': 'ok',
            'data': result,
            'details': None
        }

    except exc.LifeTimeError:
        raise exc.HTTPException(
            status_code=404,
            details='У данной записи истек срок действия'
        )
    except exc.LengthError as e:
        raise exc.HTTPException(
            status_code=422,
            details='Идентификатор записи должен состоять из 8 символов'
        )
    except (OSError, SQLAlchemyError) as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка получения данных из базы данных'
        )
    except (BotoCoreError, ClientError) as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка при получении данных из облачного хранилища'
        )
    except Exception as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка выполнения запроса'
        )


@router.post('/')
async def add_paste(new_paste: schemas.PasteCreate,
                    session: AsyncSession = Depends(db.get_async_session),
                    user: db.User = Depends(current_user)
                    ):
    try:
        response = requests.get(config.GEN_ID_URL)
        if response.status_code != 200:
            raise RequestException('в сервисе id_generator возникла ошибка, новый идентификатор не был получен')
        response = response.json()

        storage = si.ObjectStorage()
        storage.put(response['data']['id'], new_paste.message)

        date_creation = dt.datetime.utcnow()
        date_delete = get_date_delete(date_creation, new_paste.lifetime)
        user_id = user.id if user is not None else None
        stmt = sql.insert(md.Paste).values(
            id=response['data']['id'],
            date_creation=date_creation,
            date_delete=date_delete,
            author_id=user_id
        )
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

    except ConnectionError as e:
        print(e)
        raise HTTPException(
            status_code=503,
            detail='Не удается подключиться к сервису генерации идентификаторов'
        )

    except RequestException as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Возникла ошибка при получении идентификатора'
        )

    except (BotoCoreError, ClientError) as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка при получении данных из облачного хранилища'
        )
    except (OSError, SQLAlchemyError) as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка при сохранении данных в базу данных'
        )
    except Exception as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка выполнения запроса'
        )


@router.get('/delete/{id_paste}')
async def delete_paste(id_paste: str,
                       session: AsyncSession = Depends(db.get_async_session),
                       user: db.User = Depends(current_user_authenticated)
                       ):
    try:
        query = sql.select(md.Paste).where(md.Paste.id == id_paste)
        response = await session.execute(query)
        response = response.scalars().all()
        if len(response) == 0:
            raise exc.NotFoundError

        paste = response[0]
        if paste.author_id != user.id:
            raise exc.AuthorError

        storage = si.ObjectStorage()
        storage.delete([id_paste])

        stmt = sql.delete(md.Paste).where(md.Paste.id == id_paste)
        await session.execute(stmt)
        await session.commit()

        return {
            'status': 'ok',
            'data': None,
            'details': None
        }

    except exc.NotFoundError:
        raise HTTPException(status_code=404, detail={
            'status': 'error',
            'data': None,
            'details': 'Запись не найдена'
        })
    except exc.AuthorError:
        raise HTTPException(status_code=403, detail={
            'status': 'error',
            'data': None,
            'details': 'Вы не являетесь автором данной записи'
        })
    except (BotoCoreError, ClientError) as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка при получении данных из облачного хранилища'
        )
    except (OSError, SQLAlchemyError) as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка при сохранении данных в базу данных'
        )
    except Exception as e:
        print(e)
        raise exc.HTTPException(
            status_code=503,
            details='Ошибка выполнения запроса'
        )




