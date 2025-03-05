from typing import Any
from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.filter import Admin
from app.setting import pageCD

from aiogram.types import Message, CallbackQuery, InputFile

paginat = Router()
paginat.message.filter(Admin())

async def get_paginat_kb(page: int = 0,  pages:int = 2, fun=None, category_id=0, product_id=0, price_id=0) -> InlineKeyboardMarkup:
    page = int(page)
    pages = int(pages)

    start = page * pages
    end = start + pages
    res = await fun(start=start, end=end, category_id=category_id, product_id=product_id, price_id=price_id)
    builder = res[0]
    len_item = res[1]
    str_name_fun = res[2]


    buttons_row = []
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(
                text=" ⬅️ ",
                # callback_data=f"pg_{(page - 1)}_{pages}_{str_name_fun}",
                callback_data=pageCD(
                    page=(page-1),
                    pages=pages,
                    fun=str_name_fun,
                    category_id=category_id,
                    product_id=product_id,
                    price_id=price_id
                    ).pack()
            )
        )
    # buttons_row.append(
    #     InlineKeyboardButton(
    #         text=f' Стр {(page+1)} ', callback_data='ok_page', show_alert=True
    #     )
    # )

    if end < len_item:
        buttons_row.append(
            InlineKeyboardButton(
                text=" ➡️ ",
                # callback_data=f"pg_{(page + 1)}_{pages}_{str_name_fun}",
                callback_data=pageCD(page=(page + 1),
                                     pages=pages,
                                     fun=str_name_fun,
                                     category_id=category_id,
                                     product_id=product_id,
                                     price_id=price_id
                                     ).pack()
            )
        )

    builder.row(*buttons_row)
    return builder.as_markup()
