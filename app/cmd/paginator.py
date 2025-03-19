from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.setting import pageCD

paginat = Router()
# paginat.message.filter(Admin())

async def get_paginat_kb(page: int = 0,  pages:int = 2, fun=None,
                         category_id=0, product_id=0, price_id=0,
                         user_id=0, filterorder='all') -> InlineKeyboardMarkup:
    page = int(page)
    pages = int(pages)

    start = page * pages
    end = start + pages
    res = await fun(start=start, end=end, category_id=category_id,
                    product_id=product_id, price_id=price_id,
                    user_id=user_id, filterorder=filterorder)
    builder = res[0]
    len_item = res[1]
    str_name_fun = res[2]


    buttons_row = []
    if page > 0:
        buttons_row.append(
            InlineKeyboardButton(
                text=f" ⬅️ ",
                # callback_data=f"pg_{(page - 1)}_{pages}_{str_name_fun}",
                callback_data=pageCD(
                    page=(page-1),
                    pages=pages,
                    fun=str_name_fun,
                    category_id=category_id,
                    product_id=product_id,
                    price_id=price_id,
                    user_id=user_id,
                    filterorder=filterorder
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
                text=f" ➡️ ",
                # callback_data=f"pg_{(page + 1)}_{pages}_{str_name_fun}",
                callback_data=pageCD(page=(page + 1),
                                     pages=pages,
                                     fun=str_name_fun,
                                     category_id=category_id,
                                     product_id=product_id,
                                     price_id=price_id,
                                     user_id=user_id,
                                     filterorder=filterorder
                                     ).pack()
            )
        )

    builder.row(*buttons_row)
    return builder.as_markup()

