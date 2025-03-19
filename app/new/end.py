from aiogram import Router, F
from app.filter import Admin, Private
from aiogram.types import Message

import app.keyboards as kb

endrouter = Router()
endrouter.message.filter(Admin())
endrouter.message.filter(Private())
@endrouter.message()
async def user_new_tg_id_doc(message: Message):
    await message.answer('Некорректно! Введите сообщение', reply_markup=kb.cancel)