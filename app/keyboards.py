from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👨‍👩‍👦 Пользователи', callback_data='users')],
        [InlineKeyboardButton(text='📶 Размеры', callback_data='sizes')],
        [InlineKeyboardButton(text='🔵 Цвета', callback_data='color')],
])
#[InlineKeyboardButton(text='Главное меню', callback_data='admin')]


cancel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='❌ Отмена', callback_data='admin')]])

next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='❌ Отмена', callback_data='admin'),
         InlineKeyboardButton(text='⏩ Пропустить', callback_data='next')]])