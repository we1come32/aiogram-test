from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

router = Router()


@router.message(Command(commands=['echo']), StateFilter(None))
async def echo(message: Message):
    await message.answer(message.text)
