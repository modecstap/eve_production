from sqlalchemy import Column, BigInteger, ForeignKey, Numeric, Sequence, text, TIMESTAMP
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Transaction(Base):
    __tablename__ = 'transactions'

    # ПОЛЯ ТАБЛИЦЫ

    id = Column(
        BigInteger,
        Sequence('transactions_id_seq', start=1, increment=1),
        primary_key=True,
        server_default=text("nextval('transactions_id_seq')")
    )
    material_id = Column(
        BigInteger,
        ForeignKey('type_info.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    product_id = Column(
        BigInteger,
        ForeignKey('product.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True
    )
    release_date = Column(TIMESTAMP, nullable=False)
    count = Column(BigInteger, nullable=False)
    price = Column(Numeric, nullable=False)
    remains = Column(BigInteger, nullable=False)

    # ИСХОДЯЩИЕ ОТНОШЕНИЯ

    product = relationship('Product', back_populates='transactions')
    material = relationship('TypeInfo', back_populates='transactions')

    # ВХОДЯЩИЕ ОТНОШЕНИЯ

    used_transaction_list = relationship('UsedTransactionList', back_populates='transaction')
    orders = relationship("Order", back_populates="transaction")
