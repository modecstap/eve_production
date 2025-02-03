from aiohttp import web

from src.config import Settings
from src.server.handlers import TestHandler, TransactionHandler, OrderHandler, ProductHandler, TypeHandler, \
    MaterialHandler, StationHandler
from src.server.middlewares import Middlewares


class MainServer:
    def __init__(self):
        self.config = Settings().config.server_config

        self.app = web.Application()
        self.runner = None

        self._setup_middlewares()
        self._setup_handlers()

    async def start(self):
        self._setup_routs()

        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.config.host, self.config.port)
        print('started')
        await site.start()

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()
            print(f'Server stopped at http://{self.config.host}:{self.config.port}')

    def _setup_handlers(self):
        self.test_handler = TestHandler()
        self.transaction_handler = TransactionHandler()
        self.order_handler = OrderHandler()
        self.product_handler = ProductHandler()
        self.type_handler = TypeHandler()
        self.material_handler = MaterialHandler()
        self.station_handler = StationHandler()

    def _setup_middlewares(self):
        middlewares = Middlewares()

        self.app.middlewares.append(middlewares.CORS_middlevare)
        self.app.middlewares.append(middlewares.response_status)
        self.app.middlewares.append(middlewares.model_type)

    def _setup_routs(self):
        self.app.router.add_get("/api/test/ping", self.test_handler.ping)
        self.app.router.add_route("OPTIONS", "/{tail:.*}", self.test_handler.preflight_handler)

        self._setup_transaction_routs()
        self._setup_order_routs()
        self._setup_product_routs()
        self._setup_type_routs()
        self._setup_material_routs()
        self._setup_station_routs()

    def _setup_transaction_routs(self):
        self.app.router.add_get("/api/transaction/get_transactions", self.transaction_handler.get_transactions)
        self.app.router.add_get("/api/transaction/get_available_materials",
                                self.transaction_handler.get_available_materials)
        self.app.router.add_post("/api/transaction/add_transactions", self.transaction_handler.add_transactions)

    def _setup_order_routs(self):
        self.app.router.add_get("/api/order/get_orders", self.order_handler.get_orders)
        self.app.router.add_post("/api/order/add_order", self.order_handler.add_order)
        self.app.router.add_post("/api/order/change_order_status", self.order_handler.change_order_status)

    def _setup_product_routs(self):
        self.app.router.add_get("/api/product/get_products", self.product_handler.get_products)
        self.app.router.add_get("/api/product/get_available_products",
                                self.product_handler.get_available_products)
        self.app.router.add_post("/api/product/create_products", self.product_handler.create_products)

    def _setup_type_routs(self):
        self.app.router.add_get("/api/type_info/get_types", self.type_handler.get_types)

    def _setup_material_routs(self):
        self.app.router.add_get("/api/material/get_materials", self.material_handler.get_materials)

    def _setup_station_routs(self):
        self.app.router.add_get("/api/station/get_stations", self.station_handler.get_stations)
