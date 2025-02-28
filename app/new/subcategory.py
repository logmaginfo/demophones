from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null

from app.admin import subcategory_menu
from app.cmd.pagination import get_paginated_kb
from app.cmd.paginator import get_paginat_kb
from app.db.models import Category
from app.db.requests import set_subcategory_new, set_subcategory_up, get_subcategory_id, get_category_id
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpBrand, UpSub
import app.keyboards as kb


newsubcategory = Router()
newsubcategory.message.filter(Admin())
# UpSub(StatesGroup):
#     category_id = State()
#     name = State()
@newsubcategory.callback_query(F.data.startswith('add_subcategory'))
async def subcategory_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    category_id = callback.data.split('_')[2]
    await state.update_data(category_id=category_id)
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpSub.sort)
    #####
    data = await state.get_data()
    #####
    await callback.message.answer('Сортировка',
                                  reply_markup=await kb.kb_cancel(f'subcategory_{data['category_id']}'), parse_mode='html')
################################# upsubcategory_
@newsubcategory.callback_query(F.data.startswith('upsubcategory_'))
async def subcategory_up(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpSub.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    subcategory = await get_subcategory_id(id)
    category_name = await get_category_id(subcategory.category_id)
    await state.update_data(category_id=subcategory.category_id)
    await state.update_data(id=subcategory.id)
    #####
    data = await state.get_data()
    #####
    if subcategory.photo != None:
       await callback.message.answer_photo(subcategory.photo)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {subcategory.id})\n'
                                  f'Сортировка: {subcategory.sort}\n'
                                  f'{subcategory.category_id} / {category_name.name}\n'
                                  f'Название: {subcategory.name}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены❗️\nСортировка:</b>',
                                  reply_markup=await kb.kb_cancel(f'subcategory_{data['category_id']}'), parse_mode='html')

################################# cat
# @newsubcategory.callback_query(UpSub.category_id, F.data.startswith('cat_'))
# async def subcategory_new_cat(callback:CallbackQuery, state: FSMContext):
#     await state.set_state(UpSub.sort)
#     id = callback.data.split('_')[1]
#     await state.update_data(category_id=id)
#     await callback.message.edit_text('Сортировка', reply_markup=kb.cancel, parse_mode='html')

################################# sort
@newsubcategory.message(UpSub.sort, F.text)
async def subcategory_new_sort(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<5:
        await state.set_state(UpSub.name)
        await state.update_data(sort=message.text)
        await message.answer('Введите название подкатегории', reply_markup=await kb.kb_cancel(f'subcategory_{data['category_id']}'))
    else:#subcategory_{item.id}
        await message.answer('Сортировка(<5)', reply_markup=await kb.kb_cancel(f'subcategory_{data['category_id']}'))

##################################### name
@newsubcategory.message(UpSub.name, F.text)
async def subcategory_new_name(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<90:
        await state.update_data(name=message.text)
        await state.set_state(UpSub.photo)
        await message.answer('Добавьте изображение',
                             reply_markup=await kb.kb_next(f'subcategory_{data['category_id']}'))

    else:
        data = await state.get_data()
        await message.answer('Введите название подкатегории(<90)',
                             reply_markup=await kb.kb_cancel(f'subcategory_{data['category_id']}'))

################################# photo
@newsubcategory.message(UpSub.photo, F.photo)
async def category_new_photo(message: Message, state: FSMContext):
    id_photo = message.photo[-1].file_id
    await state.update_data(photo=id_photo)
    data = await state.get_data()
    category_id = data['category_id']
    # subcategory = await get_subcategory_id(category_id)
    category_name = await get_category_id(category_id)
    text = 'нет'
    if data['status'] == 'new':
        text = await set_subcategory_new(data)
    if data['status'] == 'up':
        text = await set_subcategory_up(data)
    await message.answer(
        text=f'{kb.name_menu['subcategory_menu']} / {category_name.name}',
        reply_markup=await get_paginat_kb(fun=subcategory_menu, category_id=category_id))
    await state.clear()


@newsubcategory.callback_query(UpSub.photo, F.data == 'next')
async def category_new_photo_null(callback:CallbackQuery, state: FSMContext):
    await state.update_data(photo=null())
    data = await state.get_data()
    category_id = data['category_id']
    # subcategory = await get_subcategory_id(category_id)
    category_name = await get_category_id(category_id)
    text = 'нет'
    if data['status'] == 'new':
        text = await set_subcategory_new(data)
    if data['status'] == 'up':
        text = await set_subcategory_up(data)
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await callback.message.edit_text(
        text=f'{kb.name_menu['subcategory_menu']} / {category_name.name}',
        reply_markup=await get_paginat_kb(fun=subcategory_menu, category_id=category_id))
    await state.clear()