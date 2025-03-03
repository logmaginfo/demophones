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

class UpBrand(StatesGroup):
    sort = State()
    name = State()
    description = State()

class UpCategory(StatesGroup):
    sort = State()
    name = State()
    photo = State()

class UpColor(StatesGroup):
    name = State()
    photo = State()

# class UpSub(StatesGroup):
#     category_id = State()
#     name = State()
#     sort = State()
#     photo = State()

class UpDelivery(StatesGroup):
    sort = State()
    name = State()
    description = State()
    price = State()

class Del_item(StatesGroup):
    del_item = State()

class UpProduct(StatesGroup):
    sort = State()
    name = State()
    description = State()
    photo = State()

