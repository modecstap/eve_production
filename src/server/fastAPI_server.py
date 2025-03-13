import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import Settings
from src.server.handlers import OrderHandler, TestHandler, TransactionHandler, ProductHandler, TypeHandler, \
    MaterialHandler, StationHandler


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
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_handlers(self):
        self.test_handler = TestHandler()
        self.transaction_handler = TransactionHandler()
        self.order_handler = OrderHandler()
        self.product_handler = ProductHandler()
        self.type_handler = TypeHandler()
        self.material_handler = MaterialHandler()
        self.station_handler = StationHandler()

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

        self._setup_transaction_routs()
        self._setup_order_routs()
        self._setup_product_routs()
        self._setup_type_routs()
        self._setup_material_routs()
        self._setup_station_routs()

    def _setup_transaction_routs(self):
        self.app.get("/api/transaction/get_transactions")(self.transaction_handler.get_transactions)
        self.app.get("/api/transaction/get_available_materials")(
            self.transaction_handler.get_available_materials)
        self.app.post("/api/transaction/add_transactions")(self.transaction_handler.add_transactions)

    def _setup_order_routs(self):
        self.app.get("/api/order/get_orders")(self.order_handler.get_orders)
        self.app.post("/api/order/add_order")(self.order_handler.add_order)
        self.app.post("/api/order/change_order_status")(self.order_handler.change_order_status)

    def _setup_product_routs(self):
        self.app.get("/api/product/get_products")(self.product_handler.get_products)
        self.app.get("/api/product/get_available_products")(self.product_handler.get_available_products)
        self.app.post("/api/product/create_products")(self.product_handler.create_products)
        self.app.post("/api/product/get_production_cost")(self.product_handler.calculate_production_cost)

    def _setup_type_routs(self):
        self.app.get("/api/type_info/get_types")(self.type_handler.get_types)

    def _setup_material_routs(self):
        self.app.get("/api/material/get_materials")(self.material_handler.get_materials)

    def _setup_station_routs(self):
        self.app.get("/api/station/get_stations")(self.station_handler.get_stations)
