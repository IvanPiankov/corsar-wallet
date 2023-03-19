import logging

import inject
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.repositories.users_repository import UserRepository
from routers.system_routes import system_router
from routers.users import auth_router
from services.auth_service import AuthService
from settings import Settings
from utils.exception_handler import set_custom_exception

app = FastAPI()
set_custom_exception(app)
app.include_router(system_router)
app.include_router(auth_router)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



engine: AsyncEngine | None = None


def config(binder: inject.Binder):
    global engine
    global engine

    engine = create_async_engine(
        Settings.get_pg_url()
    )

    user_repo = UserRepository(engine)
    auth_service = AuthService(user_repo)

    binder.bind(UserRepository, user_repo)
    binder.bind(AuthService, auth_service)


@app.on_event("startup")
async def startup_event() -> None:
    inject.configure(config, bind_in_runtime=False)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logging.info("Shutting down...")
    await engine.dispose()
