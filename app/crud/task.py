from datetime import date, datetime

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import joinedload, selectinload
from typing_extensions import List

from app.core.db import AsyncSessionLocal
from app.crud.base import BaseCRUD
from app.crud.validators import validate_task_data
from app.models.task import Task

from .base import BaseCRUD


class TaskCRUD(BaseCRUD):
    model = Task
