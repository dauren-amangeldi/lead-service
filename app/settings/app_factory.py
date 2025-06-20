import logging
import asyncio

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.endpoints import endpoints
from app.settings.config import settings
from app.settings.http_client import http_client

logging.basicConfig(level=logging.INFO)

class AppFactory:
    def __init__(self, settings, http_client):
        self.settings = settings
        self.app = FastAPI(
            title=self.settings.PROJECT_NAME,
            root_path=self.settings.WWW_DOMAIN if self.settings.config_name in ["DEV", "PROD"] else "",
            version=self.settings.VERSION,
            description=self.settings.DESCRIPTION,
            openapi_url="/%sec%openapi.json" if self.settings.config_name == "PROD" else "/openapi.json",
            docs_url="/%sec%/docs" if self.settings.config_name == "PROD" else "/docs",
            redoc_url="/%sec%/redoc" if self.settings.config_name == "PROD" else "/redoc",
            debug=True,
        )
        self.http_client = http_client
    
    async def startup_event(self):
        pass

    async def http_startup(self):
        await self.http_client.start()
    
    async def http_shutdown(self):
        await self.http_client.stop()

    def get_app(self) -> FastAPI:
        self.app.add_event_handler("startup", self.startup_event)

        routes = APIRouter()

        """ This events you can add if you want to use async http_client """

        @routes.on_event("startup")
        async def startup():
            logging.info("Async session started.")
            await self.http_startup()

        @routes.on_event("shutdown")
        async def shutdown():
            logging.info("Closing async session.")
            await self.http_shutdown()

        routes.include_router(endpoints.router)

        self.app.include_router(routes)

        @self.app.exception_handler(RequestValidationError)
        async def custom_form_validation_error(request, exc):
            error_text = None  # По умолчанию устанавливаем значение None
            for pydantic_error in exc.errors():
                loc, msg = pydantic_error["loc"], pydantic_error["msg"]
                filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc

                try:
                    field_string = ".".join([str(x) for x in filtered_loc])  # nested fields with dot-notation
                except Exception:
                    field_string = "unknown_field"

                # Создаем строку с ошибками
                error_str = f"{field_string}: {msg}"

                # Объединяем все ошибки в одну строку
                if error_text is None:
                    error_text = error_str
                else:
                    error_text += f"\n{error_str}"
            response_data = {"errorText": error_text, "success": False}

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=response_data,
            )

        @self.app.exception_handler(TypeError)
        async def handle_enum_type_error(request, exc):
            """Handle TypeError: EnumMeta.__call__() missing 1 required positional argument: 'value'"""
            error_text = "A TypeError occurred while processing the request. Please check your input data."
            response_data = {"errorText": error_text, "success": False}
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response_data)

        return self.app

factory = AppFactory(settings, http_client=http_client)
app = factory.get_app()
