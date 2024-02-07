from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.reply import admin_keyboard, user_keyboard
from core.google_sheets import admin_list_id
from core.utils.botstates import BotStates
from core.google_sheets import update_data


async def get_started(message: Message, bot: Bot, state: FSMContext):
    print(message.from_user.username)
    print(admin_list_id)
    if message.from_user.username in admin_list_id:
        await bot.send_message(message.from_user.id, f'Ты в списке администраторов!',
                               reply_markup=admin_keyboard)
        await state.set_state(BotStates.ADMIN_START)
    else:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}',)
                               #reply_markup=user_keyboard(message.from_user.id))
        await state.set_state(BotStates.LESSON_SELECTION)


async def admin_start_keyboard(message: Message, bot: Bot, state: FSMContext):
    match message.text:
        case 'Оставить отзыв':
            await bot.send_message(message.from_user.id, f'Ты можешь оставить отзыв к одному из этих уроков:',
                                   reply_markup=user_keyboard(message.from_user.id))
            await state.set_state(BotStates.LESSON_SELECTION)
        case 'Обновить данные бота':
            await bot.send_message(message.from_user.id, 'Данные будут обновлены в течении нескольких секунд...')
            try:
                await update_data()
            except:
                await bot.send_message(message.from_user.id, 'При обновлении данных произошла ошибка')
            else:
                await bot.send_message(message.from_user.id, 'Данные успешно обновлены')
            await state.set_state(BotStates.DEFAULT)