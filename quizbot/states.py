from aiogram.fsm.state import StatesGroup, State

class QuizForm(StatesGroup):
    question = State()
    option_a = State()
    option_b = State()
    option_c = State()
    option_d = State()
    correct = State()