from collections import defaultdict

from src.services.AService import Service
from src.services.corrected_material.corrected_material_calculator import CorrectedMaterialCalculator
from src.services.corrected_material.material_calculation_model import MaterialCalculationModel
from src.services.production_materials_calculator.production_materials import ProductionMaterials
from src.services.production_materials_calculator.production_materials_payload import ProductionMaterialsPayload


class ProductionMaterialsCalculator(Service):

    def __init__(
            self,
            calculator: CorrectedMaterialCalculator = CorrectedMaterialCalculator()
    ):
        self._calculator = calculator

    async def do(self, model: ProductionMaterialsPayload) -> ProductionMaterials:
        required_materials: dict[int, int] = defaultdict(lambda: 0)

        for id_, count in model.materials.items():
            calculation_model = MaterialCalculationModel(
                material_count=count,
                blueprint_efficiency=model.blueprint_efficiency,
                material_efficiency=model.station_material_efficiency,
                product_count=model.product_count,
            )
            calculated_material_model = await self._calculator.do(calculation_model)
            required_materials[id_] += calculated_material_model.calculated_material

        return ProductionMaterials(required_materials=required_materials)