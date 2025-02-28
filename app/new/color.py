from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null

from app.admin import color_menu
from app.cmd.pagination import get_paginated_kb
from app.cmd.paginator import get_paginat_kb
from app.db.requests import set_color_new, get_color_id, set_color_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpSize, UpColor
import app.keyboards as kb

newcolor= Router()
newcolor.message.filter(Admin())

@newcolor.callback_query(F.data.startswith('add_color'))
async def color_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpColor.name)
    await callback.message.answer('Введите название цвета <b>*</b>', reply_markup=await kb.kb_cancel('color_menu'), parse_mode='html')

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
    if color.photo != None:
        await callback.message.answer_photo(color.photo)
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'(🆔 {color.id = })\n'
                                  f'{color.name = }\n'
                                  f'{color.photo=}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены❗️\nВведите название цвета</b>', reply_markup=await kb.kb_cancel('color_menu'), parse_mode='html')


################################# name
@newcolor.message(UpColor.name, F.text)
async def color_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await state.set_state(UpColor.photo)
        await state.update_data(name=message.text)
        await message.answer('Добавьте изображение', reply_markup=await kb.kb_next('color_menu'))
    else:
        await message.answer('Введите название цвета(<90)', reply_markup=await kb.kb_cancel('color_menu'))

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
    await message.answer(f"{kb.name_menu['color_menu']} {text}", reply_markup=await get_paginat_kb(fun=color_menu))


@newcolor.callback_query(UpColor.photo, F.data == 'next')
async def color_new_photo_null(callback:CallbackQuery, state: FSMContext):
    await state.update_data(photo=null())
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_color_new(data)
        await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    if data['status'] == 'up':
        text = await set_color_up(data)
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await state.clear()
    # await callback.message.answer(text, reply_markup=await get_paginated_kb(pages=10, switch=data["switch"]))
    await callback.message.edit_text(f"{kb.name_menu['color_menu']} {text}", reply_markup=await get_paginat_kb(fun=color_menu))
