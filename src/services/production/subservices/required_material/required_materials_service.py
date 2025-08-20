from src.services.AService import Service
from src.services.production.models.production_info import ProductionInfo
from src.services.production.models.reqired_materials import RequiredMaterials
from src.services.production.subservices.production_materials_calculator.production_materials_calculator import \
    ProductionMaterialsCalculator
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

    async def do(self, production_model: ProductionInfo) -> RequiredMaterials:
        materials_list = await self._material_list_repository.get_entities(
            filters=[MaterialList.type_id == production_model.product_type_id]
        )
        station = await self._station_repository.get_entity_by_id(production_model.station_id)
        production_model.material_efficiency = station.material_efficiency

        materials = {}
        for material_list in materials_list:
            materials[material_list.material_id] = material_list.need_count

        required_materials = await self._calculator.do(
            RequiredMaterials(materials=materials),
            production_model
        )

        return RequiredMaterials(materials=required_materials.required_materials)
