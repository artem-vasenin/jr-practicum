from aiogram.fsm.state import State, StatesGroup

class FSMState(StatesGroup):
    wait_for_req = State()

class TalkState(StatesGroup):
    wait_for_answer = State()

class QuizState(StatesGroup):
    quiz = State()