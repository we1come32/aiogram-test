from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message


class Steps(StatesGroup):
    input_name = State()
    input_age = State()


router = Router()


@router.message(Command(commands=['register']), StateFilter(None))
async def register_main(message: Message, state: FSMContext):
    await message.answer("Введите Ваше имя:")
    await state.set_state(Steps.input_name)
    await state.set_data({})


@router.message(StateFilter(Steps.input_name))
async def register_get_name(message: Message, state: FSMContext):
    await message.answer(f"Хорошо, буду звать вас {message.text}\nТеперь введите Ваш возраст, пожалуйста:")
    await state.set_state(Steps.input_age)
    await state.update_data(name=message.text)


@router.message(StateFilter(Steps.input_age))
async def register_get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Я вас не понимаю. Введите возраст числом")
    user_data = await state.get_data()
    user_data['age'] = message.text
    await message.answer(f"Приятно с Вами познакомиться. Теперь я знаю, "
                         f"что Вас зовут {user_data['name']} и вам {user_data['age']} лет")
    await state.clear()
