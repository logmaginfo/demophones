from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from app.cmd.pagination import get_paginated_kb
from app.db.requests import set_delivery_new, set_delivery_up, get_delivery_id, get_product_id, set_product_new, \
    set_product_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpBrand, UpDelivery, UpProduct
import app.keyboards as kb
from sqlalchemy import null
newproduct = Router()
newproduct.message.filter(Admin())
#add_{switch}_{subcat}_{catprod}_{subcatprod}
@newproduct.callback_query(F.data.startswith('add_product'))
async def product_new(callback:CallbackQuery, state: FSMContext):

    switch = callback.data.split('_')[1]
    subcat = callback.data.split('_')[2]
    catprod = callback.data.split('_')[3]
    subcatprod = callback.data.split('_')[4]
    print(f"\n----------------->>>{subcat}<<<--------------------\n")
    await state.set_state(UpProduct.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.update_data(catprod=catprod)
    await state.update_data(subcatprod=subcatprod)
    await state.update_data(subcat=subcat)

    await callback.message.answer('Сортировка <b>*</b>', reply_markup=kb.cancel, parse_mode='html')

################################# upproduct upproduct_{switch}_{item.id}_{catprod}_{subcatprod}
@newproduct.callback_query(F.data.startswith('upproduct_'))
async def product_up(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    catprod = callback.data.split('_')[3]
    subcatprod = callback.data.split('_')[4]

    await state.set_state(UpProduct.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    await state.update_data(catprod=catprod)
    await state.update_data(subcatprod=subcatprod)
    product = await get_product_id(id)
    await state.update_data(id=product.id)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'{product.sort} (🆔 {product.id = })\n'
                                  f'Назвагние: {product.name}\n'
                                  f'Описание: {product.description}\n'
                                  f'Бренд: {product.brand_id}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены!</b>\nСортировка', reply_markup=kb.cancel, parse_mode='html')

################################# sort
@newproduct.message(UpProduct.sort, F.text)
async def product_new_sort(message: Message, state: FSMContext):
    if len(message.text)<5:
        await state.set_state(UpProduct.name)
        await state.update_data(sort=message.text)
        await message.answer('Введите название', reply_markup=kb.cancel)
    else:
        await message.answer('Сортировка(<5)', reply_markup=kb.cancel)

################################# name
@newproduct.message(UpProduct.name, F.text)
async def product_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await state.set_state(UpProduct.description)
        await state.update_data(name=message.text)
        await message.answer('Введите описание', reply_markup=kb.cancel)
    else:
        await message.answer('Введите название(<90)', reply_markup=kb.cancel)

################################# description
@newproduct.message(UpProduct.description, F.text)
async def product_new_desc(message: Message, state: FSMContext):
    if len(message.text)<500:
        await state.update_data(description=message.text)
        await state.set_state(UpProduct.brand_id)
        await message.answer('Выберите бренд', reply_markup=await kb.kbbrand())
    else:
        await message.answer('Введите описание(<500)', reply_markup=kb.cancel)
################################# brand_id   plusbrand_

@newproduct.callback_query(UpProduct.brand_id, F.data.startswith('plusbrand_'))
async def product_brand_id(callback:CallbackQuery, state: FSMContext):
    brand_id = callback.data.split('_')[1]
    await state.update_data(brand_id=brand_id)
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_product_new(data)
    if data['status'] == 'up':
        text = await set_product_up(data)

    await state.clear()
    await callback.message.answer(text,
    reply_markup = await get_paginated_kb(pages=10, switch="product", subcat=int(data['subcat']), catprod=int(data['catprod']),
                                          subcatprod=int(data['subcatprod'])))
@newproduct.callback_query(UpProduct.brand_id, F.data == 'next')
async def product_brand_id(callback:CallbackQuery, state: FSMContext):
    await state.update_data(brand_id=0)
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_product_new(data)
    if data['status'] == 'up':
        text = await set_product_up(data)

    await state.clear()
    await callback.message.answer(text,
    reply_markup = await get_paginated_kb(pages=10, switch="product", subcat=0, catprod=int(data['catprod']),
                                          subcatprod=int(data['subcatprod'])))