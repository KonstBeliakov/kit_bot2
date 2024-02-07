from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    ADMIN_START = State()
    LESSON_SELECTION = State()
    DEFAULT = State()