from datetime import datetime, time

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove
from app.core.db import AsyncSessionLocal

from app.crud.task import TaskCRUD
from app.models.task import Task

from .states import StateAdmin

command_router = Router()
task_crud = TaskCRUD()


async def send_message_with_state(message: Message, state: MemoryStorage, text: str, reply_markup=None, new_state=None):
    await message.answer(text, reply_markup=reply_markup)
    if new_state:
        await state.set_state(new_state)


@command_router.message(Command("start"))
async def command_start(message: Message, state: MemoryStorage) -> None:
    text = (
        f"Добрый день, {message.from_user.full_name}!\n"
        "Для перезапуска нажмите                 /start \n"
        "Для записи новой задачи нажмите      /task_creation \n"
        "Для просмотра активных задач нажмите    /view_active_tasks \n"
        "Для просмотра всех существующих задач нажмите    /view_tasks \n"
        "Для завершения задачи нажмите /complete_task \n"
        "Для удаления задачи нажмите /delete_task \n"
    )
    await send_message_with_state(message, state, text, new_state=StateAdmin.start_menu)


# @command_router.message(Command("task_creation"))
# async def command_task(message: Message, state: FSMContext):
#     await send_message_with_state(
#         message, state, "Переходим в меню создания новой задачи", reply_markup=work_keyboard, new_state=StateAdmin.task_creation
#     )

@command_router.message(Command("task_creation"))
async def command_create_task(message: Message, state: MemoryStorage) -> None:
    await state.set_state(StateAdmin.task_creation_one)
    await message.reply(text="Cоздание новой задачи - введите заголовок новой задачи")
    await state.set_state(StateAdmin.task_creation_two)


# @command_router.message(Command("view_tasks"))
# async def command_view_task(message: Message, state: MemoryStorage):
#     await send_message_with_state(
#         message, state, "Переходим в меню просмотра существующих задач", reply_markup=work_keyboard,
#         new_state=StateAdmin.view_tasks
#     )


@command_router.message(Command("test_creation"))
async def command_create_test_task(message: Message, state: MemoryStorage) -> None:
    task_date = '01-03-2024'
    task_date = datetime.strptime(task_date, '%d-%m-%Y').date()
    task_time_str = '11:00:00'
    task_time = datetime.strptime(task_time_str, '%H:%M:%S').time()
    test_task_data = {
        "title": 'Тестовая задача',
        "description": 'Тестовое описание',
        "task_date": task_date,
        "task_time": task_time,
        "status": "Новая"
    }
    try:

        await task_crud.create(**test_task_data)
    except Exception as e:
        print(f"Error during database operation: {e}")

    await message.reply(text="Создание задачи подтверждено               \n"
                             "Для перезапуска нажмите             /start \n"
                             "Для записи новой задачи нажмите      /task_creation \n"
                             "Для просмотра существующих задач нажмите    /view_tasks \n")


@command_router.message(Command("view_tasks"))
async def view_tasks(message: types.Message):
    session = AsyncSessionLocal()
    active_tasks = await Task.get_tasks(session)
    if active_tasks:
        task_list = "\n".join([f"{task.id}. {task.title} ({task.status})" for task in active_tasks])
        await message.answer(f"Список всех задач:\n{task_list}")
    else:
        await message.answer("У вас нет задач.")


@command_router.message(Command("view_active_tasks"))
async def view_active_tasks(message: types.Message):
    session = AsyncSessionLocal()
    tasks = await Task.get_active_tasks(session)
    if tasks:
        task_list = "\n".join([f"{task.id}. {task.title} ({task.status})" for task in tasks])
        await message.answer(f"Список активных задач:\n{task_list}")
    else:
        await message.answer("У вас нет активных задач.")


@command_router.message(Command("complete_task"))
async def complete_task(message: types.Message, state: MemoryStorage):
    await message.answer("Введите номер задачи для пометки как выполненной:")
    await state.set_state(StateAdmin.awaiting_task_id_for_completion)


@command_router.message(StateFilter(StateAdmin.awaiting_task_id_for_completion))
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


@command_router.message(Command("delete_task"))
async def delete_task_by_id(message: types.Message, state: MemoryStorage):
    await message.answer("Введите номер задачи для удаления:")
    await state.set_state(StateAdmin.awaiting_task_id_for_deletion)


@command_router.message(StateFilter(StateAdmin.awaiting_task_id_for_deletion))
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
