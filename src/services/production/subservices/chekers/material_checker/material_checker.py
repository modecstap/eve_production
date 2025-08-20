from src.services.production.models.available_materials import AvailableMaterials
from src.services.production.models.reqired_materials import RequiredMaterials
from src.services.production.subservices.chekers.checker import Checker
from src.services.exceptions import NotEnoughMaterialsException


class MaterialChecker(Checker):
    """
    Проверяет, что доступных материалов больше чем требуемых.
    В обратном случае возвращает ошибку с указанием количества недостающих материалов
    """

    def __init__(
            self,
            required_materials: RequiredMaterials,
            available_materials: AvailableMaterials
    ):
        self._required_materials = required_materials.required_materials
        self._available_materials = available_materials.materials

    async def check(self):
        missing_materials: dict[int, int] = dict()

        for material_id, required_count in self._required_materials.items():
            available_count = self._available_materials.get(material_id)
            if required_count > available_count:
                missing_materials[material_id] = required_count - available_count
        if missing_materials:
            raise NotEnoughMaterialsException(missing_materials)
