from typing import Any
from aiogram.filters.callback_data import CallbackData

class pageCD(CallbackData, prefix='pg'):
    page:int
    pages:int
    fun:Any
    category_id:int|str
    product_id:int|str
    price_id:int|str
    user_id:int|str
    filterorder: str

class pageCD2(CallbackData, prefix='pg2'):
    page:int
    pages:int
    fun:Any
    key:str
    val:str


BQ = 10#basket quantity
SO = {'all':'Все','new':'Новый', 'verified':'Проверен','pay':'Оплачен',
      'delivery':'Отправлен', 'received':'Получен',
      'archive':'В архиве', 'cancel':'Отменен'}#status order
# ADMINS = [1418091164, 7840303553]
ADMINS = [1418091164, 7840303553]