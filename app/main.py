from fastapi import FastAPI
from app.core.logging import configure_logging, get_logger
from app.utils.request_id import RequestIDMiddleware
from app.api.v1.routers import list as list_router, timeseries as ts_router

configure_logging()
logger = get_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(title="Vanda Assessment")

    # Request ID middleware
    app.add_middleware(RequestIDMiddleware)

    # include routers
    app.include_router(list_router.router, prefix="/api/v1", tags=["list"])
    app.include_router(ts_router.router, prefix="/api/v1", tags=["timeseries"])

    @app.on_event("startup")
    async def startup():
        logger.info("Application startup")

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Application shutdown")

    return app

app = create_app()
