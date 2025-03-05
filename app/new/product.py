from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null
from app.admin import product_menu
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_category_id, get_product_id, set_product_new, set_product_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpProduct
import app.keyboards as kb

newproduct = Router()
newproduct.message.filter(Admin())

@newproduct.callback_query(F.data.startswith('add_product'))
async def product_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    category_id = callback.data.split('_')[2]
    await state.update_data(category_id=category_id)
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpProduct.sort)
    #####
    data = await state.get_data()
    #####
    await callback.message.answer('Сортировка:',
                                  reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'),
                                  parse_mode='html')
################################# upproduct_
@newproduct.callback_query(F.data.startswith('upproduct_'))
async def product_up(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpProduct.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    product = await get_product_id(id)
    category = await get_category_id(product.category_id)
    if not category:
        name = kb.name_menu['category_menu']
    else:
        name = category.name
    await state.update_data(category_id=product.category_id)
    await state.update_data(id=id)
    #####
    data = await state.get_data()
    #####
    if product.photo != None:
       await callback.message.answer_photo(product.photo)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {product.id})\n'
                                  f'Сортировка: {product.sort}\n'
                                  f'{product.category_id} / {name}\n'
                                  f'Название: {product.name}\n'
                                  f'Описание: {product.description}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены❗️\nСортировка:</b>',
                                  reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'), parse_mode='html')

################################# sort
@newproduct.message(UpProduct.sort, F.text)
async def product_new_sort(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<5:
        await state.set_state(UpProduct.name)
        await state.update_data(sort=message.text)
        await message.answer('Введите название продукта',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
    else:#category_{item.id}
        await message.answer('Сортировка(<5)',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))

##################################### name
@newproduct.message(UpProduct.name, F.text)
async def product_new_name(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<90:
        await state.update_data(name=message.text)
        await state.set_state(UpProduct.description)
        await message.answer('Добавьте описание продукта (2000 зн)',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
    else:
        data = await state.get_data()
        await message.answer('Введите название продукта(< 90 зн)',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
##################################### description
@newproduct.message(UpProduct.description, F.text)
async def description_new_name(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<2000:
        await state.update_data(description=message.text)
        await state.set_state(UpProduct.photo)
        await message.answer('Добавьте баннер продукта',
                             reply_markup=await kb.kb_next(f'product_{data['category_id']}'))
    else:
        data = await state.get_data()
        await message.answer('Введите описание продукта < 2000 зн',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
################################# photo
@newproduct.message(UpProduct.photo, F.photo)
async def product_new_photo(message: Message, state: FSMContext):
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
        text = await set_product_new(data)
    if data['status'] == 'up':
        text = await set_product_up(data)
    await message.answer(
        text=f'{cat_kb} {name} {text}',
        reply_markup=await get_paginat_kb(fun=product_menu, category_id=category_id))
    await state.clear()


@newproduct.callback_query(UpProduct.photo, F.data == 'next')
async def product_new_photo_null(callback:CallbackQuery, state: FSMContext):
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
        text = await set_product_new(data)
    if data['status'] == 'up':
        text = await set_product_up(data)
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await callback.message.edit_text(
        text=f'{cat_kb} {name} {text}',
        reply_markup=await get_paginat_kb(fun=product_menu, category_id=category_id))
    await state.clear()