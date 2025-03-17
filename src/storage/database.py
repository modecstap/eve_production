import time

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Settings
from src.extensions import Singleton
from src.storage.declarative_base import DeclarativeBase
from src.storage.pgsql_functions import pgsql_functions
from src.storage.tables import Order, Product, MaterialList, Transaction, UsedTransactionList, TypeInfo, \
    Station
from src.storage.utils import get_db_url


class Database(metaclass=Singleton):
    def __init__(self):
        self._is_connection = False

        db_config = Settings().config.db_config
        db_url = get_db_url(
            user=db_config.user,
            password=db_config.password,
            host=db_config.host,
            port=db_config.port,
            dname=db_config.db_name
        )

        self.async_engine = create_async_engine(db_url)

        self.async_session_maker = sessionmaker(self.async_engine, expire_on_commit=False, class_=AsyncSession)

    async def create_all(self):
        # SQLAlchemy не создат таблицы в БД если не создать объекты.
        Order()
        Product()
        MaterialList()
        Transaction()
        UsedTransactionList()
        TypeInfo()
        Station()
        while not self._is_connection:
            await self._try_create_session()

    async def _try_create_session(self):
        try:
            async with self.async_engine.begin() as conn:
                await conn.run_sync(DeclarativeBase().base.metadata.create_all)
                for function in pgsql_functions.values():
                    await conn.execute(function)
            self._is_connection = True
        except Exception as e:
            print(f"error connect to DB: {str(e)}")
            time.sleep(10)


if __name__ == '__main__':
    Database().create_all()
