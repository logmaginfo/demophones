from sqlalchemy import null

from app.db.models import async_session
from sqlalchemy import select, update, delete, desc
from app.db.models import *
from app.db.models import *
from sqlalchemy import null

def sess(func):
    async def con(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return con


@sess
async def set_user(session, message):
    #   async with async_session() as session:
    user = await session.scalar(select(Users).where(Users.tg_id == message.from_user.id))

    if not user:
        session.add(Users(tg_id=message.from_user.id, name=message.from_user.first_name,
                          last_name=message.from_user.last_name,
                          comment=str(message.from_user.is_bot)))
        await session.commit()
        user = await session.scalar(select(Users).where(Users.tg_id == message.from_user.id))
        text = f'Новый пользователь:\n{user.id=}\n{user.tg_id=}'
        await message.bot.send_message(chat_id=-1002266116367, text=text)


@sess
async def get_users(session):
    return await session.scalars(select(Users))


@sess
async def get_sizes(session):
    return await session.scalars(select(Sizes).order_by(Sizes.name))

@sess
async def get_brands(session):
    return await session.scalars(select(Brand).order_by(Brand.name))

@sess
async def get_categorys(session):
    return await session.scalars(select(Category).order_by(Category.name))

@sess
async def get_subcategory(session):
    return await session.scalars(select(Subcategory).order_by(Subcategory.sort))

@sess
async def get_subcategory_category_id(session, id):
    return await session.scalars(select(Subcategory).where(Subcategory.category_id==int(id)).order_by(Subcategory.sort))
    # return await session.scalars(select(Subcategory).where(Subcategory.category_id == id))

@sess
async def get_color(session):
    return await session.scalars(select(Color).order_by(Color.name))

@sess
async def get_delivery(session):
    return await session.scalars(select(Delivery).order_by(Delivery.sort))

@sess
async def get_product(session):
    return await session.scalars(select(Product).order_by(Product.sort))

@sess
async def set_user_new(session, data):
    tg_id = int(data['tg_id'])
    user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
    text = '❌ Такой пользователь уже есть'
    if not user:
        session.add(Users(tg_id=tg_id, name=data['name'],
                          last_name=data['last_name'], phone=data['phone'],
                          email=data['email'], address=data['address'],
                          comment=data['comment']))
        await session.commit()
        text = '👌 Пользователь добавлен'
    return text

#
@sess
async def set_user_up(session, data):
    tg_id = int(data['tg_id'])
    await session.execute(update(Users).where(Users.tg_id == tg_id).values(name=data['name'],
                          last_name=data['last_name'], phone=data['phone'],
                          email=data['email'], address=data['address'],
                          comment=data['comment']))
    await session.commit()
    return "👌 Данные пользователя обновлены"


@sess
async def get_user_id(session, id):
  #  async with async_session() as session:
    return await session.scalar(select(Users).where(Users.id == int(id)))


@sess
async def get_size_id(session, id):
    return await session.scalar(select(Sizes).where(Sizes.id == int(id)))

@sess
async def get_brand_id(session, id):
    return await session.scalar(select(Brand).where(Brand.id == int(id)))

@sess
async def get_category_id(session, id):
    return await session.scalar(select(Category).where(Category.id == int(id)))

@sess
async def get_subcategory_id(session, id):
    return await session.scalar(select(Subcategory).where(Subcategory.id == int(id)))

@sess
async def get_product_id(session, id):
    return await session.scalar(select(Product).where(Product.id == int(id)))

@sess
async def get_product_cat(session, catprod):
    return await session.scalars(select(Product).where(Product.category_id == int(catprod)))

@sess
async def get_product_subcat(session, subcatprod):
    return await session.scalars(select(Product).where(Product.subcategory_id == int(subcatprod)))

@sess
async def get_color_id(session, id):
    return await session.scalar(select(Color).where(Color.id == int(id)))

@sess
async def get_delivery_id(session, id):
    return await session.scalar(select(Delivery).where(Delivery.id == int(id)))

@sess
async def del_data(session, data):
    id = data['del_id']
    table = data['switch']
    if table == 'users': table = Users
    if table == 'sizes': table = Sizes
    if table == 'color': table = Color
    if table == 'brand': table = Brand
    if table == 'category': table = Category
    if table == 'subcategory': table = Subcategory
    if table == 'delivery': table = Delivery
    if table == 'product': table = Product
    text = '❗️ Что-то не так!'
    item = await session.get(table, int(id))
    try:
        await session.delete(item)
        await session.commit()
        text = (True, '❌ Удалено!', data['switch'])
    except Exception as e:
        text = (False, "❗️Не удалено. Есть зависимости 🔀 ", data['switch'])
    return text

@sess
async def set_size_new(session, data):
    size = await session.scalar(select(Sizes).where(Sizes.name == data['name']))
    text = '❌ Такой размер уже есть'
    if not size:
        session.add(Sizes(name=data['name'], description=data['description']))
        await session.commit()
        text = '👌 Размер добавлен'
    return text

@sess
async def set_size_up(session, data):
    id = int(data['id'])
    await session.execute(update(Sizes).where(Sizes.id == id).values(name=data['name'],
                         description=data['description']))
    await session.commit()
    return "👌 Данные размера обновлены"

@sess
async def set_brand_new(session, data):
    brand = await session.scalar(select(Brand).where(Brand.name == data['name']))
    text = '❌ Такой бренд уже есть'
    if not brand:
        session.add(Brand(sort=data['sort'], name=data['name'], description=data['description']))
        await session.commit()
        text = '👌 Бренд добавлен'
    return text

@sess
async def set_brand_up(session, data):
    id = int(data['id'])
    await session.execute(update(Brand).where(Brand.id == id).values(sort=data['sort'], name=data['name'],
                         description=data['description']))
    await session.commit()
    return "👌 Данные бренда обновлены"

@sess
async def set_category_new(session, data):
    category = await session.scalar(select(Category).where(Category.name == data['name']))
    text = '❌ Такой уже есть'
    if not category:
        session.add(Category(name=data['name'], sort=data['sort'], photo=data['photo']))
        await session.commit()
        text = '👌 Категория добавлена'
    return text

@sess
async def set_category_up(session, data):
    id = int(data['id'])
    await session.execute(update(Category).where(Category.id == id).values(name=data['name'], sort=data['sort'], photo=data['photo']))
    await session.commit()
    return "👌 Данные категории обновлены"


@sess
async def set_subcategory_new(session, data):
    session.add(Subcategory(sort=data['sort'], name=data['name'], category_id=int(data['category_id']), photo=data['photo']))
    await session.commit()
    text = '👌 ПодКатегория добавлена'
    return text
@sess
async def set_subcategory_up(session, data):
    id = int(data['id'])
    await session.execute(update(Subcategory).where(Subcategory.id == id).values(name=data['name'], sort=data['sort'], category_id=int(data['category_id']), photo=data['photo']))
    await session.commit()
    return "👌 Данные подкатегории обновлены"

@sess
async def set_color_new(session, data):
    session.add(Color(name=data['name'], photo=data['photo']))
    await session.commit()
    return '👌 Цвет добавлен'

@sess
async def set_color_up(session, data):
    id = int(data['id'])
    await session.execute(update(Color).where(Color.id == id).values(name=data['name'],
                         photo=data['photo']))
    await session.commit()
    return "👌 Данные цвета обновлены"

@sess
async def set_delivery_new(session, data):
    session.add(Delivery(name=data['name'], sort=data['sort'], price=data['price'],
                         description=data['description']))
    await session.commit()
    return '👌 Метор доставки добавлен'

@sess
async def set_delivery_up(session, data):
    id = int(data['id'])
    await session.execute(update(Delivery).where(Delivery.id == id).values(name=data['name'], sort=data['sort'], price=data['price'],
                         description=data['description']))
    await session.commit()
    return "👌 Данные доставки обновлены"

@sess
async def set_product_new(session, data):

    category_id = int(data['catprod'])
    if category_id == 0: category_id = null()

    subcategory_id = int(data['subcatprod'])
    if subcategory_id == 0: subcategory_id = null()

    brand_id = int(data['brand_id'])
    if brand_id == 0: brand_id = null()

    session.add(Product(sort=data['sort'], name=data['name'], description=data['description'],
                        brand_id=brand_id,
                         category_id=category_id, subcategory_id=subcategory_id))
    await session.commit()
    return '👌 Товар добавлен 🎁'

@sess
async def set_product_up(session, data):
    id = int(data['id'])

    category_id = int(data['catprod'])
    if category_id == 0: category_id = null()

    subcategory_id = int(data['subcatprod'])
    if subcategory_id == 0: subcategory_id = null()

    brand_id = int(data['brand_id'])
    if brand_id == 0: brand_id = null()

    await session.execute(update(Product).where(Product.id == id).values(sort=data['sort'], name=data['name'], description=data['description'],
                        brand_id=brand_id,
                         category_id=category_id, subcategory_id=subcategory_id))
    await session.commit()
    return "👌 Данные продукта обновлены 🎁"


