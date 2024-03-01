import asyncio
import sys

from app.to_do_bot.bot_main import main_bot


async def main():
    await main_bot()


if __name__ == "__main__":
    asyncio.run(main())
