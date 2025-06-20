import asyncio
import sys
import os
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.settings.database import SessionLocal, engine
from app.settings.config import settings
from app.enums.server_status import ServerStatusEnum
from app.enums.lead_status import LeadStatusEnum
from app.models.server_configs import ServerConfigs
from app.models.lead import Lead
from app.consumers.telegram_consumer import TelegramConsumer


async def send_lazy_data():
    """
    Send the first lazy data (earliest created/updated lead with status_id == 2) 
    to all consumers if POLLING_STATUS is ACTIVE (status_id == 1) in server_configs table.
    """
    async with SessionLocal() as db:
        try:
            # Check if POLLING_STATUS is ACTIVE
            stmt = select(ServerConfigs).where(
                ServerConfigs.name == "POLLING_STATUS",
                ServerConfigs.keyword == "main"
            )
            result = await db.execute(stmt)
            server_config = result.scalar_one_or_none()

            if not server_config or server_config.status_id != ServerStatusEnum.ACTIVE:
                print("POLLING_STATUS is not ACTIVE. No action taken.")
                return

            # Find the first (earliest) lazy lead
            stmt = select(Lead).where(
                Lead.status_id == LeadStatusEnum.LAZY
            ).order_by(asc(Lead.created_at), asc(Lead.updated_at)).limit(1)
            
            result = await db.execute(stmt)
            lazy_lead = result.scalar_one_or_none()

            if not lazy_lead:
                print("No lazy leads found.")
                return

            # Store the lead ID before any operations that might close the session
            lead_id = lazy_lead.id

            # Prepare lead data for consumers
            lead_data_dict = {
                'first_name': lazy_lead.first_name,
                'last_name': lazy_lead.last_name,
                'email': lazy_lead.email,
                'phone': f"{lazy_lead.phonecc}{lazy_lead.phone}",
                'user_ip': lazy_lead.user_ip,
                'aff_sub': lazy_lead.aff_sub,
                'aff_sub2': lazy_lead.aff_sub2,
                'aff_sub3': lazy_lead.aff_sub3,
                'aff_sub4': lazy_lead.aff_sub4
            }

            # Send to all consumers
            telegram_consumer = TelegramConsumer()
            await telegram_consumer.send_data(lead_data_dict)

            # Update lead status to SEND
            lazy_lead.status_id = LeadStatusEnum.SEND
            await db.commit()

            print(f"Successfully sent lazy lead ID {lead_id} to consumers.")

        except Exception as e:
            print(f"Error in send_lazy_data: {str(e)}")
            await db.rollback()
            raise


async def main():
    """Main function to run send_lazy_data"""
    try:
        await send_lazy_data()
    finally:
        # Ensure the engine is properly closed
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
