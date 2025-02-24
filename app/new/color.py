import sqlalchemy
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from app.db.requests import set_user_new, get_user_id, set_user_up, set_size_new, get_size_id, set_size_up, \
    set_color_new, get_color_id, set_color_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpSize, UpColor
import app.keyboards as kb
import re

newcolor= Router()
newcolor.message.filter(Admin())

@newcolor.callback_query(F.data.startswith('add_color'))
async def color_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpColor.name)
    await callback.message.answer('Введите название цвета <b>*</b>', reply_markup=kb.cancel, parse_mode='html')

################################# upcolor
@newcolor.callback_query(F.data.startswith('upcolor_'))
async def color_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpColor.name)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    color = await get_color_id(id)
    await state.update_data(id=color.id)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {color.id = })\n'
                                  f'{color.name = }\n'
                                  f'{color.photo=}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены!</b>\nВведите название цвета', reply_markup=kb.cancel, parse_mode='html')


################################# name
@newcolor.message(UpColor.name, F.text)
async def color_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await state.set_state(UpColor.photo)
        await state.update_data(name=message.text)
        await message.answer('Добавьте изображение', reply_markup=kb.next)
    else:
        await message.answer('Введите название цвета(<90)', reply_markup=kb.cancel)
################################# photo
@newcolor.message(UpColor.photo, F.photo)
async def color_new_photo(message: Message, state: FSMContext):
    id_photo = message.photo[-1].file_id
    await state.update_data(photo=id_photo)
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_color_new(data)
    if data['status'] == 'up':
        text = await set_color_up(data)

    await state.clear()
    await message.answer(text, reply_markup=kb.main)

@newcolor.callback_query(UpColor.photo, F.data == 'next')
async def color_new_photo_null(callback:CallbackQuery, state: FSMContext):
    await state.update_data(photo=sqlalchemy.null())
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_color_new(data)
    if data['status'] == 'up':
        text = await set_color_up(data)

    await state.clear()
    await callback.message.answer(text, reply_markup=kb.main)