from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from app.db.requests import get_users, get_sizes, get_color
from aiogram.types import Message, CallbackQuery
from app.filter import Admin

pagin = Router()
pagin.message.filter(Admin())

# class Pagination(CallbackData, prefix="pag"):
#     page: int

async def get_paginated_kb(page: int = 0,  pages:int = 5, switch:str = 'users') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    page = int(page)
    builder.row(InlineKeyboardButton(text='⬆️ Главное меню', callback_data='admin'),
                 InlineKeyboardButton(text=f'➕ Добавить {switch}', callback_data=f'add_{switch}'))
    start_offset:int = page * pages
    end_offset:int = start_offset +  pages
    items=[]
    if switch == 'users':
        items = await get_users()
        items = items.all()
        for item in items[start_offset:end_offset]:
            builder.row(InlineKeyboardButton(text=str(item.tg_id), callback_data=f"items_{item.id}_{switch}"))

    elif switch == 'sizes':
        items = await get_sizes()
        items = items.all()
        for item in items[start_offset:end_offset]:
            builder.row(InlineKeyboardButton(text=str(item.name), callback_data=f"items_{item.id}_{switch}"))

    elif switch == 'color':
        items = await get_color()
        items = items.all()
        for item in items[start_offset:end_offset]:
            builder.row(InlineKeyboardButton(text=str(item.name), callback_data=f"items_{item.id}_{switch}"))

    len_item = len(items)
    buttons_row = []
    # buttons_row.append([InlineKeyboardButton(text='Главное меню', callback_data='admin')])
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"pag_{(page - 1)}_{switch}",
            )
        )
    if end_offset < len_item:
        buttons_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"pag_{(page + 1)}_{switch}",
            )
        )

    builder.row(*buttons_row)


    return builder.as_markup()

# @pagin.message(Command(commands=["users"]))
@pagin.callback_query(F.data.startswith("users"))
async def send_products_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text="👨‍👩‍👦 Пользователи",
        reply_markup=await get_paginated_kb(pages=3, switch="users"),
    )

@pagin.callback_query(F.data.startswith("sizes"))
async def send_products_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text="📶 Размеры",
        reply_markup=await get_paginated_kb(pages=3, switch="sizes"),
    )
@pagin.callback_query(F.data.startswith("color"))
async def send_products_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text="🔵 Цвета",
        reply_markup=await get_paginated_kb(pages=3, switch="color"),
    )

@pagin.callback_query(F.data.startswith('pag_'))
async def products_pagination_callback(callback: CallbackQuery):
    page = callback.data.split('_')[1]
    switch = callback.data.split('_')[2]
    await callback.message.edit_reply_markup(
    reply_markup=await get_paginated_kb(page=page, pages=3, switch=switch)
)