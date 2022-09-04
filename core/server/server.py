import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from settings import Settings
from core.errors.error_handler import validation_exception_handler
from core.server.api import calculate


class Server:

    def __init__(self):
        self.app = FastAPI()
        self.router = APIRouter()
        self._set_error_handler()
        self._register_api()

    def _register_api(self):
        self.router.add_api_route("/calculate", calculate, methods=["POST"])
        self.app.include_router(self.router)

    def _set_error_handler(self):
        self.app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def run(self):
        uvicorn.run("core.server.server:server.app", **Settings().uvicorn_config.dict())


server = Server()
