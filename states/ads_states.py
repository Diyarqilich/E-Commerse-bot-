from aiogram.fsm.state import State, StatesGroup

class AdsState(StatesGroup):
    waiting_for_ads = State()