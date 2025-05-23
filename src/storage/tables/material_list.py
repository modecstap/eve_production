from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class MaterialList(Base):
    __tablename__ = 'material_list'

    # ПОЛЯ ТАБЛИЦЫ

    material_id = Column(
        BigInteger,
        ForeignKey('type_info.id', onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )

    type_id = Column(
        BigInteger,
        ForeignKey('type_info.id', onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    need_count = Column(BigInteger)

    # ИСХОДЯЩИЕ ОТНОШЕНИЯ

    # ИСХОДЯЩИЕ ОТНОШЕНИЯ

    material = relationship(
        'TypeInfo',
        foreign_keys=[material_id],
        back_populates='material_list_material'
    )
    type_info = relationship(
        'TypeInfo',
        foreign_keys=[type_id],
        back_populates='material_list_type'
    )
