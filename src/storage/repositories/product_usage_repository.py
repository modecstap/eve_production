from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.repositories import BaseRepository
from src.storage.repositories.wrappers import ensure_session
from src.storage.tables import Product


class ProductUsageRepository:
    @ensure_session
    async def register_usage(self, product_id: int, count: int, session: AsyncSession):
        await BaseRepository(Product).execute_query(
            query="SELECT create_used_transaction(:input_product_id, :input_count)",
            params={"input_product_id": product_id, "input_count": count},
            session=session
        )