from src.services.AService import Service
from src.services.production_materials_calculator.production_materials_calculator import ProductionMaterialsCalculator
from src.services.production_materials_calculator.production_materials_payload import ProductionMaterialsPayload
from src.services.required_material.required_materials_payload import RequiredMaterialsPayload
from src.services.required_material.required_materials_model import RequiredMaterialsModel
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import MaterialList, Station


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="required_materials",
    )
)
class RequiredMaterialsService(Service):

    def __init__(
            self,
            station_repository: BaseRepository = BaseRepository(Station),
            material_list_repository: BaseRepository = BaseRepository(MaterialList),
            calculator: ProductionMaterialsCalculator = ProductionMaterialsCalculator(),
    ):
        self._station_repository = station_repository
        self._material_list_repository = material_list_repository
        self._calculator = calculator

    async def do(self, production_model: RequiredMaterialsPayload) -> RequiredMaterialsModel:
        materials_list = await self._material_list_repository.get_entities(
            filters=[MaterialList.type_id == production_model.product_type_id]
        )
        station = await self._station_repository.get_entity_by_id(production_model.station_id)
        materials = {}
        for material_list in materials_list:
            materials[material_list.material_id] = material_list.need_count
        payload = ProductionMaterialsPayload(
            materials=materials,
            blueprint_efficiency=production_model.blueprint_efficiency,
            station_material_efficiency=station.material_efficiency,
            product_count=production_model.count
        )

        required_materials = await self._calculator.do(payload)

        return RequiredMaterialsModel(required_materials=required_materials.required_materials)
