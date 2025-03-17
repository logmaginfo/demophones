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


class Price(Base):#, ondelete="DELETE"
    __tablename__ = 'price'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(90), nullable=True)
    price: Mapped[float] = mapped_column(default=0)
    price_discount: Mapped[float] = mapped_column(default=0)
    quantity: Mapped[int] = mapped_column(default=0)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)
    color: Mapped[str] = mapped_column(String(90), nullable=True)
    colorphoto: Mapped[str] = mapped_column(String(300), nullable=True)
    sizes: Mapped[str] = mapped_column(String(90), nullable=True)


class Brand(Base):
    __tablename__ = 'brand'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    # productbrand: Mapped[list['Orders']] = relationship(back_populates="brand")



class Productbrand(Base):
    __tablename__ = 'productbrand'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)
    # brand: Mapped[list['Orders']] = relationship(back_populates="productbrand")



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
    colorphoto: Mapped[str] = mapped_column(String(300), nullable=True)


class Delivery(Base):
    __tablename__ = 'delivery'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(90), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(default=0)


class Basket(Base):
    __tablename__ = 'basket'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    users_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete="CASCADE"), nullable=True)
    price_id: Mapped[int] = mapped_column(ForeignKey('price.id', ondelete="CASCADE"), nullable=True)
    quantity: Mapped[int]

class OrderNumber(Base):
    __tablename__ = 'ordernumber'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(50), nullable=True)
    users_id: Mapped[int] = mapped_column(nullable=True)
    tg_id = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(50), nullable=True)
    comment: Mapped[str] = mapped_column(String(200), nullable=True)
    delivery: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_price: Mapped[float] = mapped_column(nullable=True)
    date_create: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    orders: Mapped[list['Orders']] = relationship(back_populates="ordernumber")

class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(50), nullable=True)
    ordernumber_id: Mapped[int] = mapped_column(ForeignKey('ordernumber.id'), nullable=True)
    product: Mapped[str] = mapped_column(Text, nullable=True)
    price_id: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(default=0)
    color:  Mapped[str] = mapped_column(String(100), nullable=True)
    colorphoto: Mapped[str] = mapped_column(String(300), nullable=True)
    sizes: Mapped[str] = mapped_column(String(90), nullable=True)
    quantity: Mapped[int] = mapped_column(default=0, nullable=True)
    ordernumber: Mapped['OrderNumber'] = relationship(back_populates="orders")

    # name: Mapped[str] = mapped_column(String(90), nullable=True)
    # price: Mapped[float] = mapped_column(default=0)
    # price_discount: Mapped[float] = mapped_column(default=0)
    # quantity: Mapped[int] = mapped_column(default=0)
    # product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)
    # color: Mapped[str] = mapped_column(String(90), nullable=True)
    # colorphoto: Mapped[str] = mapped_column(String(300), nullable=True)
    # sizes: Mapped[str] = mapped_column(String(90), nullable=True)

class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(50))
    users_id: Mapped[int] = mapped_column(nullable=True)
    ordersnumber_id: Mapped[int] = mapped_column(ForeignKey('ordersnumber.id'), nullable=True)
    amount: Mapped[float] = mapped_column(default=0)
    payment: Mapped[str] = mapped_column(String(300))
    date_create: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class About(Base):
    __tablename__ = 'about'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(90))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(200), nullable=True)
    phone: Mapped[str] = mapped_column(String(200), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    map: Mapped[str] = mapped_column(String(300), nullable=True)
    logo: Mapped[str] = mapped_column(String(300), nullable=True)
    photo: Mapped[str] = mapped_column(String(300), nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
