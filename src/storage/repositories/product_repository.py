from decimal import Decimal

from sqlalchemy import text, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.repositories.base import BaseRepository
from src.storage.repositories.wrappers import ensure_session
from src.storage.tables import Product, UsedTransactionList, Transaction, TypeInfo


class ProductRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Product

    @ensure_session
    async def insert_with_used_transaction(self, products: list[Product], session: AsyncSession = None):
        session.add_all(products)
        await session.flush()
        for product in products:
            create_used_transaction = text(f"""
            DO $$ 
            DECLARE
                r_material_id INTEGER;
                r_material_need_count INTEGER;
            
                r_transaction_id INTEGER;
                r_transaction_remains INTEGER;
            
                r_used_count INTEGER;
                r_remaining_need INTEGER;
                r_remaining_remains INTEGER;
                input_product_id INTEGER;
                blueprint_efficiency NUMERIC;
                material_efficiency NUMERIC;
            BEGIN
                input_product_id := {product.id}; 
            
                SELECT p.blueprint_efficiency, s.material_efficiency 
                INTO blueprint_efficiency, material_efficiency
                FROM product p 
                JOIN station s ON p.station_id = s.id
                WHERE p.id = input_product_id;
            
                FOR r_material_id, r_material_need_count IN 
                    SELECT material_id, need_count FROM material_list 
                    WHERE need_count > 0 AND type_id = (SELECT type_id FROM product WHERE id = input_product_id)
                LOOP
                    r_remaining_need := ROUND(r_material_need_count * blueprint_efficiency * material_efficiency);
            
                    FOR r_transaction_id, r_transaction_remains IN 
                        SELECT id, remains FROM transactions
                        WHERE material_id = r_material_id AND remains > 0
                        ORDER BY release_date
                    LOOP
                        IF r_remaining_need > 0 THEN
                            IF r_transaction_remains >= r_remaining_need THEN
                                r_used_count := r_remaining_need;
                                r_remaining_remains := r_transaction_remains - r_used_count;
                                r_remaining_need := 0;
                            ELSE
                                r_used_count := r_transaction_remains;
                                r_remaining_remains := 0;
                                r_remaining_need := r_remaining_need - r_used_count;
                            END IF;
            
                            INSERT INTO used_transaction_list (product_id, transaction_id, used_count)
                            VALUES (input_product_id, r_transaction_id, r_used_count)
                            ON CONFLICT (product_id, transaction_id) DO NOTHING;
            
                            UPDATE transactions
                            SET remains = r_remaining_remains
                            WHERE id = r_transaction_id;
                        END IF;
                    END LOOP;
                END LOOP;
            END $$;
            """)
            await session.execute(create_used_transaction)
        await session.commit()

    @ensure_session
    async def calculate_material_cost(
            self,
            material_id: int,
            need_count: int,
            session: AsyncSession = None
    ) -> Decimal:
        
            query = text("""
                SELECT calculate_material_cost(:p_material_id, :p_need_count)
            """)

            result = await session.execute(query, {
                'p_material_id': material_id,
                'p_need_count': need_count
            })

            material_cost = result.scalar()
            return Decimal(material_cost) if material_cost is not None else Decimal('0.00')


    async def get_products_without_order(self, session: AsyncSession = None) -> list[Product]:
        
            products = await session.execute(
                select(self._entity)
                .where(
                    self._entity.order == None
                )
            )
            return products.scalars().all()

    @ensure_session
    async def get_products_without_order_by_type(self, type_id: int, session: AsyncSession = None) -> list[Product]:
        
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

    @ensure_session
    async def get_products_costs(self, products_id: list[int], session: AsyncSession = None):
        
            products_costs = await session.execute(
                select(
                    Product.id,
                    TypeInfo.name,
                    Product.production_date,
                    func.sum(UsedTransactionList.used_count * Transaction.price).label("product_cost")
                )
                .join(UsedTransactionList)
                .join(Transaction)
                .join(TypeInfo)
                .where(Product.id.in_(products_id))
                .group_by(Product.id, TypeInfo.name, Product.production_date)
            )
            return products_costs.all()

