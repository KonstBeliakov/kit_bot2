from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.reply import admin_keyboard, user_keyboard, review_type_select_keyboard, try_again_keyboard
from core.google_sheets import admin_list_id
from core.utils.botstates import BotStates
from core.google_sheets import update_data, write_review

selected_lesson = {}
selected_review_type = {}


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
    await start_text(message, bot, state)


async def start_text(message: Message, bot: Bot, state: FSMContext):
    if message.from_user.username in admin_list_id:
        await bot.send_message(message.from_user.id, f'Ты в списке администраторов! Тебе доступна возможность '
                                                     f'обновления данных бота и остановки бота', reply_markup=admin_keyboard)
        await state.set_state(BotStates.ADMIN_START)
    else:
        await keyboard_sellect_lesson(message, bot, state)


async def keyboard_sellect_lesson(message: Message, bot: Bot, state: FSMContext):
    if user_keyboard(message.from_user.username):
        await bot.send_message(message.from_user.id, f'Выбери урок к которому хочешь оставить отзыв',
                               reply_markup=user_keyboard(message.from_user.username))
        await state.set_state(BotStates.LESSON_SELECTION)
    else:
        await bot.send_message(message.from_user.id,
                               f'Не смогли найти тебя в списке учеников :( Попроси администратора добавить тебя'
                               f' в базу данных и обновить данные бота.',
                               reply_markup=user_keyboard(message.from_user.username))
        await state.set_state(BotStates.DEFAULT)


async def admin_start_keyboard(message: Message, bot: Bot, state: FSMContext):
    match message.text:
        case 'Оставить отзыв':
            await keyboard_sellect_lesson(message, bot, state)
        case 'Обновить данные бота':
            await update_bot(message, bot, state)
        case 'Остановить бота':
            exit()
        case _:
            await bot.send_message(message.from_user.id, f'Не получилось найти команду "{message.text}".'
                                                         f' Пожалуйста выбери одну из доступных комманд',
                                   reply_markup=admin_keyboard)
            await state.set_state(BotStates.ADMIN_START)


async def select_lesson(message: Message, bot: Bot, state: FSMContext):
    global selected_lesson
    print([(button[0], type(button[0])) for button in user_keyboard(message.from_user.username).keyboard])
    if message.text in [button[0].text for button in user_keyboard(message.from_user.username).keyboard]:
        selected_lesson[message.from_user.username] = message.text
        await bot.send_message(message.from_user.id, f'Теперь выбери тип отзыва для урока {message.text}',
                               reply_markup=review_type_select_keyboard)
        await state.set_state(BotStates.REVIEW_TYPE_SELECTION)
    else:
        await bot.send_message(message.from_user.id,
                               f'Урок "{message.text}" не проводится в твоем классе. Пожалуйста выбери один из доступных',
                               reply_markup=user_keyboard(message.from_user.username))
        await state.set_state(BotStates.LESSON_SELECTION)


async def select_review_type(message: Message, bot: Bot, state: FSMContext):
    global selected_review_type
    if message.text in ['Анонимный отзыв', 'Обычный отзыв']:
        selected_review_type[message.from_user.username] = message.text
        await bot.send_message(message.from_user.id,
                               f'Теперь можешь написать {"анонимный " if message.text == "Анонимный отзыв" else ""}отзыв '
                               f'к уроку {selected_lesson[message.from_user.username]}')
        await state.set_state(BotStates.WAITING_REVIEW)
    else:
        await bot.send_message(message.from_user.id, f'Не получилось найти тип отзыва "{message.text}". '
                                                     f'Пожалуйста выбери один из доступных типов',
                               reply_markup=review_type_select_keyboard)
        await state.set_state(BotStates.REVIEW_TYPE_SELECTION)


async def wait_review(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Сохраняем отзыв...')
    try:
        write_review(username=message.from_user.username, lesson=selected_lesson[message.from_user.username],
                     anonimous=selected_review_type[message.from_user.username] == 'Анонимный отзыв',
                     review_text=message.text)
    except Exception as err:
        await bot.send_message(message.from_user.id, f'При сохранении отзыва произошла ошибка: {err}')
    else:
        await bot.send_message(message.from_user.id, f'Отзыв сохранен успешно')
    finally:
        await start_text(message, bot, state)


async def try_again(message: Message, bot: Bot, state: FSMContext):
    match message.text:
        case 'Попробовать еще раз':
            await update_bot(message, bot, state)
        case 'Назад':
            await bot.send_message(message.from_user.id, f'Ты в списке администраторов! Тебе доступна возможность '
                                                         f'обновления данных бота', reply_markup=admin_keyboard)
            await state.set_state(BotStates.ADMIN_START)
        case _:
            await bot.send_message(message.from_user.id, 'Пожалуйста выбери одну из кнопок:',
                                   reply_markup=try_again_keyboard)
            await state.set_state(BotStates.TRY_AGAIN)
