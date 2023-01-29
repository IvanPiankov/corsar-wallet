from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

system_router = APIRouter(prefix="/system", tags=["System Route"])


@system_router.get("/check", description="Check work services")
async def check_health():
    return ORJSONResponse({"status": "ok"})

