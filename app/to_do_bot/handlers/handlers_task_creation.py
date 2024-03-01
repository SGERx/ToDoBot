from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.crud.task import TaskCRUD

from app.crud.user import UserCRUD
from app.to_do_bot.utils import parse_date, parse_time

from ..keyboards.task_keyboard import task_confirmation_keyboard
from ..states import StateAdmin

task_router = Router()
task_crud = TaskCRUD()


# Создание новой задачи - шаг 1

# @task_router.message(Command("task_creation"))
# async def task_creation_one(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(StateAdmin.task_creation_one)
#     await callback.message.answer(text="Cоздание новой задачи - введите заголовок новой задачи")
#     await state.set_state(StateAdmin.task_creation_two)


# Создание новой задачи - шаг 2

@task_router.message(StateFilter(StateAdmin.task_creation_two))
async def task_creation_two(message: Message, state: FSMContext):
    gathered_title = message.text
    await state.update_data(title=gathered_title)
    print(message.text)
    await message.reply(f"Введен заголовок задачи - {gathered_title}, введите описание задачи")
    await state.set_state(StateAdmin.task_creation_three)


# Создание новой задачи - шаг 3

@task_router.message(StateFilter(StateAdmin.task_creation_three))
async def task_creation_three(message: Message, state: FSMContext):
    gathered_description = message.text
    await state.update_data(description=gathered_description)
    print(message.text)
    await message.reply(f"Введено описание задачи - {gathered_description}, введите дату задачи")
    await state.set_state(StateAdmin.task_creation_four)


# Создание новой задачи - шаг 4

@task_router.message(StateFilter(StateAdmin.task_creation_four))
async def task_creation_four(message: Message, state: FSMContext):
    gathered_date = message.text
    await state.update_data(date=gathered_date)
    print(message.text)
    await message.reply(f"Введена дата задачи - {gathered_date}, введите время задачи")
    await state.set_state(StateAdmin.task_creation_five)


# Создание новой задачи - шаг 5

# @task_router.message(StateFilter(StateAdmin.task_creation_five))
# async def task_creation_five(message: Message, state: FSMContext):
#     gathered_time = message.text
#     await state.update_data(time=gathered_time)
#     print(message.text)
#     await message.reply(f"Введено время задачи - {gathered_time}, введите время задачи")
#     await state.set_state(StateAdmin.task_creation_six)


# Создание новой задачи - шаг 6



@task_router.message(StateFilter(StateAdmin.task_creation_five))
async def task_creation_six(message: Message, state: FSMContext):
    gathered_time = message.text
    await state.update_data(time=gathered_time)
    print(message.text)
    await state.set_state(StateAdmin.task_creation_six)
    create_task_data = await state.get_data()
    task_title = create_task_data['title']
    task_description = create_task_data['description']
    task_date = create_task_data['date']
    task_date_formatted = parse_date(task_date)
    task_time = create_task_data['time']

    await message.reply(f"Подтвердите создание задачи - заголовок '{task_title}',"
                        f"описание {task_description}, дата {task_date_formatted}, время {task_time}",
                        reply_markup=task_confirmation_keyboard)


# Создание новой задачи - отмена

@task_router.callback_query(StateFilter(StateAdmin.task_creation_six),
                            F.data == "cancel_creation_task")
async def task_creation_cancellation(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Для перезапуска нажмите             /start \n"
                                       "Для записи новой задачи нажмите      /task \n"
                                       "Для просмотра существующих задач нажмите    /view_tasks \n")

    await state.clear()


# Создание новой задачи - подтверждение

@task_router.callback_query(StateFilter(StateAdmin.task_creation_six),
                            F.data == "confirm_creation_task")
async def task_creation_confirmation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.task_creation_confirmation)

    create_task_data = await state.get_data()
    task_title = create_task_data['title']
    task_description = create_task_data['description']
    task_date = create_task_data['date']
    task_date_formatted = parse_date(task_date)
    task_time = create_task_data['time']
    task_time_formatted = parse_time(task_time)

    new_task_data = {
        "title": task_title,
        "description": task_description,
        "task_date": task_date_formatted,
        "task_time": task_time_formatted,
        "status": "Новая"
    }
    try:
        await task_crud.create(**new_task_data)
        await callback.message.answer(text="Создание задачи подтверждено               \n"
                                      "Для перезапуска нажмите             /start \n"
                                      "Для записи новой задачи нажмите      /task_creation \n"
                                      "Для просмотра существующих задач нажмите    /view_tasks \n")
    except Exception as e:
        print(f"Ошибка создания задачи: {e}")
        await callback.message.answer(f"Ошибка создания задачи: {e}")
    await state.clear()
