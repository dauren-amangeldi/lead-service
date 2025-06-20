from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from app.enums.server_status import ServerStatusEnum
from app.enums.lead_status import LeadStatusEnum
from app.models.server_configs import ServerConfigs
from app.models.lead import Lead
from app.schemas.server_config import ServerConfigCreate
from app.schemas.lead import LeadCreate
from app.consumers.telegram_consumer import TelegramConsumer


async def update_or_create_polling_status(db: AsyncSession, status_id: ServerStatusEnum) -> ServerConfigs:
    stmt = select(ServerConfigs).where(
        ServerConfigs.name == "POLLING_STATUS",
        ServerConfigs.keyword == "main"
    )
    result = await db.execute(stmt)
    server_config = result.scalar_one_or_none()

    if server_config:
        server_config.status_id = status_id
    else:
        server_config = ServerConfigs(
            name="POLLING_STATUS",
            keyword="main",
            status_id=status_id
        )
        db.add(server_config)

    await db.commit()
    await db.refresh(server_config)
    return server_config


async def get_main_server_configs(db: AsyncSession) -> list[ServerConfigs]:
    stmt = select(ServerConfigs).where(ServerConfigs.keyword == "main")
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def handle_lead_data(db: AsyncSession, lead_data: LeadCreate, client_host: str) -> Lead:
    # Create lead instance
    lead = Lead(
        first_name=lead_data.first_name,
        last_name=lead_data.last_name,
        email=lead_data.email,
        password=lead_data.password,
        phonecc=lead_data.phonecc,
        phone=lead_data.phone,
        user_ip=client_host,
        aff_sub=lead_data.aff_sub,
        aff_sub2=lead_data.aff_sub2,
        aff_sub3='Immediate Power Pro',
        aff_sub4=lead_data.aff_sub4,
        aff_id='27762',
        offer_id='1737'
    )

    # Check polling status
    stmt = select(ServerConfigs).where(
        ServerConfigs.name == "POLLING_STATUS",
        ServerConfigs.keyword == "main"
    )
    result = await db.execute(stmt)
    server_config = result.scalar_one_or_none()

    if server_config and server_config.status_id == ServerStatusEnum.NOTACTIVE:
        lead.status_id = LeadStatusEnum.LAZY
    else:
        lead.status_id = LeadStatusEnum.SEND
        # Send to consumers
        telegram_consumer = TelegramConsumer()
        lead_data_dict = {
            'first_name': lead.first_name,
            'last_name': lead.last_name,
            'email': lead.email,
            'phone': f"{lead.phonecc}{lead.phone}",
            'user_ip': lead.user_ip,
            'aff_sub': lead.aff_sub,
            'aff_sub2': lead.aff_sub2,
            'aff_sub3': lead.aff_sub3,
            'aff_sub4': lead.aff_sub4
        }
        await telegram_consumer.send_data(lead_data_dict)

    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead 