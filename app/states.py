from aiogram.fsm.state import StatesGroup, State

class UpUser(StatesGroup):
    tg_id = State()
    name = State()
    last_name = State()
    phone = State()
    email = State()
    address = State()
    comment = State()

class UpSize(StatesGroup):
    name = State()
    description = State()

class UpColor(StatesGroup):
    name = State()
    photo = State()


class Del_item(StatesGroup):
    del_item = State()