from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null

from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpUser
import app.keyboards as kb

newuser = Router()
newuser.message.filter(Admin())
@newuser.callback_query(F.data.startswith('add_'))
async def user_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.set_state(UpUser.tg_id)
    await callback.message.answer('Введите id Telegram <b>*</b>', reply_markup=kb.cancel, parse_mode='html')

@newuser.message(UpUser.tg_id, F.text)
async def user_new_tg_id(message: Message, state: FSMContext):
    if message.text.isnumeric():
        await state.set_state(UpUser.name)
        await state.update_data(tg_id=message.text)
        await message.answer('Введите Имя', reply_markup=kb.next)
    else:
        await message.answer('Введите id Telegram - число <b>*</b>', reply_markup=kb.cancel, parse_mode='html')

@newuser.message(UpUser.name, F.text)
async def user_new_name(message: Message, state: FSMContext):
    await state.set_state(UpUser.last_name)
    await state.update_data(name=message.text)
    await message.answer('Введите Фамилию', reply_markup=kb.cancel)

@newuser.message(UpUser.name)
@newuser.callback_query(F.data == 'next')
async def user_new_name_null(callback:CallbackQuery, state: FSMContext):
    await state.set_state(UpUser.last_name)
    await state.update_data(name='')
    await callback.message.answer('Введите Фамилию', reply_markup=kb.next)

@newuser.message(UpUser.last_name, F.text)
async def user_new_name(message: Message, state: FSMContext):
    await state.set_state(UpUser.phone)
    await state.update_data(last_name=message.text)
    data = await state.get_data()
    await message.answer(f'Введите № телефона. Формат: +71111111111 или 81111111111', reply_markup=kb.next)

@newuser.message(UpUser.last_name)
@newuser.callback_query(F.data == 'next')
async def user_new_name_null(callback:CallbackQuery, state: FSMContext):
    await state.set_state(UpUser.phone)
    await state.update_data(last_name='')
    await callback.message.answer('Введите № телефона. Формат: +71111111111 или 81111111111', reply_markup=kb.next)

