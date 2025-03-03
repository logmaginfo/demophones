# from aiogram import Router, F
# from aiogram.fsm.context import FSMContext
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from app.db.requests import get_users, get_sizes, get_color, del_data, get_brands, get_categorys, \
#     get_delivery, get_product, get_category_id, get_product_cat, get_product_subcat, get_subcategory_id
# from aiogram.types import Message, CallbackQuery
# from app.filter import Admin
# import app.keyboards as kb
# from app.states import Del_item
#
# pagin = Router()
# pagin.message.filter(Admin())
#
#
# async def get_paginated_kb(page: int = 0,  pages:int = 5, switch:str = 'users', subcat:int=0, catprod:int = 0, subcatprod:int = 0) -> InlineKeyboardMarkup:
#
#
#     builder = InlineKeyboardBuilder()
#     page = int(page)
#     builder.row(InlineKeyboardButton(text='⬆️ Главное меню', callback_data='admin'))
#     if switch == 'subcategory' or (switch == 'product' and catprod != 0):
#         builder.row(InlineKeyboardButton(text='⬆️📋 Категории', callback_data='category'))
#     if switch == 'product' and subcatprod != 0:
#         builder.row(InlineKeyboardButton(text='⬆️📋 ПодКатегория', callback_data=f'subcategory_{subcatprod}'))
#         subcat = subcatprod
#     builder.add(InlineKeyboardButton(text=f'➕ Добавить {switch}', callback_data=f'add_{switch}_{subcat}_{catprod}_{subcatprod}'))
#     start_offset:int = page * pages
#     end_offset:int = start_offset + pages
#     if switch == 'users':
#         items = await get_users()
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             builder.row(
#                 InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.tg_id)}",
#                                      callback_data=f"up_{switch}_{item.id}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#             )
#
#     elif switch == 'sizes':
#         items = await get_sizes()
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             builder.row(
#                 InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.name)}",
#                                      callback_data=f"upsizes_{switch}_{item.id}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#             )
#
#     elif switch == 'brand':
#         items = await get_brands()
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             builder.row(
#                 InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.name)}",
#                                      callback_data=f"upbrand_{switch}_{item.id}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#             )
#
#     elif switch == 'category':
#         items = await get_categorys()
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             sub_cat_len = await get_sub_can_len(item.id)
#             sub_cat_len = len(sub_cat_len.all())
#             builder.row(
#                 InlineKeyboardButton(text=f"{str(item.sort)} (🆔 {str(item.id)}) {str(item.name)}",
#                                      callback_data=f"upcategory_{switch}_{item.id}"))
#             builder.row(
#                 # InlineKeyboardButton(text=f"➕🎁 Тов", callback_data=f"add_product_{item.id}_0"),
#                 InlineKeyboardButton(text=f"🎁 Все Тов", callback_data=f"product_{item.id}_0_{subcat}"),
#                 InlineKeyboardButton(text=f"📋 Все ПодКат({sub_cat_len})", callback_data=f"subcategory_{item.id}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#                 # InlineKeyboardButton(text=f"➕📋 ПодКат", callback_data=f"add_subcategory_{item.id}", ),
#             )
#
#
#     elif switch == 'subcategory':
#         # items = await get_subcategory()
#         items = await get_sub_can_len(int(subcat))
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             builder.row(
#                 InlineKeyboardButton(text=f"{item.sort} (🆔 {str(item.id)}  ) {str(item.name)}",
#                                      callback_data=f"upsubcategory_{switch}_{item.id}"),
#                 InlineKeyboardButton(text=f"🎁 Все Тов", callback_data=f"product_0_{item.id}_{subcat}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#             )
#
#     elif switch == 'color':
#         items = await get_color()
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             photo=''
#             if item.photo!=None:
#                 photo = '🖼'
#             builder.row(
#                 InlineKeyboardButton(text=f"(🆔 {str(item.id)}) {str(item.name)} {photo}",
#                                      callback_data=f"upcolor_{switch}_{item.id}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#             )
#     elif switch == 'delivery':
#         items = await get_delivery()
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             builder.row(
#                 InlineKeyboardButton(text=f"{str(item.sort)} (🆔 {str(item.id)}) {str(item.name)} ",
#                                      callback_data=f"updelivery_{switch}_{item.id}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#             )
#
#     elif switch == 'product':
#         if catprod != 0:
#             items = await get_product_cat(int(catprod))
#         elif subcatprod != 0:
#             items = await get_product_subcat(int(subcatprod))
#         else:
#             items = await get_product()
#         items = items.all()
#         for item in items[start_offset:end_offset]:
#             builder.row(
#                 InlineKeyboardButton(text=f"{str(item.sort)} (🆔 {str(item.id)}) {str(item.name)} ",
#                                      callback_data=f"upproduct_{switch}_{item.id}_{catprod}_{subcatprod}"),
#                 InlineKeyboardButton(text="❌", callback_data=f"del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}")
#             )
#
#     len_item = len(items)
#     buttons_row = []
#     if page > 0:
#         buttons_row.append(
#             InlineKeyboardButton(
#                 text="⬅️",
#                 callback_data=f"pag_{(page - 1)}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}",
#             )
#         )
#     if end_offset < len_item:
#         buttons_row.append(
#             InlineKeyboardButton(
#                 text="➡️",
#                 callback_data=f"pag_{(page + 1)}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}",
#             )
#         )
#
#     builder.row(*buttons_row)
#     return builder.as_markup()
# #
# # @pagin.callback_query(F.data.startswith("users"))
# # async def send_users_handler(callback:CallbackQuery):
# #     await callback.message.edit_text(
# #         text="👨‍👩‍👦 Пользователи",
# #         reply_markup=await get_paginated_kb(pages=3, switch="users"),
# #     )
#
# # @pagin.callback_query(F.data.startswith("sizes"))
# # async def send_sizes_handler(callback:CallbackQuery):
# #     await callback.message.edit_text(
# #         text="📶 Размеры",
# #         reply_markup=await get_paginated_kb(pages=10, switch="sizes"),
# #     )
#
# # @pagin.callback_query(F.data.startswith("brand"))
# # async def send_brand_handler(callback:CallbackQuery):
# #     await callback.message.edit_text(
# #         text="©️ Бренд",
# #         reply_markup=await get_paginated_kb(pages=10, switch="brand"),
# #     )
#
# #
# #
# # @pagin.callback_query(F.data.startswith("subcategory"))
# # async def send_subcategory_handler(callback:CallbackQuery):
# #     subcat = callback.data.split('_')[1]
# #     category = await get_category_id(int(subcat))
# #     await callback.message.edit_text(
# #         text=f"📋 {category.name} / ПодКатегории:",
# #         reply_markup=await get_paginated_kb(pages=10, switch="subcategory", subcat=int(subcat)), parse_mode='html'
# #     )
#
# # @pagin.callback_query(F.data.startswith("color"))
# # async def send_color_handler(callback:CallbackQuery):
# #     await callback.message.edit_text(
# #         text="🔵 Цвета",
# #         reply_markup=await get_paginated_kb(pages=12, switch="color"),
# #     )
#
# #
# # @pagin.callback_query(F.data.startswith("delivery"))
# # async def send_color_handler(callback:CallbackQuery):
# #     await callback.message.edit_text(
# #         text="🚚 Доставка",
# #         reply_markup=await get_paginated_kb(pages=10, switch="delivery"),
# #     )
#
# @pagin.callback_query(F.data.startswith("product"))
# async def send_color_handler(callback: CallbackQuery):
#
#     catprod = callback.data.split('_')[1]
#     subcatprod = callback.data.split('_')[2]
#     subcat = callback.data.split('_')[3]
#     cat = ''
#     if catprod != '0':
#         catprod_name = await get_category_id(int(catprod))
#         cat = catprod_name.name
#     if subcatprod != '0':
#         subcatprod_name = await get_subcategory_id(int(subcatprod))
#         cat = subcatprod_name.name
#     await callback.message.edit_text(
#         text=f"{cat} / 🎁 Товары",
#         reply_markup=await get_paginated_kb(pages=10, switch="product", subcat=int(subcat), catprod=int(catprod), subcatprod=int(subcatprod))
#     )
#
# @pagin.callback_query(F.data.startswith('pag_'))
# async def products_pagination_callback(callback: CallbackQuery):
#     page = callback.data.split('_')[1]
#     switch = callback.data.split('_')[2]
#     subcat = callback.data.split('_')[3]
#     pages = callback.data.split('_')[4]
#     catprod = callback.data.split('_')[5]
#     subcatprod = callback.data.split('_')[6]
# #_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}
#     await callback.message.edit_reply_markup(
#     reply_markup=await get_paginated_kb(page=int(page), subcat=int(subcat), pages=int(pages), switch=switch
#                                         , catprod=int(catprod), subcatprod=int(subcatprod))
# )
#
#     #del_{item.id}_{switch}
# # @pagin.callback_query(F.data.startswith('del_'))
# # async def del_item(callback: CallbackQuery, state: FSMContext):
# #     await state.set_state(Del_item.del_item)
# #     id = callback.data.split('_')[1]
# #     switch = callback.data.split('_')[2]
# #     subcat = callback.data.split('_')[3]
# #     pages = callback.data.split('_')[4]
# #     catprod = callback.data.split('_')[5]
# #     subcatprod = callback.data.split('_')[6]
# #     #del_{item.id}_{switch}_{subcat}_{pages}_{catprod}_{subcatprod}
# #     await state.update_data(del_id=id)
# #     await state.update_data(switch=switch)
# #     await state.update_data(subcat=subcat)
# #     await state.update_data(pages=pages)
# #     await state.update_data(catprod=catprod)
# #     await state.update_data(subcatprod=subcatprod)
# #     await callback.message.answer(f'Введите "Y", если хотите удалить (🆔 {id})!',
# #     reply_markup=kb.cancel)
#
# # @pagin.message(Del_item.del_item, F.text == 'Y')
# # async def del_item_y(message: Message, state: FSMContext):
# #     data = await state.get_data()
# #     text = await del_data(data)
# #     await message.answer(text,
# #                          reply_markup=await get_paginated_kb(subcat=int(data['subcat']),
# #                                                              pages=int(data['pages']), switch=data['switch']
# #                                         , catprod=int(data['catprod']), subcatprod=int(data['subcatprod'])))
# #     await state.clear()
# #
# # @pagin.message(Del_item.del_item)
# # async def del_item_y(message: Message, state: FSMContext):
# #     await message.answer('❌ Отменено!', reply_markup=kb.main)
# #     await state.clear()
