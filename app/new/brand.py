from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from app.admin import brand_menu
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_brand_id, set_brand_new, set_brand_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpBrand
import app.keyboards as kb


newbrand = Router()
newbrand.message.filter(Admin())

@newbrand.callback_query(F.data.startswith('add_brand'))
async def brand_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpBrand.sort)
    await callback.message.answer('Сортировка', reply_markup=await kb.kb_cancel('brand'), parse_mode='html')

################################# upbrand
@newbrand.callback_query(F.data.startswith('upbrand_'))
async def brand_up(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpBrand.sort)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    brand = await get_brand_id(id)
    await state.update_data(id=brand.id)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {brand.id})\n'
                                  f'Сортировка: {brand.sort}\n'
                                  f'Название: {brand.name}\n'
                                  f'Описание: {brand.description}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены❗️\nСортировка:</b>', reply_markup=await kb.kb_cancel('brand'), parse_mode='html')


################################# sort
@newbrand.message(UpBrand.sort, F.text)
async def brand_new_sort(message: Message, state: FSMContext):
    if len(message.text)<5:
        await state.set_state(UpBrand.name)
        await state.update_data(sort=message.text)
        await message.answer('Введите название тега', reply_markup=await kb.kb_cancel('brand'))
    else:
        await message.answer('Сортировка(<5)', reply_markup=await kb.kb_cancel('brand'))
################################# name
@newbrand.message(UpBrand.name, F.text)
async def brand_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await state.set_state(UpBrand.description)
        await state.update_data(name=message.text)
        await message.answer('Введите описание тега', reply_markup=await kb.kb_cancel('brand'))
    else:
        await message.answer('Введите название тега(<90)', reply_markup=await kb.kb_cancel('brand'))

################################# description
@newbrand.message(UpBrand.description, F.text)
async def brand_new_desc(message: Message, state: FSMContext):
    if len(message.text)<500:
        await state.update_data(description=message.text)
        data = await state.get_data()
        text = 'нет'
        if data['status'] == 'new':
           text = await set_brand_new(data)
        if data['status'] == 'up':
           text = await set_brand_up(data)
        await message.answer(f'{kb.name_menu['brand_menu']} {text}', reply_markup=await get_paginat_kb(fun=brand_menu))
        await state.clear()

    else:
        await message.answer('Введите описание тега(<500)', reply_markup=await kb.kb_cancel('brand'))
