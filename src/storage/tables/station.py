from sqlalchemy import Column, BigInteger, String, Sequence, text, Numeric
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Station(Base):
    __tablename__ = 'station'

    # ПОЛЯ ТАБЛИЦЫ

    id = Column(
        BigInteger,
        Sequence('station_id_seq', start=1, increment=1),
        primary_key=True,
        server_default=text("nextval('station_id_seq')")
    )
    name = Column(String(500), nullable=False)
    material_efficiency = Column(Numeric)
    tax_percent = Column(Numeric)
    security_status = Column(Numeric)

    # ИСХОДЯЩИЕ ОТНОШЕНИЯ

    # ВХОДЯЩИЕ ОТНОШЕНИЯ

    product = relationship('Product', back_populates='station')
