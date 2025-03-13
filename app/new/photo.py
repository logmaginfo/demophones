from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import null
from app.admin import product_menu, cat_menu_start, price_menu, color_menu, photo_menu
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_category_id, get_product_id, set_product_new, set_product_up, get_price_id, \
    get_color_id, get_sizes_id, get_color, get_sizes, set_price_new, set_price_up, set_photo_new, get_photo_id
from app.filter import Admin
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from app.states import UpPrice, UpPhoto
import app.keyboards as kb

newphoto = Router()
newphoto.message.filter(Admin())

#photo_{price_id}_{product_id}_{category_id}
@newphoto.callback_query(F.data.startswith('add_photo'))
async def photo_new(callback:CallbackQuery, state: FSMContext):
    price_id = callback.data.split('_')[2]
    product_id = callback.data.split('_')[3]
    category_id = callback.data.split('_')[4]
    await state.update_data(price_id=price_id)
    await state.update_data(product_id=product_id)
    await state.update_data(category_id=category_id)
    await state.update_data(status='new')
    await state.set_state(UpPhoto.sort)
    #####
    data = await state.get_data()
    #####
    await callback.message.answer(kb.name_menu['sort_menu'],
                                  reply_markup=await kb.kb_cancel(f'price_{product_id}_{category_id}'),
                                  parse_mode='html')

################################# upphoto_  reply_markup=builder.as_markup()  photo_{item.id}_{product_id}_{category_id}"

@newphoto.callback_query(F.data.startswith('upphoto'))
async def photo_new(callback:CallbackQuery, state: FSMContext):
    photo_id = callback.data.split('_')[1]
    price_id = callback.data.split('_')[2]
    product_id = callback.data.split('_')[3]
    category_id = callback.data.split('_')[4]

    photo = await get_photo_id(photo_id)
    await callback.message.answer_photo(photo.photo, caption=kb.name_menu['photo_menu'],
        reply_markup= await kb.menu_us("🎁", f"photo_{price_id}_{product_id}_{category_id}"),
                                        parse_mode='html')

################################# sort
@newphoto.message(UpPhoto.sort, F.text)
async def photo_new_sort(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<5:
        await state.set_state(UpPhoto.photo)
        await state.update_data(sort=message.text)
        await message.answer(kb.name_menu['photo_menu'], reply_markup=await kb.kb_cancel(f'price_{data['product_id']}_{data['category_id']}'))
    else:
        await message.answer('Сортировка(<5)', reply_markup=await kb.kb_cancel(f'price_{data['product_id']}_{data['category_id']}'))

################################# photo
@newphoto.message(UpPhoto.photo, F.photo)
async def photo_new_name(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    #####
    data = await state.get_data()
    #####
    cat_menu_list = await cat_menu_start(data['category_id'])
    product = await get_product_id(data['product_id'])
    price = await get_price_id(data['price_id'])
    text = 'нет'
    if data['status'] == 'new':
        text = await set_photo_new(data)
    if data['status'] == 'up':
        pass
        # text = await set_photo_up(data)
    await message.answer(
        text=f'{cat_menu_list[1]} / {product.name} / {price.name} / {text}',
        reply_markup=await get_paginat_kb(fun=photo_menu, category_id=data['category_id'], product_id=data['product_id'], price_id=data['price_id']))
    await state.clear()
