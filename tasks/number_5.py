from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


router = Router()


@router.message(F.photo)
async def get_image_size(message: Message):
    photo = message.photo[-1]
    await message.answer(f"Размер изображения: {photo.width}x{photo.height}")
