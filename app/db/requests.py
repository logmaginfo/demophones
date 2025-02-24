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
async def get_color(session):
    return await session.scalars(select(Color).order_by(Color.name))


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
async def get_color_id(session, id):
    return await session.scalar(select(Color).where(Color.id == int(id)))

@sess
async def del_data(session, data):
    id = data['del_id']
    table = data['switch']
    if table == 'users':table = Users
    if table == 'sizes': table = Sizes
    if table == 'color': table = Color
    user = await session.get(table, int(id))
    await session.delete(user)
    await session.commit()

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
