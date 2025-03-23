from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class TypeInfo(Base):
    __tablename__ = 'type_info'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(500), nullable=False)
    is_produced = Column(Boolean, nullable=False, default=False)

    transactions = relationship('Transaction', back_populates='material')
    material_list_material = relationship(
        'MaterialList',
        back_populates='material',
        foreign_keys='MaterialList.material_id'
    )
    material_list_type = relationship(
        'MaterialList',
        back_populates='type_info',
        foreign_keys='MaterialList.type_id'
    )
