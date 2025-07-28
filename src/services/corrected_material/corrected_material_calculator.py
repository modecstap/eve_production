from decimal import Decimal, ROUND_UP

from src.services.AService import Service
from src.services.corrected_material.calculated_material_model import CalculatedMaterialModel
from src.services.corrected_material.material_calculation_model import MaterialCalculationModel


class CorrectedMaterialCalculator(Service):
    def __init__(self):
        pass

    async def do(self, model: MaterialCalculationModel) -> CalculatedMaterialModel:
        calculated_material = (model.material_count
                               * model.blueprint_efficiency
                               * model.material_efficiency
                               * model.product_count).quantize(Decimal('1.'), rounding=ROUND_UP)
        return CalculatedMaterialModel(calculated_material=int(calculated_material))
