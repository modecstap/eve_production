from sqlalchemy import Column, BigInteger, ForeignKey, Date, Sequence, text, Numeric
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Product(Base):
    __tablename__ = 'product'

    id = Column(
        BigInteger,
        Sequence('product_id_seq', start=1, increment=1),
        primary_key=True,
        server_default=text("nextval('product_id_seq')")
    )
    type_id = Column(BigInteger, ForeignKey('type_info.id'), nullable=False)
    order_id = Column(BigInteger, ForeignKey('order.id'))
    station_id = Column(BigInteger, ForeignKey('station.id'))
    blueprint_efficiency = Column(Numeric)
    production_date = Column(Date, nullable=False)

    type_info = relationship('TypeInfo', back_populates='products')
    order = relationship('Order', back_populates='products')
    used_transactions = relationship('UsedTransactionList', back_populates='product')
    station = relationship('Station', back_populates='product')
