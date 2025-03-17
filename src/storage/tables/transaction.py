from sqlalchemy import Column, BigInteger, ForeignKey, Numeric, Sequence, text, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(
        BigInteger,
        Sequence('transactions_id_seq', start=1, increment=1),
        primary_key=True,
        server_default=text("nextval('transactions_id_seq')")
    )
    release_date = Column(TIMESTAMP, nullable=False)
    material_id = Column(
        BigInteger,
        ForeignKey('type_info.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    count = Column(BigInteger, nullable=False)
    price = Column(Numeric, nullable=False)
    remains = Column(BigInteger, nullable=False)
    is_produced = Column(Boolean, nullable=False, default=False)

    material = relationship('TypeInfo', back_populates='transactions')
    used_transaction_list = relationship('UsedTransactionList', back_populates='transaction')
