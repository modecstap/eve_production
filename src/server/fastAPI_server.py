import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import Settings
from src.server.handlers import OrderHandler, TestHandler, TransactionHandler, ProductHandler, TypeHandler, \
    StationHandler, ProductionHandler, AvailableMaterialHandler


class FastAPIServer:
    def __init__(self):
        self._config = Settings().config.server_config
        self.app = FastAPI()
        self.server = None

        self._setup_cors()
        self._setup_handlers()
        self._setup_routs()


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
        self.product_handler = ProductHandler()
        self.type_handler = TypeHandler()
        self.station_handler = StationHandler()
        self.production_handler = ProductionHandler()
        self.available_material_handler = AvailableMaterialHandler()


    async def start(self):
        config = uvicorn.Config(self.app, host=self._config.host, port=self._config.port, loop="asyncio")
        self.server = uvicorn.Server(config)
        await self.server.serve()

    async def stop(self):
        if self.server:
            self.server.should_exit = True
            await asyncio.sleep(0.1)  # Даем время для корректного завершения

    def _setup_routs(self):
        self.app.get("/api/test/ping")( self.test_handler.ping)
        self.app.options("/{tail:.*}")(self.test_handler.preflight_handler)

        self._setup_transaction_routes()
        self._setup_order_routes()
        self._setup_product_routes()
        self._setup_type_routes()
        self._setup_station_routes()
        self.setup_production_routes()

    def _setup_transaction_routes(self):
        self.app.get("/api/transactions/")(self.transaction_handler.get_all)
        self.app.get("/api/transactions/{id}")(self.transaction_handler.get)
        self.app.post("/api/transactions/")(self.transaction_handler.create)
        self.app.post("/api/transactions/bulk")(self.transaction_handler.create_bulk)
        self.app.put("/api/transactions/{id}")(self.transaction_handler.update)
        self.app.put("/api/transactions/")(self.transaction_handler.update_bulk)
        self.app.delete("/api/transactions/{id}")(self.transaction_handler.delete)

    def _setup_available_materials(self):
        self.app.get("/api/available_materials")(self.available_material_handler.get_all)

    def _setup_order_routes(self):
        self.app.get("/api/order/get_orders")(self.order_handler.get_orders)
        self.app.post("/api/order/add_order")(self.order_handler.add_order)
        self.app.post("/api/order/update_price")(self.order_handler.update_price)
        self.app.post("/api/order/update_sell_count")(self.order_handler.update_sell_count)

    def _setup_product_routes(self):
        self.app.get("/api/product/get_products")(self.product_handler.get_products)
        self.app.get("/api/product/get_available_products")(self.product_handler.get_available_products)

    def _setup_type_routes(self):
        self.app.get("/api/type_info/get_types")(self.type_handler.get_types)

    def _setup_station_routes(self):
        self.app.get("/api/stations/")(self.station_handler.get_stations)
        self.app.get("/api/stations/{station_id}")(self.station_handler.get_station)
        self.app.post("/api/stations/")(self.station_handler.create_station)
        self.app.post("/api/stations/bulk")(self.station_handler.create_stations)
        self.app.put("/api/stations/{station_id}")(self.station_handler.update_station)
        self.app.put("/api/stations/")(self.station_handler.update_stations)
        self.app.delete("/api/stations/{station_id}")(self.station_handler.delete_station)

    def setup_production_routes(self):
        self.app.post("/api/product/create_products")(self.production_handler.create_products)
        self.app.post("/api/product/get_production_cost")(self.production_handler.calculate_production_cost)