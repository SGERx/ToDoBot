import os
from loguru import logger
from dotenv import load_dotenv

BOT_TOKEN = None


def env_loader():
    global BOT_TOKEN
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        if BOT_TOKEN is None:
            raise ValueError("TOKEN не найден в .env файле")
    else:
        logger.error("Не загружен .env")


env_loader()

if __name__ == '__main__':
    logger.info(BOT_TOKEN)
