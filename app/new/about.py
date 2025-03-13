from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null
from app.db.requests import get_about, set_about_new, set_about_up, set_about_name, set_about_desc, set_about_address, \
    set_about_phone, set_about_email, set_about_logo, set_about_map, set_about_photo
from app.filter import Admin
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.states import UpAbout
import app.keyboards as kb
import re

newabout = Router()
newabout.message.filter(Admin())

@newabout.callback_query(F.data == 'about')
async def about_new(callback:CallbackQuery, state: FSMContext, text_menu: str|None = ''):
    await state.clear()
    await state.set_state(UpAbout.us)
    await state.update_data(callback=callback)
    about = await get_about()
    text = 'Ведите данные:\n'
    if about:
        # about = about.one()
        # await state.update_data(status='up')
        # await state.update_data(id=about.id)
        text = (f'<b>Название:</b>\n'
                f'{about.name}\n'
                f'<b>Описание:</b>\n'
                f'{about.description}\n'
                f'<b>Адрес:</b>\n'
                f'{about.address}\n' 
                f'<b>Телефон:</b>\n'
                f'{about.phone}\n'
                f'<b>Email:</b>\n'
                f'{about.email}\n'
                f'Редактирование данных:\nСтарые будут удалены❗️\n'
                )
        if about.logo != None:
            await callback.message.answer_photo(about.logo, caption='<b>Логотип:</b>',parse_mode='html')
        if about.map != None:
            await callback.message.answer_photo(about.map, caption='<b>Карта:</b>',parse_mode='html')
        if about.photo != None:
            await callback.message.answer_photo(about.photo, caption='<b>Фото:</b>',parse_mode='html')

    await callback.message.answer(f'{kb.name_menu['about_menu']} {text_menu}\n'
                                  f'{text}',
                                  reply_markup=kb.about, parse_mode='html')
##################################### name
@newabout.callback_query(F.data == 'aboutname')
async def aboutname_new(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.name)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['name_menu'],
                                 reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
@newabout.message(UpAbout.name, F.text)
async def about_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await set_about_name(message.text)
        data = await state.get_data()
        await state.clear()
        await about_new(data['callback'], state, text_menu=kb.name_menu['name_menu'])

    else:
        await message.answer(f"{kb.name_menu['name_menu']} (< 90 зн)\n"
                             f'{message.text}',
                             reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
##################################### description
@newabout.callback_query(F.data == 'aboutdesc')
async def aboutname_desc(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.description)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['desc_menu'],
                                 reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
@newabout.message(UpAbout.description, F.text)
async def about_new_desc(message: Message, state: FSMContext):
    if len(message.text)<2000:
        await set_about_desc(message.text)
        data = await state.get_data()
        await state.clear()
        await about_new(data['callback'], state, text_menu=kb.name_menu['desc_menu'])
    else:
        await message.answer(f"{kb.name_menu['desc_menu']} (<2000 зн)",
                             reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
##################################### address
@newabout.callback_query(F.data == 'aboutaddress')
async def aboutaddress_address(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.address)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['address_menu'],
                                 reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
@newabout.message(UpAbout.address, F.text)
async def about_new_address(message: Message, state: FSMContext):
    if len(message.text)<200:
        await set_about_address(message.text)
        data = await state.get_data()
        await state.clear()
        await about_new(data['callback'], state, text_menu=kb.name_menu['address_menu'])
    else:
        await message.answer(f"{kb.name_menu['address_menu']} (<200 зн)",
                             reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
################################# phone
@newabout.callback_query(F.data == 'aboutphone')
async def aboutphone_phone(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.phone)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['phone_menu'],
                                  reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))

@newabout.message(UpAbout.phone, F.text)
async def about_new_phone(message: Message, state: FSMContext):
    if len(message.text)<20:
        await set_about_phone(message.text)
        data = await state.get_data()
        await state.clear()
        await about_new(data['callback'], state, text_menu=kb.name_menu['phone_menu'])
    else:
        await message.answer(f"{kb.name_menu['phone_menu']} (<20 зн)",
                             reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
################################# email
def validate_phone_email(email):
    pattern = re.compile(r"^\S+@\S+\.\S+$")
    if pattern.match(email):
        return True
    else:
        return False
@newabout.callback_query(F.data == 'aboutemail')
async def aboutemail_email(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.email)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['email_menu'],
                                 reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))

@newabout.message(UpAbout.email, F.text)
async def about_new_email(message: Message, state: FSMContext):
    if validate_phone_email(message.text) and len(message.text)<90:
        await set_about_email(message.text)
        data = await state.get_data()
        await state.clear()
        await about_new(data['callback'], state, text_menu=kb.name_menu['email_menu'])
    else:
        await message.answer(f"{kb.name_menu['email_menu']} Не верный формат (<90)",
                             reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))

################################# logo
@newabout.callback_query(F.data == 'aboutlogo')
async def aboutlogo_logo(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.logo)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['logo_menu'],
                                 reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
@newabout.message(UpAbout.logo, F.photo)
async def about_new_logo(message: Message, state: FSMContext):
    logo = message.photo[-1].file_id
    await set_about_logo(logo)
    data = await state.get_data()
    await state.clear()
    await about_new(data['callback'], state, text_menu=kb.name_menu['logo_menu'])

################################# map
@newabout.callback_query(F.data == 'aboutmap')
async def aboutmap_map(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.map)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['map_menu'],
                                 reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
@newabout.message(UpAbout.map, F.photo)
async def about_new_map(message: Message, state: FSMContext):
    map = message.photo[-1].file_id
    await set_about_map(map)
    data = await state.get_data()
    await state.clear()
    await about_new(data['callback'], state, text_menu=kb.name_menu['map_menu'])
################################# photo
@newabout.callback_query(F.data == 'aboutphoto')
async def aboutmap_photo(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['callback']
    await state.set_state(UpAbout.photo)
    await state.update_data(callback=c)
    await callback.message.answer(kb.name_menu['photo_menu'],
                                 reply_markup=await kb.menu_us(kb.name_menu['about_menu'], 'about'))
@newabout.message(UpAbout.photo, F.photo)
async def about_new_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await set_about_photo(photo)
    data = await state.get_data()
    await state.clear()
    await about_new(data['callback'], state, text_menu=kb.name_menu['photo_menu'])

#
# @newabout.callback_query(UpAbout.photo, F.data == 'next')
# async def about_new_photo_null(callback: CallbackQuery, state: FSMContext):
#     await state.update_data(photo=null())
#     data = await state.get_data()
#     if data['status'] == 'new':
#         await set_about_new(data)
#     if data['status'] == 'up':
#         await set_about_up(data)
#     await callback.message.bot.answer_callback_query(callback.id, text=kb.name_menu['recordAdd_menu'], show_alert=False)
#     await callback.message.answer(
#         text=f'{kb.name_menu['about_menu']} {kb.name_menu['recordAdd_menu']}',
#         reply_markup=InlineKeyboardMarkup(inline_keyboard=
#         [[kb.main_menu, InlineKeyboardButton(text=kb.name_menu['about_menu'], callback_data='about')]]))
#     await state.clear()