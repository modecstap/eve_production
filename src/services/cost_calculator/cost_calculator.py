from decimal import Decimal

from src.services.AService import Service
from src.services.cost_calculator.cost_model import CostModel
from src.services.cost_calculator.required_materials_model import RequiredMaterialsModel
from src.storage.repositories import BaseRepository
from src.storage.tables import Product


class CostCalculator(Service):
    """
    Считает цену производства продукта.
    """

    def __init__(
            self,
            product_repository: BaseRepository = BaseRepository(Product)
    ):
        self._product_repository = product_repository

    async def do(self, materials_model: RequiredMaterialsModel) -> CostModel:
        materials_cost = {}
        for material_id, required_count in materials_model.required_materials.items():
            materials_cost[material_id] = await self._product_repository.execute_query(
                query="SELECT calculate_material_cost(:p_material_id, :p_need_count)",
                params={"p_material_id": material_id, "p_need_count": required_count}
            )
        production_cost = sum(materials_cost.values(), Decimal(0))
        cost = CostModel(
            materials_cost=materials_cost,
            production_cost=production_cost
        )
        return cost