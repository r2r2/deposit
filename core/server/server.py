import uvicorn
from core.api.api_routes import controllers
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError

from core.errors.error_handler import validation_exception_handler
from settings import settings


class Server:

    def __init__(self):
        self.app = FastAPI()
        self.router = APIRouter(prefix="/api")
        self._set_error_handler()
        self._register_api()

    def _register_api(self):
        for params in controllers:
            self.router.add_api_route(**params)
        self.app.include_router(self.router)

    def _set_error_handler(self):
        self.app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def run(self):
        uvicorn.run("core.server.server:server.app", **settings.uvicorn_config.dict())


server = Server()
