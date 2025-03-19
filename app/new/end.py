import sqlalchemy
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from app.db.requests import set_user_new, get_user_id, set_user_up
from app.filter import Admin, Private
from aiogram.types import Message, CallbackQuery
from app.states import UpSize
import app.keyboards as kb
import re

endrouter = Router()
endrouter.message.filter(Admin())
endrouter.message.filter(Private())
@endrouter.message()
async def user_new_tg_id_doc(message: Message):
    await message.answer('Некорректно! Введите сообщение', reply_markup=kb.cancel)