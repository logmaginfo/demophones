from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_users, del_data, get_brands, get_sizes, get_color, get_delivery, get_categorys, \
    get_category_id, get_category_category_id, get_category_subcat_count, get_product, get_product_count, \
    get_product_category_id, get_product_brand_count, get_price_product, get_product_id, get_product_price_count, \
    get_price_id, get_photo_price, poto_join, del_item2, get_price_photo_count, get_orders_tg_id_admin, \
    get_ordersnumber_count_id_admin
from app.filter import ChatTypeFilter, IsAdmin
from aiogram.filters import Command, Filter
from app.filter import Admin
import app.keyboards as kb
from app.setting import pageCD, SO
from app.states import Del_item, DelPhoto, ProductSearch
from app.user import product_menu_user, ordsus_menu_user

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

############################################# users_menu
async def users_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    # funs_dic['users_menu'] = users_menu
    builder = InlineKeyboardBuilder()
    users = await get_users()
    users = users.all()

    builder.row(kb.main_menu)
    builder.row(await kb.add_item('users', f"➕ {kb.name_menu['users_menu']}"))
    for item in users[start:end]:
        if item.name != None: name = str(item.name)
        else: name = ''
        builder.row(
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.tg_id)} {name}",
                                     callback_data=f"up_users_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_users_{name}")

        )
    return (builder, len(users), 'users_menu')
@admin.callback_query(F.data.startswith("users"))
async def send_users_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text=kb.name_menu['users_menu'],
        reply_markup=await get_paginat_kb(fun=users_menu),
    )
############################################# brand_menu
async def brand_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    # funs_dic['brand_menu'] = brand_menu
    builder = InlineKeyboardBuilder()
    brands = await get_brands()
    brands = brands.all()

    builder.row(kb.main_menu)
    builder.row(await kb.add_item('brand', f"➕ {kb.name_menu['brand_menu']}"))
    for item in brands[start:end]:
        builder.row(
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {item.name}",
                                     callback_data=f"upbrand_brad_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_brand_{item.name}")

        )
    return (builder, len(brands), 'brand_menu')
@admin.callback_query(F.data.startswith("brand"))
async def send_brand_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text=kb.name_menu['brand_menu'],
        reply_markup=await get_paginat_kb(fun=brand_menu),
    )
############################################# sizes_menu
async def sizes_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    # funs_dic['sizes_menu'] = sizes_menu
    builder = InlineKeyboardBuilder()
    sizes = await get_sizes()
    sizes = sizes.all()

    builder.row(kb.main_menu)
    builder.row(await kb.add_item('sizes', f"➕ {kb.name_menu['sizes_menu']}"))
    for item in sizes[start:end]:
        builder.row(
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {item.name}",
                                     callback_data=f"upsizes_sizes_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_sizes_{item.name}")

        )
    return (builder, len(sizes), 'sizes_menu')
@admin.callback_query(F.data.startswith("sizes"))
async def send_sizes_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text=kb.name_menu['sizes_menu'],
        reply_markup=await get_paginat_kb(fun=sizes_menu),
    )

############################################# color_menu
async def color_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    # funs_dic['sizes_menu'] = sizes_menu
    builder = InlineKeyboardBuilder()
    color = await get_color()
    color = color.all()

    builder.row(kb.main_menu)
    builder.row(await kb.add_item('color', f"➕ {kb.name_menu['color_menu']}"))
    for item in color[start:end]:
        photo = ''
        if item.photo != None:
            photo = '🖼'
        builder.row(
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {item.name} {photo}",
                                     callback_data=f"upcolor_color_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_color_{item.name}")

        )
    return (builder, len(color), 'color_menu')
@admin.callback_query(F.data.startswith("color"))
async def send_color_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text=kb.name_menu['color_menu'],
        reply_markup=await get_paginat_kb(fun=color_menu),
    )
############################################# delivery_menu
async def delivery_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    # funs_dic['sizes_menu'] = sizes_menu
    builder = InlineKeyboardBuilder()
    delivery = await get_delivery()
    delivery = delivery.all()

    builder.row(kb.main_menu)
    builder.row(await kb.add_item('delivery', f"➕ {kb.name_menu['delivery_menu']}"))
    for item in delivery[start:end]:
        builder.row(
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {item.name} ",
                                     callback_data=f"updelivery_delivery_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_delivery_{item.name}")

        )
    return (builder, len(delivery), 'delivery_menu')
@admin.callback_query(F.data.startswith("delivery"))
async def send_delivery_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text=kb.name_menu['delivery_menu'],
        reply_markup=await get_paginat_kb(fun=delivery_menu),
    )

############################################# category_menu
async def cat_menu(category_id, cat_menu_list:list | None = None, cat_menu_str:list | None = None):

    if int(category_id) != 0:
         main_category = await get_category_id(category_id)
         cat_menu_str.insert(0, f"{main_category.name}")
         if main_category.category_id != 0:
             top_main_category = await get_category_id(main_category.category_id)

             cat_menu_list.insert(0,
                         InlineKeyboardButton(text=f"⬆️ {top_main_category.name}",
                                              callback_data=f'category_{main_category.category_id}'))
         else:
             cat_menu_str.insert(0, f"📋")
             cat_menu_list.insert(0,
                 InlineKeyboardButton(text=f"⬆️ 📋",
                                      callback_data=f'category_0'))
         if main_category.category_id != 0:
            await cat_menu(main_category.category_id , cat_menu_list, cat_menu_str)
    return (cat_menu_list, cat_menu_str)
async def cat_menu_start(category_id):
    cat_menu_list = []
    cat_menu_str = []
    res = await cat_menu(category_id, cat_menu_list, cat_menu_str)
    res_str = ' / '.join(res[1])
    if res_str == '': res_str = kb.name_menu['category_menu']
    return (res[0], res_str)

async def category_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    category_id = kwargs['category_id']

    builder = InlineKeyboardBuilder()
    category = await get_category_category_id(category_id)
    category = category.all()
    builder.row(kb.main_menu)
    cat_menu_list = await cat_menu_start(category_id)
    for i in cat_menu_list[0]:
        builder.row(i)

    builder.row(await kb.add_item(f'category_{category_id}', f"➕ Категория"))
    for item in category[start:end]:
        category_slave_count = await get_category_subcat_count(item.id)
        product_slave_count = await get_product_count(item.id)
        if category_slave_count == 0 and product_slave_count == 0:
           inDel = InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_category_{item.name}")
        else:
            inDel = InlineKeyboardButton(text="🚯",
                                         callback_data=f"delNOT")
        photo = ''
        if item.photo != None:
            photo = '🖼'
        builder.row(
            InlineKeyboardButton(text=f"{str(item.sort)}. (🆔 {str(item.id)}) {item.name} {photo}",
                                callback_data=f"upcategory_category_{item.id}"),
            InlineKeyboardButton(text=f"({product_slave_count}) {kb.name_menu['product_menu']}",
                                 callback_data=f"product_{item.id}"),
        )
        builder.row(
            InlineKeyboardButton(text=f"↳ ({category_slave_count}) {kb.name_menu['subcategory_menu']}",
                                callback_data=f"category_{item.id}", parse_mode='html'),
            inDel
        )
        builder.as_markup()
    return (builder, len(category), 'category_menu')
@admin.callback_query(F.data.startswith("category"))
async def send_category_handler(callback:CallbackQuery):
    category_id = callback.data.split('_')[1]
    category_id = int(category_id)
    cat_menu_list = await cat_menu_start(category_id)
    await callback.message.edit_text(
        text= f"{cat_menu_list[1]} ",
        reply_markup=await get_paginat_kb(fun=category_menu, category_id=category_id),
    )
############################################# product_menu
async def product_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    category_id = kwargs['category_id']
    builder = InlineKeyboardBuilder()
    product = await get_product_category_id(category_id)
    product = product.all()

    builder.row(kb.main_menu)
    cat_menu_list = await cat_menu_start(category_id)
    for i in cat_menu_list[0]:
        builder.row(i)
    builder.row(await kb.add_item(f'product_{category_id}', f"➕ {kb.name_menu['product_menu']}"))
    for item in product[start:end]:
        photo = ''
        if item.photo != None:
            photo = '🖼'
        brand_count = await get_product_brand_count(item.id)
        price_count = await get_product_price_count(item.id)
        if price_count == 0 and brand_count == 0:
           inDel = InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_product_{item.name}")
        else:
            inDel = InlineKeyboardButton(text="🚯",
                                         callback_data=f"delNOT")
        builder.row(
            InlineKeyboardButton(text=f"{item.sort}. (🆔 {str(item.id)}) {item.name} {photo}",
                                     callback_data=f"upproduct_product_{item.id}"),
            InlineKeyboardButton(text=f"({price_count}) {kb.name_menu['price_menu']}",
                                 callback_data=f"price_{item.id}_{category_id}"),
        )
        builder.row(
            InlineKeyboardButton(text=f"({brand_count}) {kb.name_menu['brand_menu']}",
                                 callback_data=f"prbr_{item.id}_{category_id}"),
            inDel,
        )
    return (builder, len(product), 'product_menu')
@admin.callback_query(F.data.startswith("product"))

async def send_product_handler(callback:CallbackQuery):

    category_id = callback.data.split('_')[1]
    category_id = int(category_id)
    cat_menu_list = await cat_menu_start(category_id)
    await callback.message.edit_text(
        text=f"🎁 {cat_menu_list[1]}",
        reply_markup=await get_paginat_kb(fun=product_menu, category_id=category_id),
    )
############################################# price_menu
async def price_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    category_id = kwargs['category_id']
    product_id = kwargs['product_id']
    builder = InlineKeyboardBuilder()
    price = await get_price_product(product_id)
    product = await get_product_id(product_id)
    price = price.all()


    builder.row(kb.main_menu)
    cat_menu_list = await cat_menu_start(category_id)
    for i in cat_menu_list[0]:
        builder.row(i)
    builder.row(InlineKeyboardButton(text=f'⬆️ 🎁 ', callback_data=f'product_{category_id}'))
    builder.row(await kb.add_item(f'price_{product_id}_{category_id}', f"➕ {kb.name_menu['price_menu']}"))
    for item in price[start:end]:
        photo_count = await get_price_photo_count(item.id)
        if photo_count == 0:
            inDel = InlineKeyboardButton(text=f"🗑",
                                 callback_data=f"dph_{item.id}_price_{product_id}_{category_id}"
                                               # f"dpr_{item.id}_price_{item.name}_{product_id}_{category_id}"
                                               f"")
        else:
            inDel = InlineKeyboardButton(text="🚯",
                                         callback_data=f"delNOT")
        builder.row(
            InlineKeyboardButton(text=f" (🆔 {str(item.id)}) {item.name}",
                                     callback_data=f"upprice_price_{item.id}_{product_id}_{category_id}"),
            InlineKeyboardButton(text=f"({photo_count}){kb.name_menu['photo_menu']}",
                                 callback_data=f"photo_{item.id}_{product_id}_{category_id}"),
            inDel
            #callback_data=f"dph_{item.id}_photo_{price_id}_{product_id}_{category_id}")
        )
    return (builder, len(price), 'price_menu')
@admin.callback_query(F.data.startswith("price"))
async def send_price_handler(callback:CallbackQuery):
    product_id = callback.data.split('_')[1]
    category_id = callback.data.split('_')[2]
    product = await get_product_id(product_id)
    cat_menu_list = await cat_menu_start(category_id)
    await callback.message.edit_text(
        text=f"💰 {cat_menu_list[1]} {product.name}",
        reply_markup=await get_paginat_kb(fun=price_menu, category_id=category_id, product_id=product_id),
    )
############################################# photo
async def photo_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    category_id = kwargs['category_id']
    product_id = kwargs['product_id']
    price_id = kwargs['price_id']
    builder = InlineKeyboardBuilder()
    photo = await get_photo_price(price_id)
    # product = await get_product_id(product_id)
    photo = photo.all()


    builder.row(kb.main_menu)
    cat_menu_list = await cat_menu_start(category_id)
    for i in cat_menu_list[0]:
        builder.row(i)
    builder.row(InlineKeyboardButton(text=f'⬆️ 🎁 ', callback_data=f'product_{category_id}'))
    builder.row(InlineKeyboardButton(text=f'⬆️ 💰 ', callback_data=f'price_{product_id}_{category_id}'))
    builder.row(await kb.add_item(f'photo_{price_id}_{product_id}_{category_id}', f"➕ {kb.name_menu['photo_menu']}"))
    for item in photo[start:end]:
        builder.row(
            InlineKeyboardButton(text=f"{item.sort}. (🆔 {str(item.id)})",
                                     callback_data=f"upphoto_{item.id}_{price_id}_{product_id}_{category_id}"),
            InlineKeyboardButton(text=f"🗑",
                                 callback_data=f"dph_{item.id}_photo_{price_id}_{product_id}_{category_id}")
        )
    return (builder, len(photo), 'photo_menu')
@admin.callback_query(F.data.startswith("photo"))
async def send_photo_handler(callback:CallbackQuery):
    price_id = callback.data.split('_')[1]
    product_id = callback.data.split('_')[2]
    category_id = callback.data.split('_')[3]
    p = await poto_join(price_id)
    price = p[0]
    product = p[1]
    cat_menu_list = await cat_menu_start(category_id)
    await callback.message.answer(
        text=f"💰 {cat_menu_list[1]} 🎁{product.name} 💰{price.name}",
        reply_markup=await get_paginat_kb(fun=photo_menu, category_id=category_id, product_id=product_id, price_id=price_id),
    )
############################################# ordernumber
async def ordsus_menu_admin(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    filterorder = kwargs['filterorder']
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=kb.name_menu['main_menu'], callback_data="admin"))
    ordernumbers = await get_orders_tg_id_admin(filterorder)
    ordernumbers = ordernumbers.all()
    buttons = []
    for k, v in SO.items():
        count = await get_ordersnumber_count_id_admin(k)
        buttons.append(InlineKeyboardButton(text=f'{v}: {count} шт',
                                      callback_data=f'ordernumber_{k}'))
    builder.row(*buttons)
    builder.adjust(1, 2)
    for ordernumber in ordernumbers[start:end]:
        builder.row(InlineKeyboardButton(text=f'№ {ordernumber.id} - {SO[ordernumber.status]}',
                                            callback_data=f'ordup_{ordernumber.id}'))
    builder.as_markup()
    return (builder, len(ordernumbers), 'ordsus_menu_admin')
@admin.callback_query(F.data.startswith("ordernumber"))
async def ordernumber_handler_all(callback:CallbackQuery):
    filterorder = 'all'
    try:
        filterorder = callback.data.split('_')[1]
    except Exception as e:pass
    await callback.message.answer(f'admin {kb.name_menu["order_menu"]}. Фильтр: {SO[filterorder]}',
                                        reply_markup=await get_paginat_kb(fun=ordsus_menu_admin,
                                                                          filterorder=filterorder))

############################################# del
@admin.callback_query(F.data.startswith('del_'))
async def del_item(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Del_item.del_item)
    id = callback.data.split('_')[1]
    switch = callback.data.split('_')[2]
    text = callback.data.split('_')[3]
    await state.update_data(del_id=id)
    await state.update_data(switch=switch)
    await callback.message.answer(f'Нажмите "DEL", если хотите удалить 🆔 {id} {text}',
    reply_markup=kb.del_yes_no)


@admin.callback_query(Del_item.del_item, F.data == 'clear_msg')
async def del_item_no(callback: CallbackQuery, state: FSMContext):
    # await callback.message.message.reply_to_message.delete(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.bot.answer_callback_query(callback.id, text="Отмена 🙅🏻", show_alert=False)
    await callback.message.delete()
    await state.clear()


@admin.callback_query(Del_item.del_item, F.data == 'Y')
async def del_item_y(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    del_answeer = await del_data(data)
    del_flag = del_answeer[0]
    text = del_answeer[1]
    switch = del_answeer[2]
    key = switch + '_menu'
    fun = funs_dic[key]
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await callback.message.edit_text(kb.name_menu[key], reply_markup=await get_paginat_kb(fun=fun))
    await state.clear()
################################################ delfoto
@admin.callback_query(F.data.startswith('dph_'))
async def delfoto(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DelPhoto.del_item)
    id = callback.data.split('_')[1]
    table = callback.data.split('_')[2]
    if table == 'photo':
       price_id = callback.data.split('_')[3]
       await state.update_data(price_id=price_id)
       product_id = callback.data.split('_')[4]
       category_id = callback.data.split('_')[5]
    if table == 'price':
        product_id = callback.data.split('_')[3]
        category_id = callback.data.split('_')[4]
    await state.update_data(del_id=id)
    await state.update_data(table=table)
    await state.update_data(product_id=product_id)
    await state.update_data(category_id=category_id)
    await callback.message.answer(f'Нажмите "DEL", если хотите удалить 🆔 {id}',
    reply_markup=kb.del_yes_no)

@admin.callback_query(DelPhoto.del_item, F.data == 'clear_msg')
async def del_item_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.bot.answer_callback_query(callback.id, text="Отмена 🙅🏻", show_alert=False)
    await callback.message.delete()
    await state.clear()

@admin.callback_query(DelPhoto.del_item, F.data == 'Y')
async def delfoto_y(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    del_answeer = await del_item2(data)
    key = data['table'] + '_menu'
    fun = funs_dic[key]
    await callback.message.bot.answer_callback_query(callback.id, text=del_answeer, show_alert=False)
    if data['table'] == 'photo':
        await callback.message.edit_text(kb.name_menu[key],
                                         reply_markup=await get_paginat_kb(fun=fun,
                                                                           category_id=data['category_id'],
                                                                           product_id=data['product_id'],
                                                                           price_id=data['price_id']
                                                                           ))
    if data['table'] == 'price':
        await callback.message.edit_text(kb.name_menu[key],
                                         reply_markup=await get_paginat_kb(fun=fun,
                                                                           category_id=data['category_id'],
                                                                           product_id=data['product_id'],
                                                                           ))
    await state.clear()


@admin.callback_query(Del_item.del_item, F.data == 'Y')
async def del_item_y(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    del_answeer = await del_data(data)
    del_flag = del_answeer[0]
    text = del_answeer[1]
    switch = del_answeer[2]
    key = switch + '_menu'
    fun = funs_dic[key]
    await callback.message.bot.answer_callback_query(callback.id, text=text, show_alert=False)
    await callback.message.edit_text(kb.name_menu[key], reply_markup=await get_paginat_kb(fun=fun))
    await state.clear()

@admin.callback_query(pageCD.filter())
async def products_pagination_callback(callback: CallbackQuery, callback_data: pageCD):
    page = callback_data.page
    pages = callback_data.pages
    fun = funs_dic[callback_data.fun]
    category_id = callback_data.category_id
    product_id = callback_data.product_id
    price_id = callback_data.price_id
    user_id = callback_data.user_id
    filterorder = callback_data.filterorder
    await callback.message.edit_reply_markup(
    reply_markup=await get_paginat_kb(page=page, pages=pages, fun=fun, category_id=category_id,
                                      product_id=product_id, price_id=price_id, user_id=user_id,
                                      filterorder=filterorder)
)

@admin.callback_query(F.data == "ok_page")
async def process_callback(callback_query: CallbackQuery):
    await callback_query.message.bot.answer_callback_query(callback_query.id, text="Страница уже открыта", show_alert=False)


@admin.callback_query(F.data == "delNOT")
async def process_callback(callback_query: CallbackQuery):
    await callback_query.message.bot.answer_callback_query(callback_query.id, text=kb.name_menu['connect_menu'],
                                                           show_alert=True)

funs_dic={'brand_menu':brand_menu,'sizes_menu':sizes_menu, 'users_menu':users_menu,
          'color_menu':color_menu, 'delivery_menu':delivery_menu, 'category_menu':category_menu,
          'product_menu':product_menu, 'price_menu':price_menu, 'photo_menu':photo_menu,
          'product_menu_user':product_menu_user, "ordsus_menu_user":ordsus_menu_user,
          'ordsus_menu_admin':ordsus_menu_admin,
          }







