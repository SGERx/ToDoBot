from app.crud.base import BaseCRUD
from app.models.task import Task


class TaskCRUD(BaseCRUD):
    model = Task
