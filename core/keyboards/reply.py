from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from core.google_sheets import students

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Оставить отзыв'
        ),
        KeyboardButton(
            text='Обновить данные бота'
        ),
    ],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выбери одну из кнопок', selective=True
)


def user_keyboard(user_id: int):
    t_keyboard = []
    if students.get(user_id, False):
        for i in range(len(students[user_id])):
            t_keyboard.append(KeyboardButton(text=students[user_id][i]), )
    else:
        t_keyboard = ['Не получилось найти уроки к которым вы можете оставить отзыв :(']

    return ReplyKeyboardMarkup(keyboard=[t_keyboard], resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Выбери одну из кнопок',
                               selective=True
                               )
