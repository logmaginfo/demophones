
from typing import Any
from aiogram.filters.callback_data import CallbackData

# from app.admin import brand_menu, sizes_menu, users_menu, color_menu, delivery_menu, category_menu, subcategory_menu


class pageCD(CallbackData, prefix='pg'):
    page:int
    pages:int
    fun:Any
    category_id:int|str
    product_id:int|str
    price_id:int|str


# funs_dic={'brand_menu':brand_menu,'sizes_menu':sizes_menu, 'users_menu':users_menu,
#           'color_menu':color_menu, 'delivery_menu':delivery_menu, 'category_menu':category_menu,
#           'subcategory_menu':subcategory_menu}