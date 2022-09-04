import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError

from core.errors.error_handler import validation_exception_handler
from core.server.routes import calculate


app = FastAPI()


class Server:

    def __init__(self):
        self.router = APIRouter()
        self._set_error_handler()
        self._register_api()

    def _register_api(self):
        self.router.add_api_route("/calculate", calculate, methods=["POST"])

    def _set_error_handler(self):
        app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def run(self):
        uvicorn.run("core.server.server:app",
                    host="0.0.0.0",
                    port=8000,
                    workers=2,
                    log_level="info")


router = Server().router
app.include_router(router)
