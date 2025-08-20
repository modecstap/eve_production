from decimal import Decimal

from src.services.production.models.Responces.check_response import CheckResponse
from src.services.production.models.production_info import ProductionInfo
from src.services.production.models.reqired_materials import RequiredMaterials
from src.services.production.production import Production
from src.services.production.models.production_cost import ProductionCostModel


class ProductionHandler:
    async def get_required_materials(
            self,
            product_type_id: int,
            count: int,
            blueprint_efficiency: Decimal,
            station_id: int,
            assembly_cost: Decimal
    ) -> RequiredMaterials:
        payload = ProductionInfo(
            product_type_id=product_type_id,
            count=count,
            blueprint_efficiency=blueprint_efficiency,
            station_id=station_id,
            assembly_cost=assembly_cost
        )
        return await Production(payload).calculate_required_materials()

    async def get_materials_availability(self, payload: ProductionInfo) -> CheckResponse:
        return await Production(payload).chek_materials_availability()

    async def get_production_cost(self, payload: ProductionInfo) -> ProductionCostModel:
        return await Production(payload).calculate_production_cost()

    async def make(self, payload: ProductionInfo) -> None:
        await Production(payload).make_product()