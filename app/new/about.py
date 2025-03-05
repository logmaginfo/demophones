from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from sqlalchemy import null
from app.db.requests import get_about, set_about_new, set_about_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.states import UpAbout
import app.keyboards as kb
import re

newabout = Router()
newabout.message.filter(Admin())

@newabout.callback_query(F.data.startswith('about'))
async def about_new(callback:CallbackQuery, state: FSMContext):
    await state.update_data(status='new')
    about = await get_about()
    text = 'Ведите данные:\n'
    if about:
        # about = about.one()
        await state.update_data(status='up')
        await state.update_data(id=about.id)
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

    await state.set_state(UpAbout.name)

    await callback.message.answer(f'{kb.name_menu['about_menu']}\n'
                                  f'{text}'
                                  f'<b>Введите название</b>:',
                                      reply_markup=kb.main_top_cancel,
                                      parse_mode='html')
##################################### name
@newabout.message(UpAbout.name, F.text)
async def about_new_name(message: Message, state: FSMContext):
    if len(message.text)<90:
        await state.update_data(name=message.text)
        await state.set_state(UpAbout.description)
        await message.answer('Добавьте описание (<2000 зн)',
                             reply_markup=kb.main_top_cancel)
    else:
        await message.answer('Введите название (< 90 зн)',
                             reply_markup=kb.main_top_cancel)
##################################### description
@newabout.message(UpAbout.description, F.text)
async def about_new_desc(message: Message, state: FSMContext):
    if len(message.text)<2000:
        await state.update_data(description=message.text)
        await state.set_state(UpAbout.address)
        await message.answer('Адрес (<200 зн)',
                             reply_markup=kb.main_top_cancel)
    else:
        await message.answer('Введите описание(<2000 зн)',
                             reply_markup=kb.main_top_cancel)
##################################### address
@newabout.message(UpAbout.address, F.text)
async def about_new_address(message: Message, state: FSMContext):
    if len(message.text)<200:
        await state.update_data(address=message.text)
        await state.set_state(UpAbout.phone)
        await message.answer('☎️ Телефон (<20 зн)',
                             reply_markup=kb.main_top_cancel)
    else:
        await message.answer('Введите описание(<200 зн)',
                             reply_markup=kb.main_top_cancel)
################################# phone
def validate_phone_number(phone_number):
    pattern = r'^\+?7\d{10}$'
    pattern2 = r'^\+?8\d{10}$'
    if re.match(pattern, phone_number) or re.match(pattern2, phone_number):
        return True
    else:
        return False
@newabout.message(UpAbout.phone, F.text)
async def about_new_phone(message: Message, state: FSMContext):
    if len(message.text)<20:
        await state.set_state(UpAbout.email)
        await state.update_data(phone=message.text)
        await message.answer('Введите 📭 email', reply_markup=kb.main_top_cancel)
    else:
        await message.answer('☎️ Телефон (<20 зн)', reply_markup=kb.main_top_cancel)
################################# email
def validate_phone_email(email):
    pattern = re.compile(r"^\S+@\S+\.\S+$")
    if pattern.match(email):
        return True
    else:
        return False

@newabout.message(UpAbout.email, F.text)
async def about_new_email(message: Message, state: FSMContext):
    if validate_phone_email(message.text) and len(message.text)<90:
        await state.set_state(UpAbout.logo)
        await state.update_data(email=message.text)
        await message.answer('Добавьте логотип', reply_markup=kb.main_top_cancel_next)
    else:
        await message.answer('Формат 📭: myemail@myemail.my (<90)', reply_markup=kb.main_top_cancel)

################################# logo
@newabout.message(UpAbout.logo, F.photo)
async def about_new_logo(message: Message, state: FSMContext):
    logo = message.photo[-1].file_id
    await state.update_data(logo=logo)
    await state.set_state(UpAbout.map)
    await message.answer('Добавьте карту', reply_markup=kb.main_top_cancel_next)

@newabout.callback_query(UpAbout.logo, F.data == 'next')
async def about_new_logo_null(callback:CallbackQuery, state: FSMContext):
    await state.update_data(logo=null())
    await state.set_state(UpAbout.map)
    await callback.message.answer('Добавьте карту', reply_markup=kb.main_top_cancel_next)


################################# map
@newabout.message(UpAbout.map, F.photo)
async def about_new_map(message: Message, state: FSMContext):
    map = message.photo[-1].file_id
    await state.update_data(map=map)
    await state.set_state(UpAbout.photo)
    await message.answer('Добавьте фото', reply_markup=kb.main_top_cancel_next)


@newabout.callback_query(UpAbout.map, F.data == 'next')
async def about_new_photo_null(callback: CallbackQuery, state: FSMContext):
    await state.update_data(map=null())
    await state.set_state(UpAbout.photo)
    await callback.message.answer('Добавьте фото', reply_markup=kb.main_top_cancel_next)

################################# photo
@newabout.message(UpAbout.photo, F.photo)
async def about_new_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    if data['status'] == 'new':
       await set_about_new(data)
    if data['status'] == 'up':
       await set_about_up(data)
    await message.answer(
        text=f'{kb.name_menu['about_menu']} {kb.name_menu['recordAdd_menu']}',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=
        [[kb.main_menu, InlineKeyboardButton(text=kb.name_menu['about_menu'], callback_data='about')]]))
    await state.clear()


@newabout.callback_query(UpAbout.photo, F.data == 'next')
async def about_new_photo_null(callback: CallbackQuery, state: FSMContext):
    await state.update_data(photo=null())
    data = await state.get_data()
    if data['status'] == 'new':
        await set_about_new(data)
    if data['status'] == 'up':
        await set_about_up(data)
    await callback.message.bot.answer_callback_query(callback.id, text=kb.name_menu['recordAdd_menu'], show_alert=False)
    await callback.message.answer(
        text=f'{kb.name_menu['about_menu']} {kb.name_menu['recordAdd_menu']}',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=
        [[kb.main_menu, InlineKeyboardButton(text=kb.name_menu['about_menu'], callback_data='about')]]))
    await state.clear()