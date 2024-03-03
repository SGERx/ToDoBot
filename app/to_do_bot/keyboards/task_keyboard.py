from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

task_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_creation_task', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_creation_task', text="Подтверждаю")

    ]
])

task_creation_return_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_creation', text="Создать еще одну задачу"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_main_menu', text="Вернуться в меню работы с задачами")

    ]
])
