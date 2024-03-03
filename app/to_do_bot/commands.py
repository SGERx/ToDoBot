from datetime import datetime, time

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, ReplyKeyboardRemove)
from aiogram.fsm.context import FSMContext
from app.core.db import AsyncSessionLocal
from app.crud.task import TaskCRUD
from app.models.task import Task

from .states import StateAdmin

command_router = Router()
task_crud = TaskCRUD()
keyboard_router = Router()


async def send_message_with_state(message: Message, state: MemoryStorage, text: str, reply_markup=None, new_state=None):
    await message.answer(text, reply_markup=reply_markup)
    if new_state:
        await state.set_state(new_state)


@command_router.message(Command("start"))
async def command_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Создать задачу"),
            types.KeyboardButton(text="Просмотреть задачи"),
            types.KeyboardButton(text="Просмотреть активные"),
            types.KeyboardButton(text="Завершить задачу"),
            types.KeyboardButton(text="Удалить задачу")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите нужное действие"
    )
    await message.answer("Какое действие с задачей требуется?", reply_markup=keyboard)


@keyboard_router.message(F.text.lower() == "создать задачу")
async def task_creation_one(message: types.Message, state: FSMContext):
    await state.set_state(StateAdmin.task_creation_one)
    await message.reply(text="Cоздание новой задачи - введите заголовок новой задачи")
    await state.set_state(StateAdmin.task_creation_two)


@keyboard_router.message(F.text.lower() == "просмотреть задачи")
async def view_tasks(message: types.Message, state: FSMContext):
    session = AsyncSessionLocal()
    active_tasks = await Task.get_tasks(session)
    if active_tasks:
        task_list = "\n".join([f"{task.id}. {task.title} ({task.status})" for task in active_tasks])
        await message.answer(f"Список всех задач:\n{task_list}")
    else:
        await message.answer("У вас нет задач.")


@keyboard_router.message(F.text.lower() == "просмотреть активные")
async def view_active_tasks(message: types.Message, state: FSMContext):
    session = AsyncSessionLocal()
    tasks = await Task.get_active_tasks(session)
    if tasks:
        task_list = "\n".join([f"{task.id}. {task.title} ({task.status})" for task in tasks])
        await message.answer(f"Список активных задач:\n{task_list}")
    else:
        await message.answer("У вас нет активных задач.")


@keyboard_router.message(F.text.lower() == "завершить задачу")
async def complete_task(message: types.Message, state: MemoryStorage):
    await message.answer("Введите номер задачи для пометки как выполненной:")
    await state.set_state(StateAdmin.awaiting_task_id_for_completion)


@keyboard_router.message(StateFilter(StateAdmin.awaiting_task_id_for_completion))
async def complete_task_by_id(message: types.Message, state: MemoryStorage):
    task_id = int(message.text)
    session = AsyncSessionLocal()

    try:
        task = await Task.get_task_by_id(session, task_id)

        if task and isinstance(task, Task):
            task.status = 'Выполнено'
            await session.commit()
            await message.answer(f"Задача с id {task_id} помечена как выполненная.")
        else:
            await message.answer(f"Задачи с id {task_id} не существует.")
    finally:
        await session.close()


@keyboard_router.message(F.text.lower() == "удалить задачу")
async def delete_task_by_id(message: types.Message, state: MemoryStorage):
    await message.answer("Введите номер задачи для удаления:")
    await state.set_state(StateAdmin.awaiting_task_id_for_deletion)


@keyboard_router.message(StateFilter(StateAdmin.awaiting_task_id_for_deletion))
async def delete_task_by_id_continue(message: types.Message, state: MemoryStorage):
    task_id = int(message.text)
    session = AsyncSessionLocal()

    try:
        task = await Task.get_task_by_id(session, task_id)

        if task and isinstance(task, Task):
            await Task.delete_task(session, task_id)
            await session.commit()
            await message.answer(f"Задача с id {task_id} удалена")
        else:
            await message.answer(f"Задачи с id {task_id} не существует.")
    finally:
        await session.close()
