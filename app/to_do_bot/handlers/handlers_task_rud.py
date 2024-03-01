from aiogram import F, Router, types
from aiogram.dispatcher import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove

from app.models.task import Task

from ..states import StateAdmin

rud_router = Router()
