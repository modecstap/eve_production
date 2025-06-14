from collections import defaultdict
from decimal import Decimal, ROUND_UP

from src.server.handlers.models.production_models import ProductionModel
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import MaterialList, Station


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="required_materials",
    )
)
class RequiredMaterialsService:

    def __init__(self):
        self._station_repository = BaseRepository(Station)
        self._material_list_repository = BaseRepository(MaterialList)

    async def get_required_materials(self, production: ProductionModel) -> dict[int, Decimal]:
        required_materials = defaultdict(lambda: Decimal('0'))
        materials_list = await self._material_list_repository.get_entities(
            filters=[MaterialList.type_id == production.type_id]
        )
        station = await self._station_repository.get_entity_by_id(production.station_id)

        for material in materials_list:
            required_materials[material.material_id] += \
                await self._get_corrected_material_count(material, production, station)
        return required_materials

    @staticmethod
    async def _get_corrected_material_count(
            material: MaterialList,
            production: ProductionModel,
            station: Station
    ) -> Decimal:
        return (
                material.need_count
                * production.blueprint_efficiency
                * station.material_efficiency
                * production.count
        ).quantize(Decimal('1.'), rounding=ROUND_UP)
