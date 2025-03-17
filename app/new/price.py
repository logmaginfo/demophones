from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import null
from app.admin import product_menu, cat_menu_start, price_menu, color_menu
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_category_id, get_product_id, set_product_new, set_product_up, get_price_id, \
    get_color_id, get_sizes_id, get_color, get_sizes, set_price_new, set_price_up
from app.filter import Admin
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from app.states import UpPrice
import app.keyboards as kb

newprice = Router()
newprice.message.filter(Admin())

@newprice.callback_query(F.data.startswith('add_price'))
async def price_new(callback:CallbackQuery, state: FSMContext):
    product_id = callback.data.split('_')[2]
    category_id = callback.data.split('_')[3]
    await state.update_data(product_id=product_id)
    await state.update_data(category_id=category_id)
    await state.update_data(status='new')
    await state.set_state(UpPrice.name)
    #####
    data = await state.get_data()
    #####
    await callback.message.answer('💰 Название прайса:',
                                  reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'),
                                  parse_mode='html')
################################# upprice_
@newprice.callback_query(F.data.startswith('upprice_'))
async def price_up(callback:CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[4]
    product_id = callback.data.split('_')[3]
    id = callback.data.split('_')[2]
    await state.set_state(UpPrice.name)
    await state.update_data(product_id=product_id)
    await state.update_data(status='up')
    product = await get_product_id(product_id)
    price = await get_price_id(id)
    category = await get_category_id(product.category_id)
    if not category:
        catname = kb.name_menu['category_menu']
    else:
        catname = category.name
    await state.update_data(category_id=product.category_id)
    await state.update_data(id=id)
    #####
    data = await state.get_data()
    #####
    await callback.message.answer(f'<b>Данные:</b>\n'
                                  f'Категория: {catname}\n'
                                  f'(🆔 {price.id})\n'
                                  f'Название : {price.name}\n'
                                  f'💰 Цена: {price.price}\n'
                                  f'💰 Цена со скидкой: {price.price_discount}\n'
                                  f'Количество: {price.quantity}\n'
                                  f'Продукт: {product.name}\n'                                  
                                  f'Цвет: {price.color}\n'
                                  f'Размер: {price.sizes}\n'
                                  f'<b>Новые данные:\n'
                                  'Старые будут удалены❗️\n'
                                  'Название прайса:</b>',
                                  reply_markup=await kb.kb_cancel(f'price_{product_id}_{category_id}'), parse_mode='html')

##################################### name
@newprice.message(UpPrice.name, F.text)
async def price_new_name(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    if len(message.text)<90:
        await state.update_data(name=message.text)
        await state.set_state(UpPrice.price)
        await message.answer('Цена товара',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
    else:
        data = await state.get_data()
        await message.answer('Название прайса (< 90 зн)',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))

##################################### price
@newprice.message(UpPrice.price, F.text)
async def price_new_price(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await state.set_state(UpPrice.price_discount)
        await message.answer('Скидка на товар (нет введите 0)',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
    except Exception as e:
        data = await state.get_data()
        await message.answer('Цена товара - это число',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))

##################################### price_discount
@newprice.message(UpPrice.price_discount, F.text)
async def price_new_price_discount(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    try:
        price_discoun = float(message.text)
        await state.update_data(price_discount=price_discoun)
        await state.set_state(UpPrice.quantity)
        await message.answer('Количество товара на складе:',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
    except Exception as e:
        data = await state.get_data()
        await message.answer('Скидка на товар - это число',
                             reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))

##################################### quantity
async def color(category_id):
    color = await get_color()
    color = color.all()
    builder = InlineKeyboardBuilder()
    buttons = []
    for item in color:
        buttons.append(InlineKeyboardButton(text=f'{item.name}',
                                      callback_data=f'prcolor_{item.id}'))
    builder.row(*buttons)
    builder.adjust(2, 2)
    builder.row(await kb.add_item('color', f"🙅🏻 Отмена 💰: Перейти к созданию цвета"))
    builder.row(InlineKeyboardButton(text='🙅🏻 Отмена', callback_data=f'product_{category_id}'))
    return builder
@newprice.message(UpPrice.quantity, F.text)
async def price_new_color(message: Message, state: FSMContext):
    #####
    data = await state.get_data()
    #####
    # try:
    quantity = int(message.text)
    await state.update_data(quantity=quantity)
    await state.set_state(UpPrice.color)
    builder = await color(data['category_id'])
    await message.answer('Цвет товара:', reply_markup=builder.as_markup())
    # except Exception as e:
    #     data = await state.get_data()
    #     await message.answer('Количество - это число:',
    #                          reply_markup=await kb.kb_cancel(f'product_{data['category_id']}'))
##################################### color
async def sizes(category_id):
    sizes = await get_sizes()
    sizes = sizes.all()
    builder = InlineKeyboardBuilder()
    buttons = []
    for item in sizes:
        buttons.append(InlineKeyboardButton(text=f'{item.name}',
                                      callback_data=f'prsizes_{item.id}'))
    builder.row(*buttons)
    builder.adjust(2, 2)
    builder.row(await kb.add_item('sizes', f"🙅🏻 Отмена 💰: Перейти к созданию размера"))
    builder.row(InlineKeyboardButton(text='🙅🏻 Отмена', callback_data=f'product_{category_id}'))
    return builder
@newprice.callback_query(UpPrice.color, F.data.startswith('prcolor'))
async def price_new_sizes(callback:CallbackQuery, state: FSMContext):
    color_id = callback.data.split('_')[1]
    await state.update_data(color_id=color_id)
    await state.set_state(UpPrice.sizes)
    #####
    data = await state.get_data()
    #####
    builder = await sizes(data['category_id'])
    await callback.message.answer('Размер товара:', reply_markup=builder.as_markup())

##################################### sizes
@newprice.callback_query(UpPrice.sizes, F.data.startswith('prsizes'))
async def price_new_sizes(callback:CallbackQuery, state: FSMContext):
    sizes_id = callback.data.split('_')[1]
    await state.update_data(sizes_id=sizes_id)
    #####
    data = await state.get_data()
    #####
    cat_menu_list = await cat_menu_start(data['category_id'])
    product = await get_product_id(data['product_id'])
    text = 'нет'
    if data['status'] == 'new':
        text = await set_price_new(data)
    if data['status'] == 'up':
        text = await set_price_up(data)
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await callback.message.edit_text(
        text=f'{cat_menu_list[1]} / {product.name} {text}',
        reply_markup=await get_paginat_kb(fun=price_menu, category_id=data['category_id'], product_id=data['product_id']))
    await state.clear()
