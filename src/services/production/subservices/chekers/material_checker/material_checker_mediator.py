from src.services.production.subservices.available_material.available_material_service import AvailableMaterialsService
from src.services.production.models.reqired_materials import RequiredMaterials
from src.services.production.subservices.chekers.material_checker.material_checker import MaterialChecker


class MaterialCheckerMediator:
    """
    Обеспечивает необходимыми данными MaterialChecker.
    """

    def __init__(
            self,
            available_materials_service=AvailableMaterialsService(),
    ):
        self._available_materials_service = available_materials_service

    async def check(self, required_materials: RequiredMaterials) -> None:
        available_materials = await self._available_materials_service.do()

        await MaterialChecker(required_materials, available_materials).check()
