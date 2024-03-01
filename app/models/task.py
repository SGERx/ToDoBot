from sqlalchemy import (Column, Date, ForeignKey, Integer, String, Text, Time,
                        select)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (Mapped, Session, mapped_column, relationship,
                            selectinload)

from app.core.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    task_date = Column(Date)
    task_time = Column(Time)
    status = Column(String(50), nullable=False)

    @classmethod
    async def get_active_tasks(cls, session: AsyncSession):
        async with session.begin():
            result = await session.execute(cls.__table__.select().where(cls.status != 'Выполнено'))
            return result.all()

    @classmethod
    async def get_tasks(cls, session: AsyncSession):
        async with session.begin():
            result = await session.execute(cls.__table__.select())
            return result.all()

    @classmethod
    async def get_task_by_id(cls, session: AsyncSession, task_id: int):
        async with session.begin():
            result = await session.execute(
                select(cls).where(cls.id == task_id)
            )
            task = result.scalars().one_or_none()
            print(f'Объект task - {task}')
            print(f'Тип объекта task - {type(task)}')
            return task

    @classmethod
    async def delete_task(cls, session: AsyncSession, task_id: int):
        async with session.begin():
            result = await session.execute(select(cls).where(cls.id == task_id))
            task = result.scalars().first()
            if task:
                await session.delete(task)
                await session.commit()
            else:
                return "Удаление невозможно - данные о переданном ID задания отсутствуют в базе"

    def __repr__(self):
        try:
            return f"Задача {self.title} с id {self.id}, статус {self.status}: {self.description}, назначена на дату {self.task_date} время {self.task_time}"
        except Exception as e:
            print(f"Ошибка представления класса Task - {e}")
