import logging
import asyncio
import os


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


from every_directory.handlers.based_handler import cmd_bassed_router
from every_directory.handlers.myfsm import fsm_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
        logging.basicConfig(
        level=logging.INFO
    )
        storage = MemoryStorage()
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher(storage=storage)
        dp.include_router(fsm_router)
        dp.include_router(cmd_bassed_router)
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

