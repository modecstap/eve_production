from src.services import CostCalculatorService
from src.services.mappers import ProductionMapper
from src.storage.tables import Transaction


class ProductionBuilder:
    def __init__(
            self,
            mapper: ProductionMapper = ProductionMapper()
    ):
        self._cost_calculator_service = CostCalculatorService()
        self.mapper = mapper

    async def build(self, production) -> tuple:
        cost = await self._cost_calculator_service.calculate_production_cost(production)
        product = self.mapper.model_to_entity(production)
        transaction = Transaction(
            release_date=production.release_date,
            material_id=production.type_id,
            product_id=product.id,
            count=production.count,
            price=cost,
            remains=production.count
        )
        return product, transaction
