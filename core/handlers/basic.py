from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.reply import admin_keyboard, user_keyboard, review_type_select_keyboard, try_again_keyboard
from core.google_sheets import admin_list_id, nicks
from core.utils.botstates import BotStates, selected_lesson, selected_review_type
from core.google_sheets import update_data, write_review


async def update_bot(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Данные будут обновлены в течении нескольких секунд...')
    try:
        update_data()
    except Exception as err:
        await bot.send_message(message.from_user.id, f'При обновлении данных произошла ошибка: {err}',
                               reply_markup=try_again_keyboard)
        await state.set_state(BotStates.TRY_AGAIN)
    else:
        await bot.send_message(message.from_user.id, 'Данные успешно обновлены')
        await state.set_state(BotStates.DEFAULT)


async def get_started(message: Message, bot: Bot, state: FSMContext):
    if message.from_user.username in admin_list_id:
        await bot.send_message(message.from_user.id, f'Ты в списке администраторов! Тебе доступна возможность '
                                                     f'обновления данных бота', reply_markup=admin_keyboard)
        await state.set_state(BotStates.ADMIN_START)
    else:
        await keyboard_sellect_lesson(message, bot, state)


async def keyboard_sellect_lesson(message: Message, bot: Bot, state: FSMContext):
    if user_keyboard(message.from_user.username):
        await bot.send_message(message.from_user.id, f'Выбери урок к которому хочешь оставить отзыв:',
                               reply_markup=user_keyboard(message.from_user.username))
        await state.set_state(BotStates.LESSON_SELECTION)
    else:
        await bot.send_message(message.from_user.id, f'Не смогли найти тебя в списке учеников :(. Попроси администратора добавить тебя в базу данных и обновить данные бота.',
                               reply_markup=user_keyboard(message.from_user.username))
        await state.set_state(BotStates.DEFAULT)


async def admin_start_keyboard(message: Message, bot: Bot, state: FSMContext):
    match message.text:
        case 'Оставить отзыв':
            await keyboard_sellect_lesson(message, bot, state)
        case 'Обновить данные бота':
            await update_bot(message, bot, state)


async def select_lesson(message: Message, bot: Bot, state: FSMContext):
    global selected_lesson
    selected_lesson[message.from_user.username] = message.text
    await bot.send_message(message.from_user.id, f'Теперь выбери тип отзыва для урока {message.text}',
                           reply_markup=review_type_select_keyboard)

    await state.set_state(BotStates.REVIEW_TYPE_SELECTION)


async def select_review_type(message: Message, bot: Bot, state: FSMContext):
    global selected_review_type
    selected_review_type[message.from_user.username] = message.text
    await bot.send_message(message.from_user.id,
                           f'Теперь можешь написать {"анонимный " if message.text == "Анонимный отзыв" else ""}отзыв '
                           f'к уроку {selected_lesson[message.from_user.username]}')
    await state.set_state(BotStates.WAITING_REVIEW)


async def wait_review(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Сохраняем отзыв...')
    try:
        write_review(message.from_user.username, selected_lesson[message.from_user.username],
                     selected_review_type == 'Анонимный отзыв', message.text)
    except Exception as err:
        await bot.send_message(message.from_user.id, f'При сохранении отзыва произошла ошибка: {err}')
    else:
        await bot.send_message(message.from_user.id, f'Отзыв сохранен успешно')
    await state.set_state(BotStates.DEFAULT)


async def try_again(message: Message, bot: Bot, state: FSMContext):
    if message.text == 'Попробовать еще раз':
        await update_bot(message, bot, state)
    else:
        await bot.send_message(message.from_user.id, f'Ты в списке администраторов! Тебе доступна возможность '
                                                     f'обновления данных бота', reply_markup=admin_keyboard)
        await state.set_state(BotStates.ADMIN_START)
