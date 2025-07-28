from src.services.chekers.material_checker.material_checker_mediator_payload import MaterialCheckerMediatorPayload
from src.services.required_material.required_materials_model import RequiredMaterialsModel


class RequiredMaterialsToMaterialsCheckerMapper:
    def __init__(self, model: RequiredMaterialsModel):
        self._model = model

    def map(self) -> MaterialCheckerMediatorPayload:
        return MaterialCheckerMediatorPayload(
            required_materials=self._model.required_materials
        )
