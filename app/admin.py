from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from app.filter import ChatTypeFilter, IsAdmin
from aiogram.filters import Command, Filter
from app.filter import Admin
import app.keyboards as kb

admin = Router()


#admin.message.filter(ChatTypeFilter(["private"]), IsAdmin())
admin.message.filter(Admin())

@admin.message(Command("admin"))
@admin.callback_query(F.data == "admin")
async def cmd_start(data, state: FSMContext):
    await state.clear()
    # await message.answer("admin")
    #photo = FSInputFile("app/img/banner.png")
    #msg = await message.answer_photo(photo, reply_markup=kb.main)  # ,caption="Меню",
    try:
        if isinstance(data, types.Message):
            await data.answer("Ⓜ️ Главное меню", reply_markup=kb.main)  # ,caption="Меню",
        elif isinstance(data, types.CallbackQuery):
            await data.message.edit_text("Ⓜ️ Главное меню", reply_markup=kb.main)
    except Exception as e: pass



# @admin.callback_query(F.data.startswith("users"))
# async def user_balance(callback:CallbackQuery):
#     try:
#        await callback.message.edit_text("Пользователи", reply_markup=kb.main)
#     except Exception as e:pass