from sqlalchemy import BigInteger, Column, Integer, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    user_id = Column(BigInteger, primary_key=True, autoincrement=False, nullable=False)
    balance = Column(Integer, default=100)


class UserCapital(Base):
    __tablename__ = 'capital'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    coin = Column(String(15), nullable=False)
    amount = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=False)


class UserOrder(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    coin = Column(String(15), nullable=False)
    amount = Column(Integer, nullable=False)
    buy_price = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=False)