from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from app.core.db import AsyncSessionLocal
from app.crud.base import BaseCRUD
from app.crud.validators import validate_user_data
from app.models.task import Task
from app.models.user import User


class UserCRUD(BaseCRUD):
    model = User

    def __init__(self, validator=None):
        self.validator = validator or validate_user_data

    async def create(self, user_data):
        validate = self.validator(user_data)
        if validate:
            return validate

        query = insert(self.model).values(**user_data).returning(self.model)
        return await self._execute_query(query)

    async def update_user(self, user_id: int, new_data: dict):
        result = await self.get_by_id(user_id)
        user = result.scalar()

        if user:
            for attr, value in new_data.items():
                setattr(user, attr, value)
            await self._commit()
        else:
            return "Изменение невозможно - данные о переданном ID пользователя отсутствуют в базе"

    async def get_by_id(self, id_data):
        query = select(self.model).where(self.model.id == id_data)
        return await self._execute_query(query)

    async def get_user_tasks(self, user_id: int):
        query = select(Task).options(selectinload(Task.user)).where(Task.user_id == user_id)
        return await self._execute_query(query)

    async def _commit(self):
        async with AsyncSessionLocal() as session:
            await session.commit()
