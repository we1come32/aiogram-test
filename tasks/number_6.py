from sqlmodel import select, Session, SQLModel, create_engine
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import config


engine = create_engine(config.DATABASE)


class User(SQLModel, table=True):
    id: int
    name: str
    age: int


class Steps(StatesGroup):
    reg_input_name = State()
    reg_input_age = State()


router = Router()


@router.message(Command(commands=['reg']), StateFilter(None))
async def register_main(message: Message, state: FSMContext):
    with Session(engine) as ss:
        user = ss.exec(select(User).where(User.id == message.from_user.id)).first()
        if user:
            await message.answer("Вы уже зарегистрированы")
            return
    await message.answer("Введите Ваше имя:")
    await state.set_state(Steps.reg_input_name)
    await state.set_data({})


@router.message(StateFilter(Steps.reg_input_name))
async def register_get_name(message: Message, state: FSMContext):
    await message.answer(f"Хорошо, буду звать вас {message.text}\nТеперь введите Ваш возраст, пожалуйста:")
    await state.set_state(Steps.reg_input_age)
    await state.update_data(name=message.text)


@router.message(StateFilter(Steps.reg_input_age))
async def register_get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Я вас не понимаю. Введите возраст числом")
    user_data = await state.get_data()
    user_data['age'] = message.text
    await message.answer(f"Приятно с Вами познакомиться. Теперь я знаю, "
                         f"что Вас зовут {user_data['name']} и вам {user_data['age']} лет")
    await state.clear()
    with Session(engine) as session:
        user = User(
            id=message.from_user.id,
            **user_data  # name and age keys
        )
        session.add(user)
        session.commit()


@router.message(Command(commands=['users']))
async def users_list(message: Message):
    with Session(engine) as ss:
        users = ss.exec(select(User).order_by(User.id)).all()
    msg = "Список пользователей:\n"
    for user in users:
        line = f"\n{user.id}) {user.name} ({user.age} лет)"
        if len(msg) + len(line) > 4000:
            await message.answer(msg)
            msg = ""
        msg += line
    if msg:
        await message.answer(msg)
