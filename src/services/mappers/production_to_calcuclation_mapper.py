from src.services.corrected_material.material_calculation_model import MaterialCalculationModel
from src.services.production_materials_calculator.production_materials_payload import ProductionMaterialsPayload


class ProductionToCalculatorMapper:
    def map(self, material_count: int, payload: ProductionMaterialsPayload) -> MaterialCalculationModel:
        return MaterialCalculationModel(
            material_count=material_count,
            blueprint_efficiency=payload.blueprint_efficiency,
            material_efficiency=payload.station_material_efficiency,
            product_count=payload.product_count,
        )
