from src.services.chekers.checker import Checker
from src.services.chekers.material_checker.material_checker_payload import MaterialCheckerPayload
from src.services.exceptions import NotEnoughMaterialsException


class MaterialChecker(Checker):
    """
    Проверяет, что доступных материалов больше чем требуемых.
    В обратном случае возвращает ошибку с указанием количества недостающих материалов
    """

    def __init__(self, payload: MaterialCheckerPayload):
        self._payload = payload

    async def check(self):
        missing_materials: dict[int, int] = dict()

        for material_id, required_count in self._payload.required_materials.items():
            available_count = self._payload.available_materials.get(material_id)
            if required_count > available_count:
                missing_materials[material_id] = required_count - available_count
        if missing_materials:
            raise NotEnoughMaterialsException(missing_materials)
