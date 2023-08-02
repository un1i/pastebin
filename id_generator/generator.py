import random
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sql
import database.models as md


class Generator:
    __CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*-'
    __NUMBER_OF_IDS = 10000

    def __init__(self):
        self.__ids = set()

    def get_id(self):
        return self.__ids.pop()

    @classmethod
    def __generate_id(cls):
        result = ''.join(random.choices(cls.__CHARS, k=8))
        return result

    async def generate(self, session: AsyncSession):
        new_ids = set()
        for _ in range(self.__NUMBER_OF_IDS):
            elem = self.__generate_id()
            new_ids.add(elem)

        exist_ids = await self.__get_exist_ids_in_database(new_ids, session)
        new_ids -= exist_ids
        self.__ids.update(new_ids)

    @staticmethod
    async def __get_exist_ids_in_database(ids: set, session: AsyncSession):
        query = sql.Select(md.Paste).where(md.Paste.id.in_(ids))
        response = await session.execute(query)
        response = response.scalars().all()
        exist_ids = set(map(lambda x: x.id, response))
        return exist_ids

    def __len__(self):
        return len(self.__ids)
