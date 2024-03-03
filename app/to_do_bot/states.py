from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

state_router = Router()


class StateAdmin(StatesGroup):
    start_menu = State()
    view_tasks = State()
    task_creation_one = State()
    task_creation_two = State()
    task_creation_three = State()
    task_creation_four = State()
    task_creation_five = State()
    task_creation_six = State()
    task_creation_seven = State()
    task_creation_confirmation = State()
    awaiting_task_id_for_completion = State()
    awaiting_task_id_for_deletion = State()


@state_router.message(F.text.casefold() == "к главному меню")
async def process_(message: Message, state: FSMContext) -> None:
    await state.set_state(StateAdmin.start_menu)
    await message.reply(
        "Возвращение в главное меню! \n"
        "Для перезапуска нажмите                 /start \n"
        "Для записи новой задачи нажмите      /task_creation \n"
        "Для просмотра активных задач нажмите    /view_active_tasks \n"
        "Для просмотра всех существующих задач нажмите    /view_tasks \n"
        "Для завершения задачи нажмите /complete_task \n"
        "Для удаления задачи нажмите /delete_task \n"
        )


@state_router.message(F.text.casefold() == "debug:print state")
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)
