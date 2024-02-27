from datetime import date, datetime

from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload, selectinload
from typing_extensions import List

from app.models.task import Task
from app.core.db import AsyncSessionLocal
from app.crud.validators import validate_task_data
from app.crud.base import BaseCRUD


class TaskCRUD(BaseCRUD):
    model = Task

    async def create_task(self, task_data):
        validate=validate_task_data(task_data)
        if validate:
            return validate
        query=insert(self.model).values(**task_data).returning(self.model.id)
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    async def get(self, task_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(self.model).options(
                    selectinload(Task.user),
                )
            )