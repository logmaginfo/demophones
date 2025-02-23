from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, Bot
from app.filter import ChatTypeFilter
from app.db.requests import set_user


user = Router()
# user.message.filter(ChatTypeFilter(["group", "supergroup"]))
# user.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))
@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('HY')
    await set_user(message)
    await state.clear()


# @user.message(Command("admin"))
# async def get_admins(message: types.Message, bot: Bot):
#     chat_id = message.chat.id
#     admins_list = await bot.get_chat_administrators(chat_id)
#     #просмотреть все данные и свойства полученных объектов
#     #print(f' ------------------------ >>>>> {admins_list}')
#     # Код ниже это генератор списка, как и этот x = [i for i in range(10)]
#     admins_list = [
#         member.user.id
#         for member in admins_list
#         if member.status == "creator" or member.status == "administrator"
#     ]
#     #print(f' ------------------------ >>>>> {admins_list}')
#     #print(f' ------------------------ >>>>> {message.from_user.id}')
#     bot.my_admins_list = admins_list
#     if message.from_user.id in admins_list:
#        # print(f' ------------------------ >>>>> {bot.my_admins_list}')
#         await message.delete()