from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


router = Router()


@router.message(Command(commands=['try_callback']), StateFilter(None))
async def try_callback(message: Message):
    await message.answer(
        "Какие-то кнопки",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Выбор 1", callback_data="choice_1")],
            [InlineKeyboardButton(text="Выбор 2", callback_data="choice_2")],
        ]))


@router.callback_query(F.data.startswith('choice_'), StateFilter(None))
async def choice_event(event: CallbackQuery):
    await event.message.answer(
        text="Вы выбрали Выбор {number}".format(number=event.data[-1])
    )
