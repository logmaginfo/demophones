from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null

from app.admin import category_menu
from app.cmd.paginator import get_paginat_kb
from app.db.models import Category
from app.db.requests import set_category_new, set_category_up, get_category_id, get_category_id
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpCategory
import app.keyboards as kb


newcategory = Router()
newcategory.message.filter(Admin())

@newcategory.callback_query(F.data.startswith('add_category'))
async def category_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    category_id = callback.data.split('_')[2]
    await state.update_data(category_id=category_id)
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpCategory.sort)
    #####
    data = await state.get_data()
    #####
    await callback.message.answer('Сортировка:',
                                  reply_markup=await kb.kb_cancel(f'category_{data['category_id']}'),
                                  parse_mode='html')
################################# upcategory_
@newcategory.callback_query(F.data.startswith('upcategory_'))
async def category_up(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpCategory.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    category = await get_category_id(id)
    main_category = await get_category_id(category.category_id)
    await state.update_data(category_id=category.category_id)
    await state.update_data(id=id)
    #####
    data = await state.get_data()
    #####
    if category.photo != None:
       await callback.message.answer_photo(category.photo)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {category.id})\n'
                                  f'Сортировка: {category.sort}\n'
                                  f'{category.category_id} / {category.name}\n'
                                  f'Название: {category.name}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены❗️\nСортировка:</b>',
                                  reply_markup=await kb.kb_cancel(f'category_{data['category_id']}'), parse_mode='html')

################################# cat
# @newcategory.callback_query(Up.category_id, F.data.startswith('cat_'))
# async def category_new_cat(callback:CallbackQuery, state: FSMContext):
#     await state.set_state(Up.sort)
#     id = callback.data.split('_')[1]
#     await state.update_data(category_id=id)
#     await callback.message.edit_text('Сортировка', reply_markup=kb.cancel, parse_mode='html')

################################# sort
@newcategory.message(UpCategory.sort, F.text)
async def category_new_sort(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<5:
        await state.set_state(UpCategory.name)
        await state.update_data(sort=message.text)
        await message.answer('Введите название категории',
                             reply_markup=await kb.kb_cancel(f'category_{data['category_id']}'))
    else:#category_{item.id}
        await message.answer('Сортировка(<5)',
                             reply_markup=await kb.kb_cancel(f'category_{data['category_id']}'))

##################################### name
@newcategory.message(UpCategory.name, F.text)
async def category_new_name(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<90:
        await state.update_data(name=message.text)
        await state.set_state(UpCategory.photo)
        await message.answer('Добавьте изображение',
                             reply_markup=await kb.kb_next(f'category_{data['category_id']}'))

    else:
        data = await state.get_data()
        await message.answer('Введите название категории(<90)',
                             reply_markup=await kb.kb_cancel(f'category_{data['category_id']}'))

################################# photo
@newcategory.message(UpCategory.photo, F.photo)
async def category_new_photo(message: Message, state: FSMContext):
    id_photo = message.photo[-1].file_id
    await state.update_data(photo=id_photo)
    data = await state.get_data()
    category_id = data['category_id']
    name = ''
    cat_kb = f"{kb.name_menu['category_menu']}"
    if int(category_id)!=0:
        main_category = await get_category_id(category_id)
        name = main_category.name
        cat_kb = f"{kb.name_menu['subcategory_menu']} /"
    text = 'нет'
    if data['status'] == 'new':
        text = await set_category_new(data)
    if data['status'] == 'up':
        text = await set_category_up(data)
    await message.answer(
        text=f'{cat_kb} {name}',
        reply_markup=await get_paginat_kb(fun=category_menu, category_id=category_id))
    await state.clear()


@newcategory.callback_query(UpCategory.photo, F.data == 'next')
async def category_new_photo_null(callback:CallbackQuery, state: FSMContext):
    await state.update_data(photo=null())
    data = await state.get_data()
    category_id = data['category_id']
    name = ''
    cat_kb = f"{kb.name_menu['category_menu']}"
    if int(category_id) != 0:
        main_category = await get_category_id(category_id)
        name = main_category.name
        cat_kb = f"{kb.name_menu['subcategory_menu']} /"
    text = 'нет'
    if data['status'] == 'new':
        text = await set_category_new(data)
    if data['status'] == 'up':
        text = await set_category_up(data)
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await callback.message.edit_text(
        text=f'{cat_kb} {name}',
        reply_markup=await get_paginat_kb(fun=category_menu, category_id=category_id))
    await state.clear()