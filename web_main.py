import importlib

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
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
            module = importlib.import_module(f'tasks.number_{i}')
            dp.include_router(module.router)
            logger.info("Imported tasks.number_{number}", number=i)
    except ImportError:
        pass

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)
