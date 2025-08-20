from collections import defaultdict
from decimal import Decimal, ROUND_UP

from src.services.production.models.production_info import ProductionInfo
from src.services.production.models.reqired_materials import RequiredMaterials

class ProductionMaterialsCalculator():

    async def do(
            self,
            materials: RequiredMaterials,
            model: ProductionInfo
    ) -> RequiredMaterials:
        required_materials: dict[int, int] = defaultdict(lambda: 0)

        for id_, count in materials.materials.items():
            calculated_material_model = await self._calculate(count, model)
            required_materials[id_] += calculated_material_model.calculated_material

        return RequiredMaterials(materials=required_materials)

    async def _calculate(self, count, model):
        return (
                count
                * model.blueprint_efficiency
                * model.material_efficiency
                * model.product_count
        ).quantize(Decimal('1.'), rounding=ROUND_UP)
