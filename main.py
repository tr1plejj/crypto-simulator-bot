import asyncio
import logging
import sys
from multiprocessing import Process
from aiogram import Bot, Dispatcher
from screeners import check_buy_prices, check_sell_prices
from handlers import start_router, coin_router, profile_router
import os


TOKEN = os.environ.get('TOKEN')

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        coin_router,
        profile_router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot_process = Process(target=asyncio.run, args=(main(),))
    bot_process.start()

    check_sell_process = Process(target=asyncio.run, args=(check_sell_prices(),))
    check_sell_process.start()

    check_buy_process = Process(target=asyncio.run, args=(check_buy_prices(),))
    check_buy_process.start()


