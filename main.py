from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType

import asyncio
import logging
import os

from core.handlers.basic import get_started
from core.settings import settings
from aiogram.filters import ContentTypesFilter, Command
from aiogram import F

admin_id = []


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s -'
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')

    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()
    dp.message.register(get_started, Command(commands=['start', 'run']))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
