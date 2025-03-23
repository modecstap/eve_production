from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession


def ensure_session(method):
    @wraps(method)
    async def wrapper(self, *args, session: AsyncSession = None, **kwargs):
        if session is None:  # Если сессия не передана, создаём новую
            async with self.db.async_session_maker() as session:
                try:
                    return await method(self, *args, session=session, **kwargs)
                finally:
                    await session.close()
        else:
            return await method(self, *args, session=session, **kwargs)  # Используем переданную сессию

    return wrapper
