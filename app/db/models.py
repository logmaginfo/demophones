import datetime
import os
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey, String, BigInteger, text, Text

USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
engine = create_async_engine(url=f"postgresql+asyncpg://{USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# PR = Numeric(5,2)

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(25), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(String(200), nullable=True)
    comment: Mapped[str] = mapped_column(String(300), nullable=True)
    date_create: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    date_last: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Sizes(Base):
    __tablename__ = 'sizes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    description: Mapped[str] = mapped_column(Text)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    photo: Mapped[str] = mapped_column(String(300), nullable=True)
    category_id: Mapped[int] = mapped_column(default=0)
    # level: Mapped[int] = mapped_column(nullable=False)


class Price(Base):
    __tablename__ = 'price'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(90), nullable=True)
    price: Mapped[float] = mapped_column(default=0)
    price_discount: Mapped[float] = mapped_column(default=0)
    quantity: Mapped[int] = mapped_column(default=0)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)
    color_id: Mapped[int] = mapped_column(ForeignKey('color.id'), nullable=True)
    sizes_id: Mapped[int] = mapped_column(ForeignKey('sizes.id'), nullable=True)


class Brand(Base):
    __tablename__ = 'brand'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    # product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)


class Productbrand(Base):
    __tablename__ = 'productbrand'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    photo: Mapped[str] = mapped_column(String(300), nullable=True)
    category_id: Mapped[int] = mapped_column(default=0)


class Photo(Base):
    __tablename__ = 'photo'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    photo: Mapped[str] = mapped_column(String(300), nullable=True)
    price_id: Mapped[int] = mapped_column(ForeignKey('price.id'), nullable=False)
    price: Mapped['Price'] = relationship()


# class Tag(Base):
#     __tablename__ = 'tag'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     sort: Mapped[str] = mapped_column(String(5), nullable=True)
#     name: Mapped[str] = mapped_column(String(200), nullable=True)
#     product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)

class Color(Base):
    __tablename__ = 'color'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    photo: Mapped[str] = mapped_column(String(300), nullable=True)


class Delivery(Base):
    __tablename__ = 'delivery'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(90), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(default=0)


class basket(Base):
    __tablename__ = 'basket'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    users_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=False)
    price_id: Mapped[int] = mapped_column(ForeignKey('price.id'), nullable=True)
    quantity: Mapped[int]


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(50))
    users_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=False)
    price: Mapped[float] = mapped_column(default=0)
    delivery: Mapped[float] = mapped_column(default=0)
    quantity: Mapped[int]
    color_id: Mapped[int] = mapped_column(ForeignKey('color.id'), nullable=False)
    sizes_id: Mapped[int] = mapped_column(ForeignKey('sizes.id'), nullable=False)
    date_create: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    comment: Mapped[str] = mapped_column(String(200))


class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(50))
    users_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    orders_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)
    amount: Mapped[float] = mapped_column(default=0)
    payment: Mapped[str] = mapped_column(String(300))
    date_create: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class About(Base):
    __tablename__ = 'about'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(90))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(200), nullable=True)
    phone: Mapped[str] = mapped_column(String(25), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    map: Mapped[str] = mapped_column(String(300), nullable=True)
    logo: Mapped[str] = mapped_column(String(300), nullable=True)
    photo: Mapped[str] = mapped_column(String(300), nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
