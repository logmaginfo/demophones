from aiogram.fsm.state import StatesGroup, State

class UpUser(StatesGroup):
    tg_id = State()
    name = State()
    last_name = State()
    phone = State()
    email = State()
    address = State()
    comment = State()