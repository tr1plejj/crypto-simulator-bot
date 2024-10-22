from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select
from database import async_session
from models import User


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Посмотреть монеты'),
            KeyboardButton(text='Профиль')
        ]
    ])
    await message.answer('Привет, если ты новенький, нажми /register и получи первые 100$ на аккаунт', reply_markup=keyboard)


@router.message(Command('register'))
async def register(message: Message):
    user_id = message.from_user.id
    async with async_session() as session:
        query = (
            select(User).
            filter_by(user_id=user_id)
        )
        user = await session.execute(query)
        if user.scalar():
            await message.answer('Вы уже зарегистрированы')
        else:
            session.add(User(user_id=user_id))
            await session.commit()
            await message.answer('Вы успешно зарегистрированы.')