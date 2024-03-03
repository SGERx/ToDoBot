from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class TaskDB(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    task_date: Optional[date] = None
    task_time: Optional[time] = None
    status: str

    class Config:
        orm_mode = True
