import sqlalchemy
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from app.db.requests import set_user_new, get_user_id, set_user_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery
from app.states import UpUser
import app.keyboards as kb
import re

newuser = Router()
newuser.message.filter(Admin())
@newuser.callback_query(F.data.startswith('add_users'))
async def user_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    await state.update_data(switch=switch)
    await state.update_data(status='new')
    await state.set_state(UpUser.tg_id)
    await callback.message.answer('Введите id Telegram <b>*</b>', reply_markup=kb.cancel, parse_mode='html')

@newuser.message(UpUser.tg_id, F.text)
async def user_new_tg_id(message: Message, state: FSMContext):
    if message.text.isnumeric() and len(message.text)<20:
        await state.set_state(UpUser.name)
        await state.update_data(tg_id=message.text)
        await message.answer('Введите Имя', reply_markup=kb.next)
    else:
        await message.answer('Введите id Telegram - число (<20) *', reply_markup=kb.cancel)#, parse_mode='html'

################################# up
@newuser.callback_query(F.data.startswith('up_'))
async def user_new(callback:CallbackQuery, state: FSMContext):
    switch = callback.data.split('_')[1]
    id = callback.data.split('_')[2]
    await state.set_state(UpUser.name)
    await state.update_data(switch=switch)
    await state.update_data(status='up')
    user = await get_user_id(id)
    await state.update_data(tg_id=user.tg_id)
    await callback.message.answer(f'<b>Данные пользователя:</b>\n'
                                  f'(🆔 {user.id = }) {user.tg_id = }\n'
                                  f'{user.name = } {user.last_name=}\n'
                                  f'{user.phone=}\n'
                                  f'{user.email=}\n'
                                  f'{user.address=}\n'
                                  f'{user.comment=}\n'
                                  f'{user.date_create.strftime("%d.%m.%Y %H:%M")}', parse_mode='html')

    await callback.message.answer('<b>Новые данные:\n'
                                  'Старые будут удалены!</b>\nВведите Имя', reply_markup=kb.next, parse_mode='html')

################################# name
@newuser.message(UpUser.name, F.text)
async def user_new_name(message: Message, state: FSMContext):
    if len(message.text)<40:
        await state.set_state(UpUser.last_name)
        await state.update_data(name=message.text)
        await message.answer('Введите Фамилию', reply_markup=kb.next)
    else:
        await message.answer('Введите Имя (<40)', reply_markup=kb.next)
# @newuser.message(UpUser.name)
@newuser.callback_query(UpUser.name, F.data == 'next')
async def user_new_name_null(callback:CallbackQuery, state: FSMContext):
    await state.set_state(UpUser.last_name)
    await state.update_data(name=sqlalchemy.null())
    await callback.message.edit_text('Введите Фамилию', reply_markup=kb.next)
################################# last_name
@newuser.message(UpUser.last_name, F.text)
async def user_new_last_name(message: Message, state: FSMContext):
    if len(message.text)<40:
        await state.set_state(UpUser.phone)
        await state.update_data(last_name=message.text)
        data = await state.get_data()
        await message.answer(f'Введите № телефона. Формат: +71111111111', reply_markup=kb.next)
    else:
        await message.answer('Фамилия (<40)', reply_markup=kb.next)

# @newuser.message(UpUser.last_name)
@newuser.callback_query(UpUser.last_name, F.data == 'next')
async def user_new_last_name_null(callback:CallbackQuery, state: FSMContext):
    await state.set_state(UpUser.phone)
    await state.update_data(last_name=sqlalchemy.null())
    await callback.message.edit_text('Введите № телефона. Формат: +71111111111', reply_markup=kb.next)

################################# phone
def validate_phone_number(phone_number):
    pattern = r'^\+?7\d{10}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False
@newuser.message(UpUser.phone, F.text)
async def user_new_phone(message: Message, state: FSMContext):
    if validate_phone_number(message.text) and len(message.text)<20:
        await state.set_state(UpUser.email)
        await state.update_data(phone=message.text)
        await message.answer('Введите email', reply_markup=kb.next)
    else:
        await message.answer('Формат: +71111111111 (<20)', reply_markup=kb.next)

# @newuser.message(UpUser.phone)
@newuser.callback_query(UpUser.phone, F.data == 'next')
async def user_new_phone_null(callback:CallbackQuery, state: FSMContext):
    await state.set_state(UpUser.email)
    await state.update_data(phone=sqlalchemy.null())
    await callback.message.edit_text('Введите email', reply_markup=kb.next)

################################# email
def validate_phone_email(email):
    pattern = re.compile(r"^\S+@\S+\.\S+$")
    if pattern.match(email):
        return True
    else:
        return False

@newuser.message(UpUser.email, F.text)
async def user_new_email(message: Message, state: FSMContext):
    if validate_phone_email(message.text) and len(message.text)<90:
        await state.set_state(UpUser.address)
        await state.update_data(email=message.text)
        await message.answer('Введите адрес', reply_markup=kb.next)
    else:
        await message.answer('Формат: myemail@myemail.my (<90)', reply_markup=kb.next)

@newuser.callback_query(UpUser.email, F.data == 'next')
async def user_new_email_null(callback:CallbackQuery, state: FSMContext):
    await state.set_state(UpUser.address)
    await state.update_data(email=sqlalchemy.null())
    await callback.message.edit_text('Введите адрес', reply_markup=kb.next)

################################# address

@newuser.message(UpUser.address, F.text)
async def user_new_address(message: Message, state: FSMContext):
    if len(message.text)<180:
        await state.set_state(UpUser.comment)
        await state.update_data(address=message.text)
        await message.answer('Введите комментарий', reply_markup=kb.next)
    else:
        await message.answer('Адрес (<180)', reply_markup=kb.next)

@newuser.callback_query(UpUser.address, F.data == 'next')
async def user_new_address_null(callback:CallbackQuery, state: FSMContext):
    await state.set_state(UpUser.comment)
    await state.update_data(address=sqlalchemy.null())
    await callback.message.edit_text('Введите комментарий', reply_markup=kb.next)

################################# comment

@newuser.message(UpUser.comment, F.text)
async def user_new_comment(message: Message, state: FSMContext):
    if len(message.text)<280:
        await state.update_data(comment=message.text)
        data = await state.get_data()
        text = 'нет'
        if data['status'] == 'new':
           text = await set_user_new(data)
        if data['status'] == 'up':
           text = await set_user_up(data)
        await message.answer(text, reply_markup=kb.main)
    else:
        await message.answer('Комментарий (<280)', reply_markup=kb.next)


@newuser.callback_query(UpUser.comment, F.data == 'next')
async def user_new_comment_null(callback:CallbackQuery, state: FSMContext):
    await state.update_data(comment=sqlalchemy.null())
    data = await state.get_data()
    text = 'нет'
    if data['status'] == 'new':
        text = await set_user_new(data)
    if data['status'] == 'up':
        text = await set_user_up(data)
    await callback.message.edit_text(text, reply_markup=kb.main)

################################################
