from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class TypeInfo(Base):
    __tablename__ = 'type_info'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(500), nullable=False)
    is_produced = Column(Boolean, nullable=False, default=False)

    products = relationship('Product', back_populates='type_info')
    material_list = relationship('MaterialList', back_populates='type_info')
