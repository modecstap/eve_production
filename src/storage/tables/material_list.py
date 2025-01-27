from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class MaterialList(Base):
    __tablename__ = 'material_list'

    material_id = Column(BigInteger, ForeignKey('material.id'), primary_key=True)
    type_id = Column(BigInteger, ForeignKey('type_info.id'), primary_key=True)
    count = Column(BigInteger)

    material = relationship('Material', back_populates='material_list')
    type_info = relationship('TypeInfo', back_populates='material_list')
