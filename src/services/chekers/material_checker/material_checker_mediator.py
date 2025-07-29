from src.services.available_material.available_material_service import AvailableMaterialsService
from src.services.chekers.checker import Checker
from src.services.chekers.material_checker.material_checker import MaterialChecker
from src.services.chekers.material_checker.material_checker_mediator_payload import MaterialCheckerMediatorPayload
from src.services.mappers.material_mediator_to_checker_mapper import MaterialMediatorToCheckerMapper


class MaterialCheckerMediator(Checker):
    """
    Обеспечивает необходимыми данными MaterialChecker.
    """

    def __init__(
            self,
            check_payload: MaterialCheckerMediatorPayload,
            available_materials_service=AvailableMaterialsService(),
    ):
        self._check_payload = check_payload
        self._available_materials_service = available_materials_service

    async def check(self) -> None:
        required_materials = self._check_payload.required_materials
        available_materials = await self._available_materials_service.do()
        payload = MaterialMediatorToCheckerMapper(required_materials, available_materials).map()
        await MaterialChecker(payload).check()
