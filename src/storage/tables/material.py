from sqlalchemy import Column, BigInteger, String, Sequence, text
from sqlalchemy.orm import relationship

from src.storage.declarative_base import DeclarativeBase

Base = DeclarativeBase().base


class Material(Base):
    __tablename__ = 'material'

    id = Column(
        BigInteger,
        Sequence('material_id_seq', start=1, increment=1),
        primary_key=True,
        server_default=text("nextval('material_id_seq')")
    )
    name = Column(String(500), nullable=False)

    material_list = relationship('MaterialList', back_populates='material')
