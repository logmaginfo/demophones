from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from app.admin import sizes_menu
from app.cmd.paginator import get_paginat_kb
from app.db.requests import set_size_new, get_size_id, set_size_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpSize
import app.keyboards as kb


newsize = Router()
newsize.message.filter(Admin())

@newsize.callback_query(F.data.startswith('add_sizes'))
async def sizes_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpSize.name)
    await callback.message.answer('Введите название размера <b>*</b>', reply_markup=await kb.kb_cancel('sizes_menu'), parse_mode='html')

################################# upsizes
@newsize.callback_query(F.data.startswith('upsizes_'))
async def sizes_up(callback:CallbackQuery, state: FSMContext):
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
                                  'Старые будут удалены❗️\nВведите название размера</b>', reply_markup=await kb.kb_cancel('sizes_menu'), parse_mode='html')



################################# name
@newsize.message(UpSize.name, F.text)
async def size_new_name(message: Message, state: FSMContext):
    if len(message.text)<28:
        await state.set_state(UpSize.description)
        await state.update_data(name=message.text)
        await message.answer('Введите описание размера', reply_markup=await kb.kb_cancel('sizes_menu'))
    else:
        await message.answer('Введите название размера(<28)', reply_markup=await kb.kb_cancel('sizes_menu'))

################################# description
@newsize.message(UpSize.description, F.text)
async def size_new_desc(message: Message, state: FSMContext):
    if len(message.text)<500:
        await state.update_data(description=message.text)
        data = await state.get_data()
        text = 'нет'
        if data['status'] == 'new':
           text = await set_size_new(data)
        if data['status'] == 'up':
           text = await set_size_up(data)
        # await message.answer(text, reply_markup=await get_paginated_kb(pages=10, switch=data["switch"]))
        await message.answer(f'{kb.name_menu['sizes_menu']} {text}', reply_markup=await get_paginat_kb(fun=sizes_menu))
        await state.clear()

    else:
        await message.answer('Введите описание размера(<500)', reply_markup=await kb.kb_cancel('sizes_menu'))

        #await state.clear()