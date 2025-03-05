import os
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from dotenv import load_dotenv #pip install python-dotenv
import asyncio
from aiogram import Bot, Dispatcher
from app.admin import admin
from app.cmd.paginator import paginat
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
from app.user import user
from app.db.models import async_main

dp = Dispatcher()
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = []

async def main():
    dp.include_routers(user, admin, newuser, newsize,
                       newcolor, newbrand, newcategory, newdelivery,
                       newproductbrand, newproduct, newprice, paginat, newphoto, newabout, endrouter)
    dp.startup.register(on_startup)
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    # await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    #await bot.set_my_commands(commands=cmdPrivate, scope=BotCommandScopeAllPrivateChats())
    #await bot.set_my_commands(commands=cmdGrup, scope=BotCommandScopeAllGroupChats())
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    await async_main()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Off')