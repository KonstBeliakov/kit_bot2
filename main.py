from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType

import asyncio
import logging
import os

from core.google_sheets import update_data, admin_list_id
from core.handlers import basic
from core.handlers.basic import get_started
from core.settings import settings
from aiogram.filters import ContentTypesFilter, Command
from aiogram import F

from core.utils.commands import set_commands
from core.utils.botstates import BotStates

admin_id = []


async def start_bot(bot: Bot):
    await set_commands(bot)
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

    dp.message.register(basic.admin_start_keyboard, BotStates.ADMIN_START)
    dp.message.register(basic.select_lesson, BotStates.LESSON_SELECTION)
    dp.message.register(basic.select_review_type, BotStates.REVIEW_TYPE_SELECTION)
    dp.message.register(basic.try_again, BotStates.TRY_AGAIN)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
