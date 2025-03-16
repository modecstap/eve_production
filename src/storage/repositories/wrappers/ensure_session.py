from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession


def ensure_session(method):
    @wraps(method)
    async def wrapper(self, session: AsyncSession = None, *args, **kwargs):
        function_owner_session = session is None  # Проверяем, создаёт ли метод свою сессию

        if function_owner_session:
            async with self.db.async_session_maker() as session:  # Создаём новую сессию

                try:
                    return await method(self, session, *args, **kwargs)  # Передаём сессию в метод
                finally:
                    if function_owner_session:
                        await session.close()  # Закрываем сессию, если создавали её здесь

    return wrapper

