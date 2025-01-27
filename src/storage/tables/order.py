from sqlalchemy import Column, BigInteger, Date, Numeric, text, Sequence, Enum
from sqlalchemy.orm import relationship

from src.storage.tables.enums import Status
from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Order(Base):
    __tablename__ = 'order'

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
    status = Column(
        Enum(
            Status,
            name="StatusNames"
        ),
        nullable=False
    )

    products = relationship('Product', back_populates='order')
