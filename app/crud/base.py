from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal


class BaseCRUD:
    model = None

    @classmethod
    async def create(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    result = await session.execute(query)
                    return result.mappings().first()
        except Exception as e:
            print(f"Error during database operation: {e}")
            raise

    @classmethod
    async def get(cls, object_id: int):
        return await cls._execute_query(select(cls.model).where(cls.model.id == object_id))

    @classmethod
    async def get_multi(cls):
        return await cls._execute_query(select(cls.model))

    @classmethod
    async def remove(cls, db_obj_id):
        db_obj = await cls.get(db_obj_id)
        if db_obj:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    session.delete(db_obj)
            return db_obj

    @classmethod
    async def update(cls, object_id: int, data: dict):
        query = update(cls.model).where(cls.model.id == object_id).values(data).returning(cls.model)
        return await cls._execute_query(query)

    @classmethod
    async def _execute_query(cls, query):
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            return result.scalars().first()
