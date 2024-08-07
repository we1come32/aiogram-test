import asyncio

import aioschedule
from aiogram import Router, Bot
from sqlmodel import select, Session
from loguru import logger

import config
from tasks.number_6 import User, engine

router = Router()


async def notifier():
    bot = Bot(config.BOT_TOKEN)
    logger.info("Запущен процесс отправки уведомлений")
    with Session(engine) as ss:
        users = ss.exec(select(User)).all()
        for user in users:
            await bot.send_message(
                chat_id=user.id,
                text='Не забудьте проверить уведомления!'
            )
    await bot.session.close()
    logger.success("Процесс отправки уведомлений успешно завершился!")


async def scheduler():
    aioschedule.every().day.at("9:00").do(notifier)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


@router.startup.register
async def on_startup(bot: Bot):
    asyncio.create_task(scheduler())
