from sqlalchemy import null, func, table, column
from sqlalchemy import select, update, delete, desc
from app.db.models import *
from sqlalchemy import and_, or_

from app.setting import BQ


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
    # return await session.sele(Sizes)
    return await session.scalars(select(Sizes).order_by(Sizes.name))

@sess
async def get_brands(session):
    return await session.scalars(select(Brand).order_by(Brand.name))

@sess
async def get_categorys(session):
    return await session.scalars(select(Category).order_by(Category.name))

@sess
async def get_category_category_id(session, id):
    return await session.scalars(
        select(Category).where(Category.category_id == int(id)).order_by(Category.sort))

@sess
async def get_category_category_id_product(session, id):
    # select(Order.id, Order.product, Customer.name).select_from(
    #     Order).join(Customer, Order.customer_id == Customer.id)
    q = select(Category, Product).select_from(Product).join(
        Category,
        Product.category_id == int(id)
    ).where(Category.id == int(id))
    t = await session.execute(q)
    return t

    # q = select(Price, Product).join(
    #     Price,
    #     Product.id == Price.product_id
    # ).where(Price.id == int(id))
    # t = await session.execute(q)
    # return t.one()
@sess
async def get_sizes_id(session, id):
    return await session.scalar(select(Sizes).where(Sizes.id == int(id)))


@sess
async def get_photo_id(session, id):
    return await session.scalar(select(Photo).where(Photo.id == int(id)))

@sess
async def get_photo_price_id(session, id):
    return await session.scalars(select(Photo).where(Photo.price_id == int(id)))
@sess
async def get_product_category_id(session, id):
    return await session.scalars(
        select(Product).where(Product.category_id == int(id)).order_by(Product.sort))

@sess
async def get_price_product(session, id):
    return await session.scalars(
        select(Price).where(Price.product_id == int(id)).order_by(Price.name))


@sess
async def get_photo_price(session, id):
    return await session.scalars(
        select(Photo).where(Photo.price_id == int(id)).order_by(Photo.sort))

@sess
async def get_price_product_name(session, id):
    return await session.scalar(
        select(Price).where(Price.product_id == int(id)).order_by(Price.name))
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
async def get_user_tg_id(session, tg_id):
    return await session.scalar(select(Users).where(Users.tg_id == int(tg_id)))


@sess
async def get_basket_id(session, id):
    return await session.scalar(select(Basket).where(Basket.id == int(id)))

@sess
async def get_basket(session, user_id):
    return await session.scalars(select(Basket).where(Basket.users_id == int(user_id)))

@sess
async def get_basket_user_product(session, users_id, price_id, product_id):
    return await session.scalar(select(Basket).where(and_(Basket.users_id == int(users_id),
                                                     Basket.product_id == int(product_id),
                                                     Basket.price_id == int(price_id))))

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
async def get_category_subcat_count(session, id):
    result = await session.execute(select(func.count()).select_from(Category).where(Category.category_id==int(id)))
    count = result.scalar()
    return count

@sess
async def get_product_count(session, id):
    result = await session.execute(select(func.count()).select_from(Product).where(Product.category_id==int(id)))
    count = result.scalar()
    return count

@sess
async def get_product_brand_count(session, id):
    result = await session.execute(select(func.count()).select_from(Productbrand).where(Productbrand.product_id==int(id)))
    count = result.scalar()
    return count

@sess
async def get_product_price_count(session, id):
    result = await session.execute(select(func.count()).select_from(Price).where(Price.product_id==int(id)))
    count = result.scalar()
    return count

@sess
async def get_price_photo_count(session, id):
    result = await session.execute(select(func.count()).select_from(Photo).where(Photo.price_id==int(id)))
    count = result.scalar()
    return count


# @sess
# async def get_product_price_count(session, id):
#     result = await session.execute(select(func.count()).select_from(Productbrand).where(Productbrand.product_id==int(id)))
#     count = result.scalar()
#     return count

# @sess
# async def get_subcategory_id(session, id):
#     return await session.scalar(select(Subcategory).where(Subcategory.id == int(id)))

@sess
async def get_product_id(session, id):
    return await session.scalar(select(Product).where(Product.id == int(id)))
@sess
async def get_products_id(session, id):
    return await session.scalars(select(Product).where(Product.category_id == int(id)))
@sess
async def get_price_id(session, id):
    return await session.scalar(select(Price).where(Price.id == int(id)))

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
async def get_productbrand_pl(session, brand_id, product_id):
    res = await session.scalar(select(Productbrand).
                         where(
                   Productbrand.brand_id == int(brand_id),
                               Productbrand.product_id ==int(product_id)))
    if res: return True
    else: return False

@sess
async def get_about(session):
    return await session.scalar(select(About))

@sess
async def get_cat(session):
    return await session.scalar(select(Category))


@sess
async def del_data(session, data):
    id = data['del_id']
    table = data['switch']
    if table == 'users': table = Users
    if table == 'sizes': table = Sizes
    if table == 'color': table = Color
    if table == 'brand': table = Brand
    if table == 'category': table = Category
    if table == 'delivery': table = Delivery
    if table == 'product': table = Product
    if table == 'price': table = Price
    if table == 'photo': table = Photo
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
async def del_item2(session, data):
    id = data['del_id']
    table = data['table']
    if table == 'price': table = Price
    if table == 'photo': table = Photo
    item = await session.get(table, int(id))
    try:
        await session.delete(item)
        await session.commit()
        text = '❌ Удалено!'
    except Exception as e:
        text = "❗️Не удалено. Есть зависимости 🔀 "
    return text
@sess
async def get_basket_all(session, user_id):
    product = await session.scalars(select(Basket).where(Basket.users_id==int(user_id)))
    product = product.all()
    quantity_all = 0
    for pr in product:
        quantity_all = quantity_all + pr.quantity
    # print(f'----------------{quantity_all}-----{BQ}')
    return quantity_all


@sess
async def get_basket_price_all(session, user_id):
    q = select(Price.price, Price.price_discount).select_from(Price, Basket).join(
        Price,
        Basket.price_id == Price.id
    ).where(Basket.users_id == int(user_id))
    t = await session.execute(q)

    price_all = []
    for price in t:
        # print(f'-------------------{price.price}')
        if price.price_discount != 0:
            price_all.append(price.price_discount)
        else:
            price_all.append(price.price)
    # print(f'-------------------{sum(price_all)}')
    return sum(price_all)

@sess
async def set_basket(session, user_id, price_id, product_id, basketact, price_id_basket):
    # print(f'---------{user_id=} {price_id=} {product_id=} {basketact=} {price_id_basket=}-------------')
    basket = await get_basket_user_product(user_id, price_id, product_id)
    quantity_all = await get_basket_all(user_id)

    price = await get_price_id(price_id)
    price_quantity = price.quantity
    if price_id_basket != '':
        if int(price_id_basket) == int(price_id):
            price_id_basket = int(price_id_basket) #== int(price_id):
            if not basket:
                if price_quantity > 0 and quantity_all < BQ:
                    if basketact == "plus":
                        session.add(Basket(users_id = int(user_id), price_id=int(price_id), product_id = int(product_id), quantity = 1))
                        await session.commit()
            else:
                if basketact == "plus" and quantity_all < BQ:
                    if basket.quantity+1 <= price_quantity:
                        await session.execute(update(Basket).where(Basket.price_id == price_id_basket).values(quantity=basket.quantity+1))
                        await session.commit()
                if basketact == "minus":
                    if basket.quantity-1 <= 0:
                        # DELETE FROM public.product WHERE Id = 1
                        await session.execute(delete(Basket).where(Basket.price_id == price_id_basket))
                        await session.commit()
                    else:
                        await session.execute(update(Basket).where(Basket.price_id == price_id_basket).
                                              values(quantity=basket.quantity-1))
                        await session.commit()
    basket = await get_basket_user_product(user_id, price_id, product_id)

    if basket:
        quantity = basket.quantity
    else:
        quantity = 0
    return quantity

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
async def set_about_name(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(name=data))
        await session.commit()
    else:
        session.add(About(name=data))
        await session.commit()


@sess
async def set_about_desc(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(description=data))
        await session.commit()
    else:
        session.add(About(description=data))
        await session.commit

@sess
async def set_about_address(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(address=data))
        await session.commit()
    else:
        session.add(About(address=data))
        await session.commit


@sess
async def set_about_phone(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(phone=data))
        await session.commit()
    else:
        session.add(About(phone=data))
        await session.commit


@sess
async def set_about_email(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(email=data))
        await session.commit()
    else:
        session.add(About(email=data))
        await session.commit

@sess
async def set_about_logo(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(logo=data))
        await session.commit()
    else:
        session.add(About(logo=data))
        await session.commit

@sess
async def set_about_map(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(map=data))
        await session.commit()
    else:
        session.add(About(map=data))
        await session.commit

@sess
async def set_about_photo(session, data):
    about = await get_about()
    if about:
        await session.execute(update(About).values(photo=data))
        await session.commit()
    else:
        session.add(About(photo=data))
        await session.commit
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
    text = '❌ Такая категория уже есть'
    if not category:
        session.add(Category(name=data['name'],
                             sort=data['sort'],
                             photo=data['photo'],
                             category_id=int(data['category_id'])
                             ))
        await session.commit()
        text = '👌 Категория добавлена'
    return text

@sess
async def set_category_up(session, data):
    id = int(data['id'])
    category = await session.scalar(select(Category).where(and_(Category.name == data['name'], Category.id != id)))
    text = '❌ Такая категория уже есть'
    if not category:
        await session.execute(update(Category).where(Category.id == id).values(name=data['name'],
                                                                               sort=data['sort'],
                                                                               photo=data['photo'],
                                                                               category_id=int(data['category_id'])
                                                                               ))
        await session.commit()
        text = "👌 Данные категории обновлены"
    return text

@sess
async def set_product_new(session, data):
    product = await session.scalar(select(Product).where(Product.name == data['name']))
    text = '❌ Такой товар уже есть'
    if not product:
        session.add(Product(name=data['name'],
                             sort=data['sort'],
                             photo=data['photo'],
                             description=data['description'],
                             category_id=int(data['category_id'])
                             ))
        await session.commit()
        text = '👌 Товар добавлен'
    return text

@sess
async def set_product_up(session, data):
    id = int(data['id'])
    product = await session.scalar(select(Product).where(and_(Product.name == data['name'], Product.id != id)))
    text = '❌ Такой товар уже есть'
    if not product:
        await session.execute(update(Product).where(Product.id == id).values(name=data['name'],
                                                                               sort=data['sort'],
                                                                               photo=data['photo'],
                                                                             description=data['description'],
                                                                               category_id=int(data['category_id'])
                                                                               ))
        await session.commit()
        text = "👌 Данные продукта обновлены"
    return text

@sess
async def set_price_new(session, data):
    price = await session.scalar(select(Price).where(Price.name == data['name']))
    text = '❌ Такой прайс уже есть'
    if not price:
        session.add(Price(name=data['name'],
                             price=float(round(data['price'], 2)),
                             price_discount=float(round(data['price_discount'], 2)),
                             quantity=int(data['quantity']),
                             product_id=int(data['product_id']),
                             color_id=int(data['color_id']),
                             sizes_id=int(data['sizes_id'])
                             ))
        await session.commit()
        text = '👌 Прайс добавлен'
    return text

@sess
async def set_price_up(session, data):
    id = int(data['id'])
    price = await session.scalar(select(Price).where(and_(Price.name == data['name'], Price.id != id)))
    text = '❌ Такой прайс уже есть'
    if not price:
        await session.execute(update(Price).where(Product.id == id).values(
                             name=data['name'],
                             price=float(data['price']),
                             price_discount=float(data['price_discount']),
                             quantity=int(data['quantity']),
                             product_id=int(data['product_id']),
                             color_id=int(data['color_id']),
                             sizes_id=int(data['sizes_id'])
                             ))
        await session.commit()
        text = "👌 Данные прайса обновлены"
    return text
@sess
async def set_photo_new(session, data):
    session.add(Photo(sort=data['sort'],
                      photo=data['photo'],
                      price_id=int(data['price_id']),
                         ))
    await session.commit()
    text = '👌 Фото добавлено'
    return text
# @sess
# async def set_subcategory_new(session, data):
#     session.add(Subcategory(sort=data['sort'], name=data['name'], category_id=int(data['category_id']), photo=data['photo']))
#     await session.commit()
#     text = '👌 ПодКатегория добавлена'
#     return text
# @sess
# async def set_subcategory_up(session, data):
#     id = int(data['id'])
#     await session.execute(update(Subcategory).where(Subcategory.id == id).values(name=data['name'], sort=data['sort'], category_id=int(data['category_id']), photo=data['photo']))
#     await session.commit()
#     return "👌 Данные подкатегории обновлены"

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
    return '👌 Метод доставки добавлен'

@sess
async def set_delivery_up(session, data):
    id = int(data['id'])
    await session.execute(update(Delivery).where(Delivery.id == id).values(name=data['name'], sort=data['sort'], price=data['price'],
                         description=data['description']))
    await session.commit()
    return "👌 Данные доставки обновлены"

@sess
async def set_about_new(session, data):
    session.add(About(name=data['name'],
                      description=data['description'],
                      address=data['address'],
                      phone=data['phone'],
                      email=data['email'],
                      map=data['map'],
                      logo=data['logo'],
                      photo=data['photo'],
                      ))
    await session.commit()

@sess
async def set_about_up(session, data):
    id = int(data['id'])
    await session.execute(update(About).where(About.id == id).values(
                    name=data['name'],
                    description=data['description'],
                    address=data['address'],
                    phone=data['phone'],
                    email=data['email'],
                    map=data['map'],
                    logo=data['logo'],
                    photo=data['photo'],
                    ))
    await session.commit()


@sess
async def set_productbrand(session, brand_id, product_id):
    session.add(Productbrand(brand_id = int(brand_id), product_id = int(product_id)))
    await session.commit()

@sess
async def del_productbrand(session, brand_id, product_id):
    item = await session.scalar(select(Productbrand).
                                where(and_(Productbrand.brand_id == int(brand_id), Productbrand.product_id == int(product_id))))
    await session.delete(item)
    await session.commit()

@sess
async def poto_join(session, id):
    q = select(Price, Product).join(
        Price,
        Product.id == Price.product_id
    ).where(Price.id == int(id))
    t = await session.execute(q)
    return t.one()






