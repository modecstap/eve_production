from src.services.chekers.material_checker.material_checker_mediator_payload import MaterialCheckerMediatorPayload
from src.services.required_material.required_materials_model import RequiredMaterialsModel


class RequiredMaterialsToMaterialsCheckerMapper:
    def map(self, model: RequiredMaterialsModel) -> MaterialCheckerMediatorPayload:
        return MaterialCheckerMediatorPayload(
            required_materials=model.required_materials
        )
