from aiogram import Bot
from sqlalchemy import select, update, delete
from database import async_session
from http_client import get_price
from models import UserCapital, User
import os


TOKEN = os.environ.get('TOKEN')

bot = Bot(TOKEN)

async def send_notification_about_sell(chat_id: int, coin: str, sell_price: int, amount: int):
    await bot.send_message(chat_id=chat_id, text=f'{coin} достигла цены {sell_price}.\nПродано {amount} монет')
    await bot.session.close()


async def check_sell_prices():
    while True:
        async with async_session() as session:
            query = select(UserCapital)
            data = await session.execute(query)
            users = data.scalars().all()
        for user in users:
            user_id = user.user_id
            coin = user.coin
            sell_price = user.sell_price
            amount = user.amount
            current_price = await get_price(coin)
            if current_price >= sell_price:
                dollars = amount * current_price
                async with async_session() as session:
                    get_user_balance = (
                        select(User.balance).
                        filter_by(user_id=user_id)
                    )
                    user_balance = await session.execute(get_user_balance)
                    user_balance = user_balance.one()[0]
                    new_user_balance = user_balance + dollars
                    change_user_balance = (
                        update(User).
                        filter_by(user_id=user_id).
                        values(balance=new_user_balance)
                    )
                    await session.execute(change_user_balance)
                    await session.commit()

                    query = (
                        delete(UserCapital).
                        filter_by(user_id=user_id, sell_price=sell_price, amount=amount, coin=coin)
                    )
                    await session.execute(query)
                    await session.commit()

                await send_notification_about_sell(chat_id=user_id, coin=coin, sell_price=sell_price, amount=amount)