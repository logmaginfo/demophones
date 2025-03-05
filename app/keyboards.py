from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from app.db.requests import get_categorys, get_brands
name_menu ={
            'main_menu':'⬆️ Главное меню',
            'users_menu':'👨‍👩‍👦 Пользователи',
            'brand_menu':'📌 Теги',
            'sizes_menu':'📶 Размеры',
            'color_menu':'🔵 Цвета',
            'delivery_menu':'🚚 Доставки',
            'category_menu':'📋 Категории',
            'subcategory_menu':'📋 ПодКатегории',
            'product_menu':'🎁 Товары',
            'price_menu':'💰 Прайсы',
            'photo_menu':'📸 Фото',
            'cancel':'🙅🏻 Отмена',
            'sort_menu':'🔢 Сортировка',
            'connect_menu':'❗️Не удалено. Есть зависимости 🔀',
            'delete_menu':'❌ Удалено!',
            'recordNo_menu':'❌ Такая запись уже есть',
            'recordAdd_menu':'👌 Данные добавлены',
            'recordUp_menu':'👌 Данные обновлены',
            'about_menu':'☎️ О нас',
            'next_menu':'⏩ Пропустить'
            }


main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name_menu['users_menu'], callback_data='users')],
        [InlineKeyboardButton(text=name_menu['sizes_menu'], callback_data='sizes')],
        [InlineKeyboardButton(text=name_menu['color_menu'], callback_data='color')],
        [InlineKeyboardButton(text=name_menu['brand_menu'], callback_data='brand')],
        [InlineKeyboardButton(text=name_menu['category_menu'], callback_data='category_0')],
        # [InlineKeyboardButton(text='📋 ПодКатегории', callback_data='subcategory')],
        [InlineKeyboardButton(text=name_menu['delivery_menu'], callback_data='delivery')],
        [InlineKeyboardButton(text=name_menu['about_menu'], callback_data='about')],
        # [InlineKeyboardButton(text='🎁 Товары', callback_data='product')],
])
#[InlineKeyboardButton(text='Главное меню', callback_data='admin')]

main_menu = InlineKeyboardButton(text=name_menu['main_menu'], callback_data='admin')

main_top = InlineKeyboardMarkup(inline_keyboard=[[main_menu]])

main_top_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [main_menu, InlineKeyboardButton(text=name_menu['cancel'], callback_data='about')]
    ])



async def menu_item(text, call):
     return InlineKeyboardButton(text=text, callback_data=call)

async def add_item(i, text='➕ Добавить'):
     return InlineKeyboardButton(text=text, callback_data=f'add_{i}')

cancel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🙅🏻 Отмена', callback_data='admin')]])

next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🙅🏻 Отмена', callback_data='admin'),
         InlineKeyboardButton(text='⏩ Пропустить', callback_data='next')]])

main_top_cancel_next = InlineKeyboardMarkup(inline_keyboard=[
    [main_menu,
     InlineKeyboardButton(text=name_menu['cancel'], callback_data='about'),
     InlineKeyboardButton(text=name_menu['next_menu'], callback_data='next'),
     ]
    ])

# async def kb_about_menu(i):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text='➕', callback_data=f'ub'),
#          ]])
async def kb_next(i):
        return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='🙅🏻 Отмена', callback_data=f'{i}'),
                 InlineKeyboardButton(text='⏩ Пропустить', callback_data='next')]])

async def kb_cancel(i):
        return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='🙅🏻 Отмена', callback_data=f'{i}')]])

del_yes_no = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='DEL 🗑', callback_data='Y'),
         InlineKeyboardButton(text='Отмена 🙅🏻', callback_data='clear_msg')]])

async def cancel_or_main(namemenu, submenu):
        kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⬆️ Главное меню', callback_data='admin'),
         InlineKeyboardButton(text=namemenu, callback_data=submenu)]])
        return kb
async def kbbrand():
        brands = await get_brands()
        brands = brands.all()
        k = []
        for brand in  brands:
                k.append([InlineKeyboardButton(text=f'⬆️ {brand.name}', callback_data=f'plusbrand_{brand.id}')])
        k.append([InlineKeyboardButton(text='🙅🏻 Отмена', callback_data='admin'),
         InlineKeyboardButton(text='⏩ Пропустить', callback_data='next')])
        return InlineKeyboardMarkup(inline_keyboard=k)

async def cat(category_id):
        cats = await get_categorys()
        cats = cats.all()
        buttons = []
        for cat in cats:
                fl = ''
                if int(category_id) == cat.id:
                        fl = '✅'
                buttons.append([InlineKeyboardButton(text=f'{fl} (🆔 {cat.id}) {cat.name}', callback_data=f'cat_{cat.id}')])
        buttons.append([InlineKeyboardButton(text='🙅🏻 Отмена', callback_data='admin')])
        return InlineKeyboardMarkup(inline_keyboard=buttons)