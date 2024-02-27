from sqlalchemy import (Column, Date, ForeignKey, Integer, String, Text, Time,
                        select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    task_date = Column(Date)
    task_time = Column(Time)
    status = Column(String(50), nullable=False)


def __repr__(self):
    try:
        return f"Задача {self.title} с id {self.id}, статус {self.status}: {self.description}, назначена на дату {self.task_date} время {self.task_time}"
    except Exception as e:
        print(f"Ошибка представления класса Task - {e}")
