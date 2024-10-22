from aiogram import Bot
from http_client import get_price
from models import UserOrder, UserCapital, User
from sqlalchemy import select, delete, update
from database import async_session
import os


TOKEN = os.environ.get('TOKEN')

bot = Bot(TOKEN)


async def send_notification_about_buy(chat_id: int, coin: str, buy_price: int, amount: int):
    await bot.send_message(chat_id=chat_id, text=f'{coin} достигла цены {buy_price}.\nКуплено {amount} монет')
    await bot.session.close()


async def check_buy_prices():
    while True:
        async with async_session() as session:
            query = select(UserOrder)
            data = await session.execute(query)
            users = data.scalars().all()
        for user in users:
            coin = user.coin
            buy_price = user.buy_price
            user_id = user.user_id
            sell_price = user.sell_price
            amount = user.amount
            current_price = await get_price(coin)
            if current_price <= buy_price:
                dollars = current_price * amount
                async with async_session() as session:
                    get_user_balance = (
                        select(User.balance).
                        filter_by(user_id=user_id)
                    )
                    user_balance = await session.execute(get_user_balance)
                    user_balance = user_balance.one()[0]
                    new_user_balance = user_balance - dollars
                    if new_user_balance < 0:
                        break
                    change_user_balance = (
                        update(User).
                        filter_by(user_id=user_id).
                        values(balance=new_user_balance)
                    )
                    await session.execute(change_user_balance)
                    await session.commit()

                    session.add(UserCapital(user_id=user_id, coin=coin, sell_price=sell_price, amount=amount))
                    query = (
                        delete(UserOrder).
                        filter_by(user_id=user_id, coin=coin, buy_price=buy_price, sell_price=sell_price, amount=amount)
                    )
                    await session.execute(query)
                    await session.commit()

                await send_notification_about_buy(chat_id=user_id, coin=coin, buy_price=buy_price, amount=amount)