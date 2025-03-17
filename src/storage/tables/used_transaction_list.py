from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class UsedTransactionList(Base):
    __tablename__ = 'used_transaction_list'

    product_id = Column(
        BigInteger,
        ForeignKey('product.id', onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    transaction_id = Column(
        BigInteger,
        ForeignKey('transactions.id', onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    used_count = Column(BigInteger, nullable=False)

    product = relationship('Product', back_populates='used_transactions')
    transaction = relationship('Transaction', back_populates='used_transaction_list')
