from sqlalchemy import text, select, and_

from src.storage.repositories.base import BaseRepository
from src.storage.tables import Product


class ProductRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Product

    async def insert_with_used_transaction(self, products: list[Product]):
        async with self.db.async_session() as session:
            session.add_all(products)
            await session.flush()
            for product in products:
                create_used_transaction = text(f"""
                                DO $$
                                    DECLARE
                                        r_material material_list%ROWTYPE;
                                        r_transaction transactions%ROWTYPE;
                                        r_used_count INTEGER;
                                        r_remaining_need INTEGER;
                                        r_remaining_remains INTEGER;
                                        input_product_id INTEGER;
                                    BEGIN
                                        input_product_id := {product.id};

                                        FOR r_material IN 
                                            SELECT * FROM material_list 
                                            WHERE count > 0 AND type_id = (SELECT type_id FROM product WHERE id = input_product_id)
                                        LOOP
                                            r_remaining_need := r_material.count;

                                            FOR r_transaction IN 
                                                SELECT * FROM transactions
                                                WHERE material_id = r_material.material_id AND remains > 0
                                                ORDER BY release_date
                                            LOOP
                                                IF r_remaining_need > 0 THEN
                                                    IF r_transaction.remains >= r_remaining_need THEN
                                                        r_used_count := r_remaining_need;
                                                        r_remaining_remains := r_transaction.remains - r_used_count;
                                                        r_remaining_need := 0;
                                                    ELSE
                                                        r_used_count := r_transaction.remains;
                                                        r_remaining_remains := 0;
                                                        r_remaining_need := r_remaining_need - r_used_count;
                                                    END IF;

                                                    INSERT INTO used_transaction_list (product_id, transaction_id, used_count)
                                                    VALUES (input_product_id, r_transaction.id, r_used_count)
                                                    ON CONFLICT (product_id, transaction_id) DO NOTHING;

                                                    UPDATE transactions
                                                    SET remains = r_remaining_remains
                                                    WHERE id = r_transaction.id;
                                                END IF;
                                            END LOOP;
                                        END LOOP;
                                    END $$;
                            """)
                await session.execute(create_used_transaction)
            await session.commit()

    async def get_products_without_order(self, type_id: int) -> list[Product]:
        async with self.db.async_session() as session:
            products = await session.execute(
                select(self._entity)
                .where(
                    and_(
                        self._entity.order == None,
                        self._entity.type_id == type_id
                    )
                )
            )
            return products.scalars().all()

    async def set_order(self, products: list[Product]):
        async with self.db.async_session() as session:
            await session.commit()
