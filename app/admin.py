from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.cmd.paginator import get_paginat_kb
from app.db.requests import get_users, del_data, get_brands, get_sizes, get_color, get_delivery, get_categorys, \
    get_subcategory, get_subcategory_category_id, get_category_id
from app.filter import ChatTypeFilter, IsAdmin
from aiogram.filters import Command, Filter
from app.filter import Admin
import app.keyboards as kb
from app.setting import pageCD
from app.states import Del_item

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
                                 callback_data=f"del_{item.id}_users")

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
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.name)}",
                                     callback_data=f"upbrand_brad_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_brand")

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
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.name)}",
                                     callback_data=f"upsizes_sizes_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_sizes")

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
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.name)} {photo}",
                                     callback_data=f"upcolor_color_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_color")

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
            InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.name)} ",
                                     callback_data=f"updelivery_delivery_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_delivery")

        )
    return (builder, len(delivery), 'delivery_menu')
@admin.callback_query(F.data.startswith("delivery"))
async def send_delivery_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text=kb.name_menu['delivery_menu'],
        reply_markup=await get_paginat_kb(fun=delivery_menu),
    )

############################################# category_menu
async def category_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    # funs_dic['sizes_menu'] = sizes_menu
    builder = InlineKeyboardBuilder()
    category = await get_categorys()
    category = category.all()

    builder.row(kb.main_menu)
    builder.row(await kb.add_item('category', f"➕ {kb.name_menu['category_menu']}"))
    # builder.row(await kb.add_item('subcategory', f"{kb.name_menu['subcategory_menu']}"))
    for item in category[start:end]:
        photo = ''
        if item.photo != None:
            photo = '🖼'
        builder.row(
            InlineKeyboardButton(text=f"{str(item.sort)}) (🆔 {str(item.id)}) {str(item.name)} {photo}",
                                     callback_data=f"upcategory_category_{item.id}"),
            InlineKeyboardButton(text=kb.name_menu['subcategory_menu'],
                             callback_data=f"subcategory_{item.id}"),
            InlineKeyboardButton(text=kb.name_menu['product_menu'],
                                 callback_data=f"subcategory_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_category")

        )
    return (builder, len(category), 'category_menu')
@admin.callback_query(F.data.startswith("category"))
async def send_category_handler(callback:CallbackQuery):
    await callback.message.edit_text(
        text=kb.name_menu['category_menu'],
        reply_markup=await get_paginat_kb(fun=category_menu),
    )
############################################# subcategory_menu
async def subcategory_menu(**kwargs):
    start = kwargs['start']
    end = kwargs['end']
    category_id = kwargs['category_id']

    builder = InlineKeyboardBuilder()
    subcategory = await get_subcategory_category_id(category_id)
    subcategory = subcategory.all()

    builder.row(kb.main_menu)
    builder.row(await kb.menu_item( f"⬆️ {kb.name_menu['category_menu']}", 'category'))
    builder.row(await kb.add_item(f'subcategory_{category_id}', f"➕ {kb.name_menu['subcategory_menu']}"))
    # builder.row(await kb.add_item('subcategory', f"{kb.name_menu['subcategory_menu']}"))
    for item in subcategory[start:end]:
        photo = ''
        if item.photo != None:
            photo = '🖼'
        builder.row(
            InlineKeyboardButton(text=f"{str(item.sort)}) (🆔 {str(item.id)}) {str(item.name)} {photo}",
                                callback_data=f"upsubcategory_subcategory_{item.id}"),
            InlineKeyboardButton(text=kb.name_menu['product_menu'],
                                 callback_data=f"subcategory_{item.id}"),
            InlineKeyboardButton(text="🗑",
                                 callback_data=f"del_{item.id}_subcategory")

        )
    return (builder, len(subcategory), 'subcategory_menu')
@admin.callback_query(F.data.startswith("subcategory"))
async def send_subcategory_handler(callback:CallbackQuery):
    category_id = callback.data.split('_')[1]
    category_name = await get_category_id(category_id)
    await callback.message.edit_text(
        text=f'{kb.name_menu['subcategory_menu']} / {category_name.name}',
        reply_markup=await get_paginat_kb(fun=subcategory_menu, category_id=category_id),
    )

############################################# del
@admin.callback_query(F.data.startswith('del_'))
async def del_item(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Del_item.del_item)
    id = callback.data.split('_')[1]
    switch = callback.data.split('_')[2]
    await state.update_data(del_id=id)
    await state.update_data(switch=switch)
    await callback.message.answer(f'Нажмите "DEL", если хотите удалить 🆔 {id}',
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
################################################

@admin.callback_query(pageCD.filter())
async def products_pagination_callback(callback: CallbackQuery, callback_data: pageCD):
    page = callback_data.page
    pages = callback_data.pages
    fun = funs_dic[callback_data.fun]
    await callback.message.edit_reply_markup(
    reply_markup=await get_paginat_kb(page=page, pages=pages, fun=fun)
)

@admin.callback_query(F.data == "ok_page")
async def process_callback(callback_query: CallbackQuery):
    await callback_query.message.bot.answer_callback_query(callback_query.id, text="Страница уже открыта", show_alert=False)


funs_dic={'brand_menu':brand_menu,'sizes_menu':sizes_menu, 'users_menu':users_menu,
          'color_menu':color_menu, 'delivery_menu':delivery_menu, 'category_menu':category_menu,
          'subcategory_menu':subcategory_menu}







