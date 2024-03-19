from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core import google_sheets

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Оставить отзыв'
        ),
    ],
    [
        KeyboardButton(
            text='Обновить данные бота'
        ),
    ],
    [
        KeyboardButton(
            text='Остановить бота'
        ),
    ],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выбери одну из кнопок', selective=True)

review_type_select_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Обычный отзыв'
        ),
        KeyboardButton(
            text='Анонимный отзыв'
        ),
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выбери одну из кнопок', selective=True)

try_again_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Попробовать еще раз'
        ),
        KeyboardButton(
            text='Назад'
        ),
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выбери одну из кнопок', selective=True)


def user_keyboard(username: str):
    t_keyboard = []
    if google_sheets.students.get(username, False):
        for i in range(len(google_sheets.students[username])):
            t_keyboard.append([KeyboardButton(text=google_sheets.students[username][i])])
        return ReplyKeyboardMarkup(keyboard=t_keyboard, resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Выбери одну из кнопок',
                               selective=True
                               )
