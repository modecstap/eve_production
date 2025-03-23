from sqlalchemy import Column, BigInteger, ForeignKey, Sequence, text, Numeric
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Product(Base):
    __tablename__ = 'product'

    # ПОЛЯ ТАБЛИЦЫ

    id = Column(
        BigInteger,
        Sequence('product_id_seq', start=1, increment=1),
        primary_key=True,
        server_default=text("nextval('product_id_seq')")
    )
    station_id = Column(
        BigInteger,
        ForeignKey('station.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    blueprint_efficiency = Column(Numeric)

    # ИСХОДЯЩИЕ ОТНОШЕНИЯ

    station = relationship('Station', back_populates='product')

    # ВХОДЯЩИЕ ОТНОШЕНИЯ

    transactions = relationship('Transaction', back_populates='product')
    used_transactions = relationship('UsedTransactionList', back_populates='product')
