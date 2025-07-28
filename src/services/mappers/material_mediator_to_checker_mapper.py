from src.services.available_material.available_material_model import AvailableMaterialModel
from src.services.chekers.material_checker.material_checker_mediator_payload import MaterialCheckerMediatorPayload
from src.services.chekers.material_checker.material_checker_payload import MaterialCheckerPayload


class MaterialMediatorToCheckerMapper:
    def __init__(
            self,
            required_materials: MaterialCheckerMediatorPayload,
            available_materials: list[AvailableMaterialModel]
    ):
        self._required_materials = required_materials
        self._available_materials = available_materials

    def map(self) -> MaterialCheckerPayload:
        available_materials: dict[int, int] = dict()
        for available_material in self._available_materials:
            available_materials[available_material.material_id] = available_material.count

        return MaterialCheckerPayload(
            required_materials=self._required_materials.required_materials,
            available_materials=available_materials
        )
