from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command



cmd_bassed_router = Router()


@cmd_bassed_router.message(Command('start'))
async def start_cmd(message: Message):
    await message.answer(f'Здраствуй {message.chat.username}! Это бот для отслеживания финансов и учетов')


@cmd_bassed_router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer(f'Команды:\n /addexpence\n /report\n /categories')

