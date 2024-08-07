from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiohttp import ClientOSError
from aiohttp import ClientSession
from loguru import logger

import config

router = Router()


@router.message(Command(commands=['weather']), StateFilter(None))
async def get_weather(message: Message):
    command = message.text.split(' ', maxsplit=1)
    if len(command) == 1:
        return await message.answer("Напишите ещё город")
    city_name = command[1]
    try:
        """
        curl -X 'GET' \
          'https://api.weatherapi.com/v1/current.json?q=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3&lang=ru&key=29b6196cc227455093774427240708' \
          -H 'accept: application/json'
        """
        async with ClientSession() as session:
            async with session.get(
                        'https://api.weatherapi.com/v1/current.json',
                        params={
                            'q': city_name,
                            'lang': 'ru',
                            'key': config.WEATHER_API_TOKEN
                        }
                    ) as request:
                weather = await request.json()
    except ClientOSError:
        logger.error("Сервер api.weatherapi.com на данный момент недоступен")
        await message.answer("Сервер погоды на данный момент недоступен, попробуйте позже")
    else:
        location = weather.get('location')
        weather = weather.get('current')
        await message.answer(
            text=f"Погода для населённого пункта {location['name']}:\n"
                 f"Температура: {weather.get('temp_c')}℃, ощущается на {weather.get('feelslike_c')}℃\n"
                 f"{weather['condition'].get('text')}\n"
                 f"Скорость ветра: {weather.get('wind_mph')} метров в час"
        )
