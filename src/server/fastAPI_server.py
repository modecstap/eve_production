import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import Settings
from src.server.handlers import OrderHandler, TestHandler, TransactionHandler, ProductHandler, TypeHandler, \
    StationHandler, ProductionHandler, AvailableMaterialHandler, MaterialListHandler, CostCalculatorHandler
from src.server.handlers.entity_handlers.used_transaction_handler import UsedTransactionHandler


class FastAPIServer:
    def __init__(self):
        self._config = Settings().config.server_config
        self.app = FastAPI()
        self.server = None

        self._setup_cors()
        self._setup_handlers()
        self._setup_routes()

    def _setup_cors(self):
        origins = [
            "https://eve-production.my-shield.ru"
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_handlers(self):
        self.test_handler = TestHandler()
        self.transaction_handler = TransactionHandler()
        self.order_handler = OrderHandler()
        self.used_transaction_handler = UsedTransactionHandler()
        self.material_list_handler = MaterialListHandler()
        self.product_handler = ProductHandler()
        self.type_handler = TypeHandler()
        self.station_handler = StationHandler()
        self.production_handler = ProductionHandler()
        self.cost_calculator_handler = CostCalculatorHandler()
        self.available_material_handler = AvailableMaterialHandler()

    async def start(self):
        config = uvicorn.Config(self.app, host=self._config.host, port=self._config.port, loop="asyncio")
        self.server = uvicorn.Server(config)
        await self.server.serve()

    async def stop(self):
        if self.server:
            self.server.should_exit = True
            await asyncio.sleep(0.1)  # Даем время для корректного завершения

    def _setup_routes(self):
        self.app.get("/api/test/ping")(self.test_handler.ping)
        self.app.options("/{tail:.*}")(self.test_handler.preflight_handler)

        self._setup_transaction_routes()
        self._setup_order_routes()
        self._setup_product_routes()
        self._setup_material_list_routes()
        self._setup_type_routes()
        self._setup_available_materials_routes()
        self._setup_station_routes()
        self._setup_used_transaction_routes()
        self.setup_production_routes()

    def _setup_transaction_routes(self):
        self.app.get("/api/transactions/")(self.transaction_handler.get_all)
        self.app.get("/api/transactions/{id}")(self.transaction_handler.get)
        self.app.post("/api/transactions/")(self.transaction_handler.create)
        self.app.post("/api/transactions/bulk")(self.transaction_handler.create_bulk)
        self.app.put("/api/transactions/{id}")(self.transaction_handler.update)
        self.app.put("/api/transactions/")(self.transaction_handler.update_bulk)
        self.app.delete("/api/transactions/{id}")(self.transaction_handler.delete)

    def _setup_order_routes(self):
        self.app.get("/api/orders/")(self.order_handler.get_all)
        self.app.get("/api/orders/{id}")(self.order_handler.get)
        self.app.post("/api/orders/")(self.order_handler.create)
        self.app.post("/api/orders/bulk")(self.order_handler.create_bulk)
        self.app.put("/api/orders/{id}")(self.order_handler.update)
        self.app.put("/api/orders/{id}/sell_count")(self.order_handler.update_sell_count)
        self.app.put("/api/orders/{id}/update_price")(self.order_handler.update_price)
        self.app.put("/api/orders/")(self.order_handler.update_bulk)
        self.app.delete("/api/orders/{id}")(self.order_handler.delete)

    def _setup_material_list_routes(self):
        self.app.get("/api/material_list/")(self.material_list_handler.get_all)
        self.app.get("/api/material_list/{id}")(self.material_list_handler.get)
        self.app.post("/api/material_list/")(self.material_list_handler.create)
        self.app.post("/api/material_list/bulk")(self.material_list_handler.create_bulk)
        self.app.put("/api/material_list/{id}")(self.material_list_handler.update)
        self.app.put("/api/material_list/")(self.material_list_handler.update_bulk)
        self.app.delete("/api/material_list/{id}")(self.material_list_handler.delete)

    def _setup_used_transaction_routes(self):
        self.app.get("/api/used_transaction/")(self.used_transaction_handler.get_all)
        self.app.get("/api/used_transaction/{id}")(self.used_transaction_handler.get)
        self.app.post("/api/used_transaction/")(self.used_transaction_handler.create)
        self.app.post("/api/used_transaction/bulk")(self.used_transaction_handler.create_bulk)
        self.app.put("/api/used_transaction/{id}")(self.used_transaction_handler.update)
        self.app.put("/api/used_transaction/")(self.used_transaction_handler.update_bulk)
        self.app.delete("/api/used_transaction/{id}")(self.used_transaction_handler.delete)

    def _setup_product_routes(self):
        self.app.get("/api/products/")(self.product_handler.get_all)
        self.app.get("/api/products/{id}")(self.product_handler.get)
        self.app.post("/api/products/")(self.product_handler.create)
        self.app.post("/api/products/bulk")(self.product_handler.create_bulk)
        self.app.put("/api/products/{id}")(self.product_handler.update)
        self.app.put("/api/products/")(self.product_handler.update_bulk)
        self.app.delete("/api/products/{id}")(self.product_handler.delete)

    def _setup_type_routes(self):
        self.app.get("/api/types/")(self.type_handler.get_all)
        self.app.get("/api/types/{id}")(self.type_handler.get)
        self.app.post("/api/types/")(self.type_handler.create)
        self.app.post("/api/types/bulk")(self.type_handler.create_bulk)
        self.app.put("/api/types/{id}")(self.type_handler.update)
        self.app.put("/api/types/")(self.type_handler.update_bulk)
        self.app.delete("/api/types/{id}")(self.type_handler.delete)

    def _setup_station_routes(self):
        self.app.get("/api/stations/")(self.station_handler.get_all)
        self.app.get("/api/stations/{id}")(self.station_handler.get)
        self.app.post("/api/stations/")(self.station_handler.create)
        self.app.post("/api/stations/bulk")(self.station_handler.create_bulk)
        self.app.put("/api/stations/{id}")(self.station_handler.update)
        self.app.put("/api/stations/")(self.station_handler.update_bulk)
        self.app.delete("/api/stations/{id}")(self.station_handler.delete)

    def setup_production_routes(self):
        self.app.post("/api/product/create_products")(self.production_handler.create_products)

    def setup_cost_calculator_routes(self):
        self.app.post("/api/cost_calculator")(self.cost_calculator_handler.calculate_production_cost)

    def _setup_available_materials_routes(self):
        self.app.get("/api/available_materials")(self.available_material_handler.get_all)
