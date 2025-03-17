from typing import Any
from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import BigInteger

from app.filter import Admin
from app.setting import pageCD, pageCD2

from aiogram.types import Message, CallbackQuery, InputFile

paginat = Router()
# paginat.message.filter(Admin())

async def get_paginat_kb2(page: int = 0,  pages:int = 2, fun=None, key=None, val=None) -> InlineKeyboardMarkup:
    page = int(page)
    pages = int(pages)


    start = page * pages
    end = start + pages
    res = await fun(start=start, end=end, key=key, val=val)
    builder = res[0]
    len_item = res[1]
    str_name_fun = res[2]


    buttons_row = []
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(
                text=f" ⬅️ ",
                # callback_data=f"pg_{(page - 1)}_{pages}_{str_name_fun}",
                callback_data=pageCD2(
                    page=(page-1),
                    pages=pages,
                    fun=str_name_fun,
                    key=key,
                    val=val
                    ).pack()
            )
        )



    if end < len_item:
        buttons_row.append(
            InlineKeyboardButton(
                text=f" ➡️ ",
                # callback_data=f"pg_{(page + 1)}_{pages}_{str_name_fun}",
                callback_data=pageCD2(page=(page + 1),
                                     pages=pages,
                                     fun=str_name_fun,
                                     key=key,
                                     val=val
                                     ).pack()
            )
        )

    builder.row(*buttons_row)
    return builder.as_markup()

