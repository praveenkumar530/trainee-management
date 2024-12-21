from typing import List
from fastapi import FastAPI, APIRouter
from app.routers import router_list
from core.database.database_conn import create_connection_pool, close_connection_pool
from core.logging_config import logger


def init_routers(app_:FastAPI, routers: List[APIRouter], prefix:str = "")-> None:
    for router in routers:
        app_.include_router(router, prefix=prefix)

def create_app() -> FastAPI:

    app_ = FastAPI(
        docs_url="/docs",
        redoc_url="/redoc",
    )

    init_routers(app_=app_, routers=router_list, prefix="/gym-management" )

    return app_

gym_management_app = create_app()


@gym_management_app.on_event("startup")
async def startup_event():
    print("app started")
    logger.info("Application started")
    await create_connection_pool()


@gym_management_app.on_event("shutdown")
async def startup_event():
    print("app Ended")
    logger.info("Application stopped")
    await close_connection_pool()


