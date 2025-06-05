from src.server.handlers.models.production_models import ProductionModel
from src.services.mappers import BaseMapper
from src.storage.tables import Product


class ProductionMapper(BaseMapper):

    def model_to_entity(self, production: ProductionModel) -> Product:
        return Product(
            station_id=production.station_id,
            blueprint_efficiency=production.blueprint_efficiency
        )
