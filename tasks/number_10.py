from aiogram import Router
from aiogram.types import ErrorEvent, Message
from aiogram.filters import Command


router = Router()


@router.message(Command(commands=['error']))
async def error_runner(message: Message):
    raise ZeroDivisionError


@router.error()
async def error_handler(event: ErrorEvent):
    text = "Произошла ошибка, попробуйте позже"
    if event.update.message:
        await event.update.message.answer(text)
    elif event.update.callback_query:
        await event.update.callback_query.message.answer(text)
