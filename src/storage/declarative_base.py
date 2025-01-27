from sqlalchemy.orm import declarative_base

from src.extensions import Singleton


class DeclarativeBase(metaclass=Singleton):
    def __init__(self):
        self.base = declarative_base()
