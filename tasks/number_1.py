from aiogram import Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message


router = Router()


@router.message(CommandStart(), StateFilter(None))
async def start(message: Message):
    await message.answer("Добро пожаловать в наш бот!")


@router.message(Command(commands=['help']), StateFilter(None))
async def help_handler(message: Message):
    await message.answer("Доступные команды: /start, /help, /echo, /photo")
