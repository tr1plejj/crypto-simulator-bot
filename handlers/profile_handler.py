from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from database import async_session
from models import User, UserCapital, UserOrder


router = Router()


@router.message(F.text == 'Профиль')
async def get_profile(message: Message):
    user_id = message.from_user.id
    async with async_session() as session:
        query = (
            select(User).
            filter_by(user_id=user_id)
        )
        user = await session.execute(query)
    user = user.scalar()
    if user:
        async with async_session() as session:
            query = (
                select(UserCapital).
                filter_by(user_id=user_id)
            )
            capital = await session.execute(query)
            capital = capital.scalars().all()
            query = (
                select(UserOrder).
                filter_by(user_id=user_id)
            )
            orders = await session.execute(query)
            orders = orders.scalars().all()

        profile_msg = f'Баланс: {user.balance}$\n\nЗаказы на покупку:'
        for order in orders:
            coin = order.coin
            amount = order.amount
            dollars = order.buy_price * amount
            profile_msg += f'\n\n{coin}\n\t\tКоличество: {amount}\n\t\tНа сумму: {dollars}$'

        profile_msg += '\n\nЗаказы на продажу:'

        for cap in capital:
            coin = cap.coin
            amount = cap.amount
            dollars = cap.sell_price * amount
            profile_msg += f'\n\n{coin}\n\t\tКоличество: {amount}\n\t\tНа сумму: {dollars}'

        await message.answer(text=profile_msg)

    else:
        await message.answer(text='Вы еще не зарегистрированы. Нажмите /register')