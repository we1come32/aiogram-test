from aiogram import Router, Bot

import config

router = Router()


@router.startup.register
async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}", secret_token=config.WEBHOOK_SECRET)
