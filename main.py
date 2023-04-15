import logging

import inject
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from infrastructure.repositories.accounts import AccountsRepository
from infrastructure.repositories.users import UserRepository
from routers.accounts import accounts_router
from routers.auth import auth_router
from routers.system_routes import system_router
from routers.users import user_router
from services.account_service import AccountsService
from services.auth_service import AuthService
from services.user_service import UserService
from settings import Settings
from utils.exception_handler import set_custom_exception

app = FastAPI()
set_custom_exception(app)
app.include_router(system_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(accounts_router)

# TODO: Придумать, что с ними делать.
origins = ["http://localhost:3000", "http://localhost:8000", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


engine: AsyncEngine


def config(binder: inject.Binder):
    global engine

    engine = create_async_engine(Settings.get_pg_url())

    user_repo = UserRepository(engine)
    accounts_repo = AccountsRepository(engine)
    auth_service = AuthService(user_repo)
    user_service = UserService(user_repo)
    accounts_service = AccountsService(accounts_repo)

    binder.bind(UserRepository, user_repo)
    binder.bind(AccountsRepository, accounts_repo)
    binder.bind(AuthService, auth_service)
    binder.bind(UserService, user_service)
    binder.bind(AccountsService, accounts_service)


@app.on_event("startup")
async def startup_event() -> None:
    inject.configure(config, bind_in_runtime=False)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    global engine
    logging.info("Shutting down...")
    await engine.dispose()
