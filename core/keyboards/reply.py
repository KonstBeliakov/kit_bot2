from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from core.google_sheets import students, nicks

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


def user_keyboard(username: str):
    t_keyboard = []
    if students.get(username, False):
        for i in range(len(students[username])):
            t_keyboard.append(KeyboardButton(text=students[username][i]))
    else:
        print(students.get(username, True), students.items(), sep='\n')
        print(nicks, nicks.get(username, True))
        t_keyboard = [KeyboardButton(text='Уроки не найдены')]

    return ReplyKeyboardMarkup(keyboard=[t_keyboard], resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Выбери одну из кнопок',
                               selective=True
                               )
