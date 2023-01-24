import logging

import inject
from fastapi import FastAPI

from routers.system_routes import system_router

app = FastAPI()
app.include_router(system_router)


def config(binder: inject.Binder):
    pass


@app.on_event("startup")
async def startup_event() -> None:
    inject.configure(config, bind_in_runtime=False)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logging.info("Shutting down...")
