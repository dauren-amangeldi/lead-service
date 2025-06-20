from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.enums.server_status import ServerStatusEnum
from app.schemas.server_config import ServerConfig
from app.schemas.lead import LeadCreate, LeadResponse
from app.services import service
from app.settings.database import get_async_session

router = APIRouter()


@router.get("/health/ready", status_code=status.HTTP_200_OK, tags=["HealthChecks"])
async def health_ready():
    return {"status": "ready"}


@router.get("/health/live", status_code=status.HTTP_200_OK, tags=["HealthChecks"])
async def health_live():
    return {"status": "live"}


@router.post("/shutdown_polling", response_model=ServerConfig, tags=["Polling"])
async def shutdown_polling(
    db: AsyncSession = Depends(get_async_session)
):
    return await service.update_or_create_polling_status(db, status_id=ServerStatusEnum.NOTACTIVE)


@router.post("/start_polling", response_model=ServerConfig, tags=["Polling"])
async def start_polling(
    db: AsyncSession = Depends(get_async_session)
):
    return await service.update_or_create_polling_status(db, status_id=ServerStatusEnum.ACTIVE)


@router.get("/server_configs", response_model=list[ServerConfig], tags=["Server Config"])
async def get_server_configs(
    db: AsyncSession = Depends(get_async_session)
):
    return await service.get_main_server_configs(db)


@router.post(
    "/tracker",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Leads"],
    description="Submit a new lead for processing. The lead will be saved and, if polling is active, sent to configured consumers (Telegram)."
)
async def track_lead(
    lead_data: LeadCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> LeadResponse:
    """
    Submit a new lead for processing.
    
    - If polling is active (status_id != NOTACTIVE), the lead will be saved with status SEND and sent to consumers
    - If polling is not active, the lead will be saved with status LAZY and not sent to consumers
    
    The lead data includes personal information and affiliate tracking parameters.
    """
    client_host = request.client.host if request.client else "unknown"
    lead = await service.handle_lead_data(db, lead_data, client_host)
    return LeadResponse(status="success", lead_id=lead.id)