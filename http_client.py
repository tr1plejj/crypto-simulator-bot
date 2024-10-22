from aiohttp import ClientSession


async def get_session():
    return ClientSession()


async def get_price(symbol: str):
    session = await get_session()
    async with session.get(url='https://api.bybit.com/v5/market/tickers',
                           params={'category': 'inverse', 'symbol': symbol}) as resp:
        result = await resp.json()
        price = result.get('result').get('list')[0].get('indexPrice')
    await session.close()
    return float(price)


