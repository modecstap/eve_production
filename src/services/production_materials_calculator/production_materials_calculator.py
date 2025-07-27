from collections import defaultdict

from src.services.AService import Service
from src.services.corrected_material.corrected_material_calculator import CorrectedMaterialCalculator
from src.services.mappers.production_to_calcuclation_mapper import ProductionToCalculatorMapper
from src.services.production_materials_calculator.production_materials import ProductionMaterials
from src.services.production_materials_calculator.production_materials_payload import ProductionMaterialsPayload


class ProductionMaterialsCalculator(Service):

    def __init__(
            self,
            calculator: CorrectedMaterialCalculator = CorrectedMaterialCalculator(),
            mapper: ProductionToCalculatorMapper = ProductionToCalculatorMapper()
    ):
        self._calculator = calculator
        self._mapper = mapper

    async def do(self, model: ProductionMaterialsPayload) -> ProductionMaterials:
        required_materials: dict[int, int] = defaultdict(lambda: 0)

        for id_, count in model.materials.items():
            calculation_payload = self._mapper.map(material_count=count, payload=model)
            calculated_material_model = await self._calculator.do(calculation_payload)
            required_materials[id_] += calculated_material_model.calculated_material

        return ProductionMaterials(required_materials=required_materials)
