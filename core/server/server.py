import uvicorn
from core.api.api_routes import controllers
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError

from core.errors.error_handler import validation_exception_handler
from settings import settings
from infrastructure.database.database import database


class Server:

    def __init__(self):
        self.app = FastAPI(title="Calculation APP")
        self.router = APIRouter(prefix="/api")
        self._set_error_handler()
        self._set_listeners()
        self._register_api()

    def _register_api(self):
        for params in controllers:
            self.router.add_api_route(**params)
        self.app.include_router(self.router)

    def _set_error_handler(self):
        self.app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def _set_listeners(self):
        self.app.add_event_handler("startup", self.startup)
        self.app.add_event_handler("shutdown", self.shutdown)

    async def startup(self):
        await database.connect()

    async def shutdown(self):
        await database.disconnect()

    def run(self):
        uvicorn.run("core.server.server:server.app", **settings.uvicorn_config.dict())


server = Server()
