from aiogram.fsm.state import State, StatesGroup

class FSMState(StatesGroup):
    wait_for_req = State()