from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import null
from app.admin import category_menu, product_menu, cat_menu_start
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_category_id, get_product_id, set_product_new, set_product_up, get_brands, \
    get_productbrand_pl, set_productbrand, del_productbrand
from app.filter import Admin
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.states import UpCategory, UpProduct
import app.keyboards as kb

newproductbrand = Router()
newproductbrand.message.filter(Admin())

@newproductbrand.callback_query(F.data.startswith('prbr_'))
async def productbrand_new(callback:CallbackQuery, state: FSMContext):
    product_id = callback.data.split('_')[1]
    product = await get_product_id(product_id)
    category_id = status = callback.data.split('_')[2]
    try:
        status = callback.data.split('_')[3]
        brand_id = callback.data.split('_')[4]
        if status == 'add':
            await set_productbrand(brand_id, product_id)
        if status == 'del':
            await del_productbrand(brand_id, product_id)
    except Exception as e:
        pass
    brand = await get_brands()
    brand = brand.all()
    builder = InlineKeyboardBuilder()
    buttons = []
    for item in brand:
        productbrand = await get_productbrand_pl(item.id, product_id)
        if not productbrand:
          buttons.append(InlineKeyboardButton(text=f'{item.name} ➕', callback_data=f'prbr_{product_id}_{category_id}_add_{item.id}'))
        else:
            buttons.append(InlineKeyboardButton(text=f'{item.name} ➖', callback_data=f'prbr_{product_id}_{category_id}_del_{item.id}'))

    builder.row(*buttons)
    builder.adjust(2, 2)
    builder.row(InlineKeyboardButton(text='⬅️ 🎁', callback_data=f'product_{category_id}'))
    cat_menu_list = await cat_menu_start(category_id)
    await callback.message.edit_text(f'📌 {cat_menu_list[1]} / {product.name}', reply_markup=builder.as_markup())