import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.server_config import ServerConfig
from src.server.handlers import OrderHandler, TestHandler, TransactionHandler, ProductHandler, TypeHandler, \
    StationHandler, ProductionHandler, AvailableMaterialHandler, MaterialListHandler, CostCalculatorHandler
from src.server.handlers.entity_handlers.entity_handler import EntityHandler
from src.server.handlers.entity_handlers.used_transaction_handler import UsedTransactionHandler
from src.server.routers import CRUDRouter, OrdersRouter, AvailableMaterialsRouter, CostCalculatorRouter, \
    ProductionsRouter, EntityPrefix


class FastAPIServer:
    def __init__(self, config: ServerConfig):
        self._config = config
        self.app = FastAPI()
        self.server: uvicorn.Server = None

        self._setup_cors()
        self._setup_handlers()
        self._setup_routes()

    def _setup_cors(self):
        origins = [
            "https://eve-production.my-shield.ru"
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_handlers(self):
        self.test_handler = TestHandler()
        self.ENTITY_ROUTES: dict[EntityPrefix, EntityHandler] = {
            EntityPrefix.TRANSACTIONS: TransactionHandler(),
            EntityPrefix.ORDERS: OrderHandler(),
            EntityPrefix.USED_TRANSACTIONS: UsedTransactionHandler(),
            EntityPrefix.MATERIALS_LIST: MaterialListHandler(),
            EntityPrefix.PRODUCTS: ProductHandler(),
            EntityPrefix.TYPES: TypeHandler(),
            EntityPrefix.STATIONS: StationHandler(),
        }
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

    def _setup_routes(self):
        self.app.get("/api/test/ping")(self.test_handler.ping)
        self.app.options("/{tail:.*}")(self.test_handler.preflight_handler)

        self._include_crud_routes()
        self.app.include_router(OrdersRouter().router)
        self.app.include_router(AvailableMaterialsRouter().router)
        self.app.include_router(CostCalculatorRouter().router)
        self.app.include_router(ProductionsRouter().router)

    def _include_crud_routes(self):
        for prefix, handler in self.ENTITY_ROUTES.items():
            self.app.include_router(CRUDRouter(prefix.value, handler).router)
