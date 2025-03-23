from sqlalchemy import Column, BigInteger, Date, Numeric, text, Sequence, Enum, ForeignKey
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase
from src.storage.tables.enums import Status

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
    price = Column(Numeric, nullable=False)
    commission_percent = Column(Numeric, nullable=False)
    tax_percent = Column(Numeric, nullable=False)
    updating_cost = Column(Numeric)
    release_date = Column(Date, nullable=False)
    transaction_id = Column(
        BigInteger,
        ForeignKey('transactions.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    status = Column(
        Enum(Status, name="StatusNames"),
        nullable=False
    )

    # ИСХОДЯЩИЕ ОТНОШЕНИЯ

    transaction = relationship('Transaction', back_populates='orders')

    # ВХОДЯЩИЕ ОТНОШЕНИЯ
