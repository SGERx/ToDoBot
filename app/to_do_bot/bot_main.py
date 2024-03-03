import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.to_do_bot.env_loader import BOT_TOKEN
from app.to_do_bot.handlers.handlers_task_creation import task_router

from .commands import command_router, keyboard_router

logger_to_do_bot = logging.getLogger(__name__)


async def main_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger_to_do_bot.info("Starting to_do_bot")
    to_do_bot = Bot(token=BOT_TOKEN)
    admin_storage = MemoryStorage()
    admin_dp = Dispatcher(storage=admin_storage)
    admin_dp.include_router(command_router)
    admin_dp.include_router(task_router)
    admin_dp.include_router(keyboard_router)

    await to_do_bot.delete_webhook(drop_pending_updates=True)
    await admin_dp.start_polling(to_do_bot)
