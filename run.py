import os
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from dotenv import load_dotenv #pip install python-dotenv
import asyncio
from aiogram import Bot, Dispatcher, types #from aiogram import Router, F, types
from app.admin import admin
from app.cmd.cmd import cmdPrivate
from app.cmd.paginator import paginat
from app.db.requests import get_ordernumber_orders, get_price_id
from app.new.about import newabout
from app.new.brand import newbrand
from app.new.category import newcategory
from app.new.color import newcolor
from app.new.delivery import newdelivery
from app.new.end import endrouter
from app.new.photo import newphoto
from app.new.price import newprice
from app.new.product import newproduct
from app.new.productbrand import newproductbrand
from app.new.sizes import newsize
from app.new.user import newuser
from app.pay import pay
from app.user import user
from app.db.models import async_main
import app.keyboards as kb

dp = Dispatcher()
load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = []

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    ordernumber_id = pre_checkout_query.invoice_payload
    ordernumber = await get_ordernumber_orders(ordernumber_id)
    quantity_all = []
    for order in ordernumber.orders:
        price = await get_price_id(order.price_id)
        if not price: quantity_all.append(False)
        else:
            if price.quantity <= 0:
                quantity_all.append(False)
    if False in quantity_all:
        res = False
    else:
        res = True
    try:
       await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=res)
    except Exception:
        await bot.send_message(pre_checkout_query.from_user.id, "Товара нет на складе",
                               reply_markup = await kb.menu_us(kb.name_menu['main_menu'],
                                                "start")
                               )

async def main():
    dp.include_routers(user, admin, newuser, newsize,
                       newcolor, newbrand, newcategory, newdelivery,
                       newproductbrand, newproduct, newprice, paginat, newphoto, newabout, pay, endrouter, )
    dp.startup.register(on_startup)
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    # await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(commands=cmdPrivate, scope=BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=cmdGrup, scope=BotCommandScopeAllGroupChats())
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    await async_main()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Off')