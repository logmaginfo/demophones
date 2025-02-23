from app.db.models import async_session
from sqlalchemy import select, update, delete, desc
from app.db.models import *
from app.db.models import *

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
async def get_color(session):
    return await session.scalars(select(Color).order_by(Color.name))

