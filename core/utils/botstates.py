from aiogram.fsm.state import StatesGroup, State


selected_lesson = {}
selected_review_type = {}


class BotStates(StatesGroup):
    ADMIN_START = State()
    LESSON_SELECTION = State()
    DEFAULT = State()
    REVIEW_TYPE_SELECTION = State()
    WAITING_REVIEW = State()
    TRY_AGAIN = State()