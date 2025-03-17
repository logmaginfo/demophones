from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputFile, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder

from app.cmd.paginator import get_paginat_kb
from app.filter import ChatTypeFilter
from app.db.requests import set_user, get_about, get_cat, get_category_category_id, get_category_subcat_count, \
    get_product_count, get_category_id, get_category_category_id_product, get_product_id, get_products_id, get_price_id, \
    get_price_product, get_color_id, get_sizes_id, get_price_photo_count, get_photo_id, get_photo_price_id, get_user_id, \
    get_user_tg_id, get_basket_user_product, set_basket, get_basket, get_basket_all, get_basket_price_all, get_delivery, \
    set_new_order, get_orders_tg_id, get_ordersnumber_count_id, get_ordernumber_orders, get_delivery_id, format_number, \
    get_productbrand_product_id
import app.keyboards as kb
from aiogram.types import FSInputFile

from app.setting import SO
from app.states import Order

user = Router()
# user.message.filter(ChatTypeFilter(["group", "supergroup"]))
# user.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))

@user.callback_query(F.data == "start")
@user.message(F.text == "start")
@user.message(CommandStart())
async def cmd_start(data, state: FSMContext):
    await state.clear()
    try:
        if isinstance(data, types.Message):
            message =  data
        elif isinstance(data, types.CallbackQuery):
            message =  data.message
    except Exception as e: pass
    await set_user(message)
    about = await get_about()
    builder = InlineKeyboardBuilder()
    name = kb.name_menu['name_menu']
    phone = kb.name_menu['phone_menu']
    email = kb.name_menu['email_menu']
    logo = FSInputFile("app/img/logo.png")
    if about:
        if about.name:
            name = about.name
        if about.address:
            builder.add(InlineKeyboardButton(text=f'{kb.name_menu['desc_menu']} {kb.name_menu['address_menu']}',
                                             callback_data=f"co_about_address"))
        if about.phone:
            phone = f'☎ {about.phone}'
        if about.email:
            email = f'📩 {about.email}'
        if about.logo:
            logo = about.logo

    cat = await get_cat()
    if cat:
        builder.add(InlineKeyboardButton(text=f'{kb.name_menu['category_menu']} ',
                                         callback_data=f"cocat_0"))
    builder.add(InlineKeyboardButton(text=f'{kb.name_menu['basket_menu']} ',
                                     callback_data=f"basket"))
    builder.add(InlineKeyboardButton(text=f'{kb.name_menu['order_menu']} ',
                                     callback_data=f"ordsus"))

    builder.adjust(2, 2)
    await message.answer_photo(logo)
    await message.answer(f'<b>{name} {phone} {email}</b>',
                               reply_markup=builder.as_markup(), parse_mode='html')
@user.callback_query(F.data=="co_about_address")
async def send_co_about(callback:CallbackQuery):
    about = await get_about()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=f'{kb.name_menu['main_menu']} ',
                                     callback_data=f"start"))
    name = kb.name_menu['name_menu']
    phone = kb.name_menu['phone_menu']
    email = kb.name_menu['email_menu']
    description = kb.name_menu['desc_menu']
    address = kb.name_menu['address_menu']
    photo = kb.name_menu['phone_menu']
    email = kb.name_menu['email_menu']
    logo = FSInputFile("app/img/logo.png")
    map = kb.name_menu['map_menu']
    photo = kb.name_menu['photo_menu']
    text = ""
    if about:
        if about.name:
            name = about.name
            text = f"{text} <b>{name}</b>\n"
        if about.description:
            description = about.description
            text = f"{text} {description}\n"
        if about.address:
            address = about.address
            text = f"{text} {address}\n"
        if about.phone:
            phone = f'☎ {about.phone}'
            text = f"{text} {phone}\n"
        if about.email:
            email = f'📩 {about.email}'
            text = f"{text} {email}\n"
        if about.logo:
            logo = about.logo
        if about.map:
            map = about.map
            builder.add(InlineKeyboardButton(text=f'{kb.name_menu['map_menu']} ',
                                             callback_data=f"co_about_map"))

    builder.adjust(2, 2)
    await callback.message.answer_photo(logo, caption=f'{text}',
                                        reply_markup=builder.as_markup(),
                                        parse_mode='html')


@user.callback_query(F.data == "co_about_map")
async def send_co_about(callback: CallbackQuery):
    about = await get_about()
    if about:
        if about.photo and about.map:
            photo = about.photo
            await callback.message.answer_photo(photo, caption=f'{kb.name_menu['photo_menu']}',
                                                parse_mode='html')
        if about.map:
            map = about.map
            await callback.message.answer_photo(map, caption=f'{kb.name_menu['map_menu']}',
                                                reply_markup=await kb.menu_us(kb.name_menu['main_menu'],
                                                                              "start"),
                                                parse_mode='html')

async def cat_menu_user(category_id, cat_menu_list:list | None = None, cat_menu_str:list | None = None):

    if int(category_id) != 0:

         main_category = await get_category_id(category_id)
         cat_menu_str.insert(0, f"{main_category.name}")
         if main_category.category_id != 0:
             top_main_category = await get_category_id(main_category.category_id)

             cat_menu_list.insert(0,
                         InlineKeyboardButton(text=f"⬆️ {top_main_category.name}",
                                              callback_data=f'cocat_{main_category.category_id}'))
         else:
             cat_menu_str.insert(0, f"📋")
             cat_menu_list.insert(0,
                 InlineKeyboardButton(text=f"⬆️ 📋",
                                      callback_data=f'cocat_0'))
         if main_category.category_id != 0:
            await cat_menu_user(main_category.category_id , cat_menu_list, cat_menu_str)
    return (cat_menu_list, cat_menu_str)
async def cat_menu_start_user(category_id):
    cat_menu_list = []
    cat_menu_str = []
    res = await cat_menu_user(category_id, cat_menu_list, cat_menu_str)
    res_str = ' / '.join(res[1])
    if res_str == '': res_str = kb.name_menu['category_menu']
    return (res[0], res_str)

async def product_menu_user(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    category_id = kwargs['category_id']
    product = await get_products_id(category_id)


    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=kb.name_menu['main_menu'], callback_data="start"))
    category = await get_category_category_id(category_id)
    category = category.all()
    cat_menu_list = await cat_menu_start_user(category_id)

    # builder.row(*cat_menu_list[0])

    for i in cat_menu_list[0]:
        builder.row(i)
    for item in category:
        builder.row(
            InlineKeyboardButton(text=f"⬆️📋 {item.name}  ",
                                callback_data=f"cocat_{item.id}"),
        )
    if product:
        product = product.all()
        for item in product[start:end]:
            builder.row(
                InlineKeyboardButton(text=f"🎁 {item.name} ",
                                    callback_data=f"copro_{item.id}_{category_id}"),
            )
    else:
        return True
    builder.as_markup()
    return (builder, len(product), 'product_menu_user')

@user.callback_query(F.data.startswith("cocat"))
async def send_co_about(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    category_id = int(category_id)
    category = await get_category_id(category_id)
    cat_menu_list = await cat_menu_start_user(category_id)
    if category:
        if category.photo:
            await callback.message.answer_photo(category.photo, caption=f"{cat_menu_list[1]}",
                reply_markup=await get_paginat_kb(fun=product_menu_user, category_id=category_id), )
        else:
            await callback.message.answer(
                text=f"{cat_menu_list[1]}",
                reply_markup=await get_paginat_kb(fun=product_menu_user, category_id=category_id), )
    else:
        await callback.message.answer(
                text= f"{cat_menu_list[1]}",
                reply_markup=await get_paginat_kb(fun=product_menu_user, category_id=category_id),)

async def quantity_basket(user_id, price_id, product_id, category_id, basketact, button_text,
                          price_id_basket, menu_quantity, menu):
    quantity = await set_basket(user_id, price_id, product_id, basketact, price_id_basket)

    button_basket = []#copro
    if menu_quantity == 'copro' or (menu_quantity == 'basket' and quantity != 0):
        button_basket.append(
            InlineKeyboardButton(text=f"➕",
                                 callback_data=f"{menu_quantity}_{product_id}_{category_id}_{price_id}_plus_{price_id}")
        )
        button_basket.append(
            InlineKeyboardButton(text=f"🧺: {quantity}шт {button_text} ",
                                 callback_data=f"{menu}_{product_id}_{category_id}")
        )
        button_basket.append(
            InlineKeyboardButton(text=f"➖",
                                 callback_data=f"{menu_quantity}_{product_id}_{category_id}_{price_id}_minus_{price_id}")
        )
    return button_basket

@user.callback_query(F.data.startswith("copro"))
async def send_co_copro(callback: CallbackQuery):
    product_id = int(callback.data.split('_')[1])
    category_id = int(callback.data.split('_')[2])
    tg_id = callback.message.from_user.id
    user_id = await get_user_tg_id(tg_id)
    user_id = user_id.id
    price_id_basket = ''
    basket = ''
    button_basket =[]
    try:
        price_id = callback.data.split('_')[3]
        basket = callback.data.split('_')[4]
        price_id_basket = callback.data.split('_')[5]
    except Exception as e: pass

    product = await get_product_id(product_id)
    builder = InlineKeyboardBuilder()

    category = await get_category_category_id(category_id)
    category = category.all()
    cat_menu_list = await cat_menu_start_user(category_id)
    catbui = []
    for i in cat_menu_list[0]:
        # builder.row(i)
        catbui.append(i)
    # builder.row(*cat_menu_list[0])
    bui = []
    for item in category:
        bui.append(
            InlineKeyboardButton(text=f"📋 {item.name}  ",
                                callback_data=f"cocat_{item.id}"),
        )
    text = ''
    if product:
        text = '\n'
        brands = await get_productbrand_product_id(product_id)
        for brand in brands:
            text = f"{text} <b><u>{brand.name}</u></b> \n"
        name = product.name
        description = product.description
        text = (f'{text} <b>{name}</b>\n'
                f'{description}\n')
        price = await get_price_product(product_id)
        price = price.all()
        for pr in price:
            button_text = ''
            tprice = await format_number(pr.price)
            if pr.price_discount:
                if pr.price_discount > 0:
                    tprice = f"<s>{await format_number(pr.price)}</s> {await format_number(pr.price_discount)}"
                    button_tprice = pr.price_discount
            text = f"{text} Цена: <b>{tprice} ₽</b> "
            if pr.color:
                text = f"{text} {pr.color} "
                button_text = f"{button_text} {pr.color}"
            if pr.sizes:
                text = f"{text} {pr.sizes} "
                button_text = f"{button_text} {pr.sizes}"
            if pr.quantity:
                text = f"{text} / В наличии: {pr.quantity} шт."
            text = f"{text}\n"
            photo_count = await get_price_photo_count(pr.id)
            if photo_count>0:
                builder.row(InlineKeyboardButton(text=f"{kb.name_menu['photo_menu']} / {button_text} ",
                                                 callback_data=f"cophot_{pr.id}_{product_id}_{category_id}"))
                button_text = ''
            button_basket=(await quantity_basket(user_id, pr.id, product_id, category_id, basket, button_text,
                                                 price_id_basket, 'copro', 'basket'))
            builder.row(*button_basket)

        if product.photo:
            await callback.message.answer_photo(product.photo)

            # if int(category_id) != 0:
            #     category_now = await get_category_id(category_id)
            #     builder.row(InlineKeyboardButton(text=f"⬆️📋 {category_now.name}", callback_data=f"cocat_{category_id}"))
            #
            # await callback.message.answer_photo(product.photo, caption=f"{cat_menu_list[1]} / {product.name}\n",
            #                                                          #  f"{text}"
            #                                     reply_markup=builder.as_markup(), parse_mode='html')
        # else:

        if int(category_id) != 0:
            category_now = await get_category_id(category_id)
            builder.row(InlineKeyboardButton(text=f"⬆️📋 {category_now.name}", callback_data=f"cocat_{category_id}"))

        await callback.message.answer(
            text=f"{cat_menu_list[1]} / {product.name}\n"
                 f"{text}",
            reply_markup=builder.as_markup(), parse_mode='html')
    else:
        builder.row(*button_basket)
        if int(category_id) != 0:
            category_now = await get_category_id(category_id)
            builder.row(InlineKeyboardButton(text=f"⬆️📋 {category_now.name}", callback_data=f"cocat_{category_id}"))

        await callback.message.answer(
            text=f"{cat_menu_list[1]} / {product.name}\n"
                 f"{text}",
            reply_markup=builder.as_markup(), parse_mode='html')


@user.callback_query(F.data.startswith("cophot"))
async def send_co_cophot(callback: CallbackQuery):
    price_id = int(callback.data.split('_')[1])
    product_id = int(callback.data.split('_')[2])
    category_id = int(callback.data.split('_')[3])
    photo = await get_photo_price_id(price_id)
    photo = photo.all()
    media_group = MediaGroupBuilder(caption="Media group caption")
    for ph in photo:
        media_group.add_photo(type="photo", media=ph.photo)
    await callback.message.answer_media_group(media=media_group.build())
    await callback.message.answer("Вернуться к товару:",
                                        reply_markup=await kb.menu_us("⬅️ 🎁",
                                                                      f"copro_{product_id}_{category_id}"),
                                        parse_mode='html')


@user.callback_query(F.data.startswith("basket"))
async def send_basket(callback: CallbackQuery):
    price_id_basket = ''
    basketact = ''
    try:
        basketact = callback.data.split('_')[4]
        price_id_basket = callback.data.split('_')[5]
    except Exception as e: pass
    tg_id = callback.message.from_user.id
    user = await get_user_tg_id(tg_id)
    basket = await get_basket(user.id)
    builder = InlineKeyboardBuilder()

    for bskt in basket.all():
        product = await get_product_id(bskt.product_id)
        price = await get_price_id(bskt.price_id)
        category = await get_category_id(product.category_id)
        # text = f'<b>{product.name}</b>\n'
        button_text = product.name
        # tprice = price.price
        button_tprice = price.price
        if price.price_discount:
            if price.price_discount > 0:
                # tprice = f"<s>{price.price}</s> {price.price_discount}"
                button_tprice = price.price_discount
        button_text = f"{button_text} {button_tprice}₽"
        # text = f'{text} tprice\n'
        if price.color:
            button_text = f"{button_text} {price.color}"
            # text = f"{text} {color.name} "
        if price.sizes:
            button_text = f"{button_text} {price.sizes}"
            # text = f"{text} {sizes.name} "
        button_copro =InlineKeyboardButton(text=f" {button_text} ",
                             callback_data=f"copro_{product.id}_{category.id}")
        button_text = ''
        #  if menu_quantity == 'copro' or (menu_quantity == 'basket' and quantity != 0):
        button_basket = await quantity_basket(user.id, bskt.price_id, bskt.product_id, product.category_id,
                              basketact, button_text, price_id_basket, 'basket', 'copro')

        if len(button_basket)>0: builder.row(button_copro)
        builder.row(*button_basket)

    quantity_all = await get_basket_all(user.id)
    price_all = await get_basket_price_all(user.id)
    if quantity_all>0:
       builder.row(InlineKeyboardButton(text=f'{kb.name_menu['neworder_menu']} ',
                                     callback_data=f"ordus"))
    builder.row(InlineKeyboardButton(text=f'{kb.name_menu['main_menu']} ',
                                     callback_data=f"start"))
    await callback.message.answer(
        text=f"{kb.name_menu['basket_menu']} {quantity_all}шт. {price_all}₽",
        reply_markup=builder.as_markup(), parse_mode='html')

############################################# create new order: ordus

@user.callback_query(F.data.startswith("ordus"))
async def send_ordus(callback: CallbackQuery, state: FSMContext):
    await state.update_data(status='new')
    await state.set_state(Order.status)
    delivery = await get_delivery()
    delivery = delivery.all()
    builder = InlineKeyboardBuilder()
    buttons = []
    for item in delivery:
        buttons.append(InlineKeyboardButton(text=f'{item.name}',
                                      callback_data=f'delivus_{item.id}'))
    builder.row(*buttons)
    builder.adjust(2, 2)
    builder.row(InlineKeyboardButton(text=kb.name_menu['main_menu'], callback_data=f'start'))

    await callback.message.answer(
        text=f"{kb.name_menu['order_menu']} {kb.name_menu['delivery_menu']}",
        reply_markup=builder.as_markup(), parse_mode='html')


@user.callback_query(Order.status, F.data.startswith('delivus_'))
async def send_ordus_new(callback:CallbackQuery, state: FSMContext):
    tg_id = callback.message.from_user.id
    # try:
    delivery_id = callback.data.split('_')[1]
    await set_new_order(tg_id, delivery_id, callback.message)
    text = "Заказ создан!"
    # except Exception as e:
    #     text ="Что-то пошло не так!"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=kb.name_menu['order_menu'],
                                             callback_data=f'ordsus'))
    builder.row(InlineKeyboardButton(text=kb.name_menu['main_menu'],
                                             callback_data=f'start'))
    await state.clear()
    await callback.message.answer(
        text=f"{text}",
        reply_markup=builder.as_markup(), parse_mode='html')
################################################## all ordersbumber ordsus
async def ordsus_menu_user(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    user_id = kwargs['user_id']
    filterorder = kwargs['filterorder']
    # tg_id = kwargs['tg_id']
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=kb.name_menu['main_menu'], callback_data="start"))
    ordernumbers = await get_orders_tg_id(user_id, filterorder)
    ordernumbers = ordernumbers.all()
    buttons = []
    for k, v in SO.items():
        count = await get_ordersnumber_count_id(user_id, k)
        buttons.append(InlineKeyboardButton(text=f'{v}: {count} шт',
                                      callback_data=f'ordsus_{k}'))
    builder.row(*buttons)
    builder.adjust(1, 2)
    for ordernumber in ordernumbers[start:end]:
        builder.row(InlineKeyboardButton(text=f'№ {ordernumber.id} - {SO[ordernumber.status]}',
                                            callback_data=f'ordup_{ordernumber.id}'))
    builder.as_markup()
    return (builder, len(ordernumbers), 'ordsus_menu_user')

@user.callback_query(F.data.startswith('ordsus'))
async def ordsus_all(callback: CallbackQuery):
    tg_id = callback.message.from_user.id
    filterorder = 'all'
    try:
        filterorder = callback.data.split('_')[1]
    except Exception as e:pass
    user = await get_user_tg_id(int(tg_id))
    user_id = user.id
    await callback.message.answer(f'{kb.name_menu["order_menu"]}. Фильтр: {SO[filterorder]}',
                                        reply_markup=await get_paginat_kb(fun=ordsus_menu_user,
                                                                          user_id=user_id,
                                                                          filterorder=filterorder))

@user.callback_query(F.data.startswith('ordup'))
async def ordup(callback: CallbackQuery):
    ordernumber_id = callback.data.split('_')[1]
    text = ''
    builder = InlineKeyboardBuilder()
    ordernumber = await get_ordernumber_orders(ordernumber_id)
    text = f"{text} Статус: <b>{SO[ordernumber.status]}</b>\n"
    text = f"{text} Доставка: {ordernumber.delivery} {ordernumber.delivery_price}₽\n"
    data = ordernumber.date_create
    data = data.strftime("%d.%m.%Y %H:%M")
    text = f"{text} Дата: {data}\n\n"
    n = 1
    summ = float(ordernumber.delivery_price)
    for order in ordernumber.orders:
        text = f"{text} ✅{n}) <b>{order.product}</b>\n"
        text = f"{text} ℹ️{order.color} "
        text = f"{text} /{order.sizes}\n"
        text = f"{text} Цена: <b>{await format_number(order.price)}</b> ₽\n"
        text = f"{text} Количество: {order.quantity}шт.\n\n"
        summ = summ + float(order.price)
        n += 1
    if ordernumber.status == 'verified':
        builder.row(InlineKeyboardButton(text=f"{kb.name_menu['pay_menu']}"
                                              f" {summ} ₽", callback_data="start"))
    builder.row(InlineKeyboardButton(text=f'⬆️{kb.name_menu['order_menu']} ', callback_data=f"ordsus"))
    builder.row(InlineKeyboardButton(text=kb.name_menu['main_menu'], callback_data="start"))

    await callback.message.answer(f'<b>{kb.name_menu['ord_menu']} № {ordernumber_id}</b>\n'
                                  f'{text}'
                                  f'<b>Итого: {await format_number(summ)} ₽</b>',
                                  reply_markup=builder.as_markup(), parse_mode='html')

############################################ s = select([users]).where(users.c.username.ilike('%john%'))



    # orders = await get_orders_tg_id(tg_id)
    # for order in orders:
    #     builder.row(InlineKeyboardButton(text=f'{order[0].id}',
    #                                         callback_data=f'start'))
    # await state.clear()
    # builder.row(InlineKeyboardButton(text=kb.name_menu['main_menu'], callback_data=f'start'))
    # await callback.message.answer(
    #     text=f"{kb.name_menu['order_menu']}",
    #     reply_markup=builder.as_markup(), parse_mode='html')

    # await callback.message.edit_text(
    #     text = f"{cat_menu_list[1]} ",
    #     reply_markup=await get_paginat_kb(fun=category_menu_user, category_id=category_id),
    # )
    # product_slave_count = await get_product_count(category_id)
    # if product_slave_count>0:
    #     await callback.message.answer(
    #         text= f"{kb.name_menu['product_menu']}",
    #         reply_markup=await get_paginat_kb(fun=product_menu_user, category_id=category_id),
    #     )
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