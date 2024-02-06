from aiogram import Bot
from aiogram.types import Message

from core.keyboards.reply import admin_keyboard, user_keyboard
from core.google_sheets import admin_list_id


async def get_started(message: Message, bot: Bot):
    if message.from_user.id in admin_list_id:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}',
                               reply_markup=admin_keyboard)
    else:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}',
                               reply_markup=user_keyboard(message.from_user.id))
