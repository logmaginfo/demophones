import sqlalchemy
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from app.db.requests import set_user_new, get_user_id, set_user_up, set_size_new, get_size_id, set_size_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpSize
import app.keyboards as kb
import re

newsize = Router()
newsize.message.filter(Admin())

@newsize.callback_query(F.data.startswith('add_sizes'))
async def user_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpSize.name)
    await callback.message.answer('Введите название размера <b>*</b>', reply_markup=kb.cancel, parse_mode='html')

################################# upsizes
@newsize.callback_query(F.data.startswith('upsizes_'))
async def user_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpSize.name)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    size = await get_size_id(id)
    await state.update_data(id=size.id)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {size.id = })\n'
                                  f'{size.name = }\n'
                                  f'{size.description=}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены!</b>\nВведите название размера', reply_markup=kb.cancel, parse_mode='html')



################################# name
@newsize.message(UpSize.name, F.text)
async def user_new_name(message: Message, state: FSMContext):
    if len(message.text)<28:
        await state.set_state(UpSize.description)
        await state.update_data(name=message.text)
        await message.answer('Введите описание размера', reply_markup=kb.cancel)
    else:
        await message.answer('Введите название размера(<28)', reply_markup=kb.cancel)

################################# description
@newsize.message(UpSize.description, F.text)
async def user_new_name(message: Message, state: FSMContext):
    if len(message.text)<500:
        await state.update_data(description=message.text)
        data = await state.get_data()
        text = 'нет'
        if data['status'] == 'new':
           text = await set_size_new(data)
        if data['status'] == 'up':
           text = await set_size_up(data)
        await message.answer(text, reply_markup=kb.main)
        await state.clear()

    else:
        await message.answer('Введите описание размера(<500)', reply_markup=kb.cancel)

        #await state.clear()