from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null

from app.admin import category_menu
from app.cmd.pagination import get_paginated_kb
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_category_id, set_category_new, set_category_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpCategory
import app.keyboards as kb
import re

newcategory = Router()
newcategory.message.filter(Admin())

@newcategory.callback_query(F.data.startswith('add_category'))
async def category_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpCategory.sort)
    await callback.message.answer('Сортировка', reply_markup=await kb.kb_cancel('category_menu'), parse_mode='html')

################################# upbrand
@newcategory.callback_query(F.data.startswith('upcategory_'))
async def category_up(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpCategory.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    category = await get_category_id(id)
    if category.photo != None:
       await callback.message.answer_photo(category.photo)
    await state.update_data(id=category.id)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {category.id = })\n'
                                  f'{category.name = }', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены❗️\nСортировка:</b>', reply_markup=await kb.kb_cancel('category_menu'), parse_mode='html')

################################# sort
@newcategory.message(UpCategory.sort, F.text)
async def brand_new_name(message: Message, state: FSMContext):
    if len(message.text)<5:
        await state.set_state(UpCategory.name)
        await state.update_data(sort=message.text)
        await message.answer('Введите название категории', reply_markup=await kb.kb_cancel('category_menu'))
    else:
        await message.answer('Сортировка(<5)', reply_markup=await kb.kb_cancel('category_menu'))
################################# name
@newcategory.message(UpCategory.name, F.text)
async def category_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await state.update_data(name=message.text)
        await state.set_state(UpCategory.photo)
        await message.answer('Добавьте изображение', reply_markup=await kb.kb_next('category_menu'))
    else:
        await message.answer('Введите название(<90)', reply_markup=await kb.kb_cancel('category_menu'))

################################# photo
@newcategory.message(UpCategory.photo, F.photo)
async def category_new_photo(message: Message, state: FSMContext):
    id_photo = message.photo[-1].file_id
    await state.update_data(photo=id_photo)
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_category_new(data)
    if data['status'] == 'up':
        text = await set_category_up(data)
    await message.answer(f"{kb.name_menu['category_menu']} {text}", reply_markup=await get_paginat_kb(fun=category_menu))
    await state.clear()

@newcategory.callback_query(UpCategory.photo, F.data == 'next')
async def category_new_photo_null(callback:CallbackQuery, state: FSMContext):
    await state.update_data(photo=null())
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_category_new(data)
    if data['status'] == 'up':
        text = await set_category_up(data)
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await callback.message.edit_text(f"{kb.name_menu['category_menu']} {text}", reply_markup=await get_paginat_kb(fun=category_menu))
    await state.clear()