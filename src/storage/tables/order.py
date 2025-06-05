from sqlalchemy import Column, BigInteger, Date, Numeric, text, Sequence, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Order(Base):
    __tablename__ = 'order'

    # ПОЛЯ ТАБЛИЦЫ

    id = Column(
        BigInteger,
        Sequence('order_id_seq', start=1, increment=1),
        primary_key=True,
        server_default=text("nextval('order_id_seq')")
    )
    transaction_id = Column(
        BigInteger,
        ForeignKey('transactions.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    release_date = Column(Date, nullable=False)
    price = Column(Numeric, nullable=False)
    count = Column(Integer, nullable=False)
    remains = Column(Integer, nullable=False)
    broker_cost = Column(Numeric, default=0)
    tax_percent = Column(Numeric, nullable=False)
    income = Column(Numeric, default=0)

    # ИСХОДЯЩИЕ ОТНОШЕНИЯ

    transaction = relationship('Transaction', back_populates='orders')

    # ВХОДЯЩИЕ ОТНОШЕНИЯ
