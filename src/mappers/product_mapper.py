from src.mappers import BaseMapper
from src.server.handlers.models import ProductModel, AvailableProductModel
from src.storage.tables import Product


class ProductMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = ProductModel
        self._entity_type = Product

    def product_cost_to_model(self, entity) -> AvailableProductModel:
        return AvailableProductModel(
            name=entity.name,
            production_date=entity.production_date,
            product_cost=entity.product_cost
        )

    def products_costs_to_models(self, entities):
        return [self.product_cost_to_model(entity) for entity in entities]
