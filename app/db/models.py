import datetime
import os
from sqlalchemy import ForeignKey, String, BigInteger, Numeric
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

PR = Numeric(5,2)
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



class Price(Base):
    __tablename__ = 'price'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    price: Mapped[float] = mapped_column(PR, default=0)
    price_discount: Mapped[float] = mapped_column(PR, default=0)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=True)
    color_id: Mapped[int] = mapped_column(ForeignKey('color.id'), nullable=True)
    sizes_id: Mapped[int] = mapped_column(ForeignKey('sizes.id'), nullable=True)

class Subcategory(Base):
    __tablename__ = 'subcategory'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    photo: Mapped[str] = mapped_column(String(300), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)
    category: Mapped['Category'] = relationship()

class Brand(Base):
    __tablename__ = 'brand'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text)

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'), nullable=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'), nullable=True)
    category: Mapped['Category'] = relationship()
    subcategory: Mapped['Subcategory'] = relationship()
    brand: Mapped['Brand'] = relationship()

class Photo(Base):
    __tablename__ = 'photo'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sort: Mapped[str] = mapped_column(String(5), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True)
    price_id: Mapped[int] = mapped_column(ForeignKey('price.id'), nullable=False)
    price: Mapped['Price']=relationship()

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
    price: Mapped[float] = mapped_column(PR, default=0)

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
    price: Mapped[float] = mapped_column(PR, default=0)
    delivery: Mapped[float] = mapped_column(PR, default=0)
    quantity: Mapped[int]
    color_id: Mapped[int] = mapped_column(ForeignKey('color.id'), nullable=False)
    sizes_id: Mapped[int] = mapped_column(ForeignKey('sizes.id'), nullable=False)
    date_create: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    date_last: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    comment: Mapped[str] = mapped_column(String(200))

class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(50))
    users_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    orders_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)
    amount: Mapped[float] = mapped_column(PR, default=0)
    payment: Mapped[str] = mapped_column(String(300))
    date_create: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    date_last: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
