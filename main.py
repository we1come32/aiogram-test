import importlib

from aiogram import Dispatcher, Bot
from loguru import logger

import config

if config.CACHE_STORAGE:
    from aiogram.fsm.storage.redis import RedisStorage
    storage = RedisStorage(config.CACHE_STORAGE)
else:
    from aiogram.fsm.storage.memory import MemoryStorage
    storage = MemoryStorage()

dp = Dispatcher(storage=storage)


if __name__ == '__main__':
    bot = Bot(config.BOT_TOKEN)
    try:
        for i in range(1, 100):
            if i == 8:
                continue
            module = importlib.import_module(f'tasks.number_{i}')
            dp.include_router(module.router)
            logger.info("Imported tasks.number_{number}", number=i)
    except ImportError:
        pass
    dp.run_polling(bot)
