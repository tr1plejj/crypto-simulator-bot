from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from database import async_session
from http_client import get_price
from models import UserOrder, User

router = Router()

symbols = ['DEEPUSDT', 'APEUSDT', 'TOMIUSDT', 'MAGICUSDT', 'GODSUSDT', 'LOOKSUSDT',
           'SWEATUSDT', 'TNSRUSDT', 'JUPUSDT', 'CYBERUSDT', 'AEVOUSDT', 'XAIUSDT']


class GetPercent(StatesGroup):
    coin = State()
    amount = State()
    percent = State()


class CoinCallback(CallbackData, prefix='coin'):
    coin: str


class CoinActionCallback(CallbackData, prefix='coinaction'):
    coin: str
    action: str


@router.message(F.text == 'Посмотреть монеты')
async def get_coins(message: Message):
    try:
        user_id = message.from_user.id
        async with async_session() as session:
            check_user = (
                select(User).
                filter_by(user_id=user_id)
            )
            user = await session.execute(check_user)
        if user.scalar() is None:
            await message.answer(
                text='Похоже, вы еще не создали профиль. Для работы бота необходимо зарегистрироваться '
                     '/register')
        else:
            coins_kb = InlineKeyboardBuilder()
            for symbol in symbols:
                coins_kb.button(text=symbol, callback_data=CoinCallback(coin=symbol).pack())
            coins_kb.adjust(3)
            await message.answer(text='Доступные к торговле монеты', reply_markup=coins_kb.as_markup())

    except Exception:
        await message.answer('Неизвестная ошибка')


@router.callback_query(CoinCallback.filter())
async def get_info_about_coin(query: CallbackQuery, callback_data: CoinCallback):
    symbol = callback_data.coin
    price = await get_price(symbol)
    actions_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Закупить и продать при изменении цены на X%',
                                 callback_data=CoinActionCallback(coin=symbol, action='buyandsell').pack())
        ]
    ])
    await query.message.answer(text=f'{symbol} - {price}$', reply_markup=actions_kb)
    await query.answer('Done')


@router.callback_query(CoinActionCallback.filter())
async def get_percent_first(query: CallbackQuery, callback_data: CoinActionCallback, state: FSMContext):
    await query.message.answer('Укажите %, при изменении цены на которое произойдет покупка и затем продажа')
    await state.update_data(coin=callback_data.coin)
    await state.set_state(GetPercent.percent)


@router.message(GetPercent.percent)
async def get_percent_second(message: Message, state: FSMContext):
    try:
        percent = float(message.text)
        if percent >= 100:
            await message.answer('Процент не может быть больше или равен 100')
            await state.set_state(GetPercent.percent)
        else:
            await state.update_data(percent=percent)
            await message.answer(text='Укажите кол-во $, на которое произвести покупку')
            await state.set_state(GetPercent.amount)

    except ValueError:
        await state.set_state(GetPercent.percent)
        await message.answer('Введите число')


@router.message(GetPercent.amount)
async def get_amount_of_dollars(message: Message, state: FSMContext):
    try:
        dollars = float(message.text)
        user_id = message.from_user.id

        async with async_session() as session:
            get_user_balance = (
                select(User.balance).
                filter_by(user_id=user_id)
            )
            user_balance = await session.execute(get_user_balance)
        user_balance = user_balance.one()[0]
        if user_balance <= dollars:
            await message.answer('Недостаточно средств.')
        else:
            data = await state.get_data()
            await state.clear()
            coin = data['coin']
            percent = data['percent']
            coin_price = await get_price(coin)
            buy_price = coin_price - (coin_price * (percent * 0.01))
            amount = dollars / buy_price
            sell_price = coin_price + (coin_price * (percent * 0.01))
            async with async_session() as session:
                session.add(UserOrder(user_id=user_id, coin=coin, buy_price=buy_price,
                                        sell_price=sell_price, amount=amount))
                await session.commit()
            await message.answer(text=f'Заказ на покупку {coin} успешно выставлен. Вам придет уведомление, '
                                          f'как только монета будет куплена и продана.')

    except ValueError:
        await state.set_state(GetPercent.amount)
        await message.answer(text='Пожалуйста, введите число')

    except Exception:
        await message.answer('Неизвестная ошибка')


