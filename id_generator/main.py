from fastapi import FastAPI, Depends
import id_generator.generator as gen
from sqlalchemy.ext.asyncio import AsyncSession
import database.database as db


id_generator = gen.Generator()
app = FastAPI()


@app.get('/')
async def default(session: AsyncSession = Depends(db.get_async_session)):
    if len(id_generator) == 0:
        await id_generator.generate(session)

    result = {
        'id': id_generator.get_id()
    }

    return {
        'status': 'ok',
        'data': result,
        'details': None
    }


@app.get('/check-ids')
async def check_number_of_ids(session: AsyncSession = Depends(db.get_async_session)):
    remains = len(id_generator)

    if remains < 1000:
        await id_generator.generate(session)
        result = 'success generate!'
    else:
        result = f'remains: {remains}'

    return {
        'status': 'ok',
        'data': result,
        'details': None
    }

