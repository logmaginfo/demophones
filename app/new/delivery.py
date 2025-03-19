from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from app.admin import delivery_menu
from app.cmd.paginator import get_paginat_kb
from app.db.requests import set_delivery_new, set_delivery_up, get_delivery_id
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpDelivery
import app.keyboards as kb

newdelivery = Router()
newdelivery.message.filter(Admin())

@newdelivery.callback_query(F.data.startswith('add_delivery'))
async def delivery_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpDelivery.sort)
    await callback.message.answer('Сортировка <b>*</b>', reply_markup=await kb.kb_cancel('supply'), parse_mode='html')
################################# upbrand
@newdelivery.callback_query(F.data.startswith('updelivery_'))
async def delivery_up(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpDelivery.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    delivery = await get_delivery_id(id)
    await state.update_data(id=delivery.id)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {delivery.id})\n'
                                  f'Сортировка: {delivery.sort}\n'
                                  f'Название: {delivery.name}\n'
                                  f'Описание: {delivery.description}\n'
                                  f'Прайс: {delivery.price}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены❗️\nСортировка:</b>', reply_markup=kb.cancel, parse_mode='html')


################################# sort
@newdelivery.message(UpDelivery.sort, F.text)
async def delivery_new_sort(message: Message, state: FSMContext):
    if len(message.text)<5:
        await state.set_state(UpDelivery.name)
        await state.update_data(sort=message.text)
        await message.answer('Введите название', reply_markup=await kb.kb_cancel('supply'))
    else:
        await message.answer('Сортировка(<5)', reply_markup=await kb.kb_cancel('supply'))

################################# name
@newdelivery.message(UpDelivery.name, F.text)
async def delivery_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await state.set_state(UpDelivery.price)
        await state.update_data(name=message.text)
        await message.answer('Введите цену', reply_markup=await kb.kb_cancel('supply'))
    else:
        await message.answer('Введите название(<90)', reply_markup=await kb.kb_cancel('supply'))

################################# price
@newdelivery.message(UpDelivery.price, F.text)
async def delivery_new_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.set_state(UpDelivery.description)
        await state.update_data(price=price)
        await message.answer('Введите описание', reply_markup=await kb.kb_cancel('supply'))
    except Exception as e:
        await message.answer('Цена. Формат: "50.5" или "786"', reply_markup=await kb.kb_cancel('supply'))

################################# description
@newdelivery.message(UpDelivery.description, F.text)
async def delivery_new_desc(message: Message, state: FSMContext):
    if len(message.text)<500:
        await state.update_data(description=message.text)
        data = await state.get_data()
        text = 'нет'
        if data['status'] == 'new':
           text = await set_delivery_new(data)
        if data['status'] == 'up':
           text = await set_delivery_up(data)
        await message.answer(f"{kb.name_menu['delivery_menu']} {text}", reply_markup=await get_paginat_kb(fun=delivery_menu))
        await state.clear()
    else:
        await message.answer('Введите описание(<500)', reply_markup=await kb.kb_cancel('supply'))