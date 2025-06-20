import aiohttp
from typing import Dict, Any

from app.consumers.consumer import Consumer
from app.settings.config import settings

class TelegramConsumer(Consumer):
    def __init__(self):
        self.api_token = settings.TELEGRAM_API
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.api_token}"

    async def send_data(self, data: Dict[str, Any]) -> None:
        message = self._format_message(data)
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/sendMessage"
            params = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            async with session.post(url, params=params) as response:
                await response.json()

    def _format_message(self, data: Dict[str, Any]) -> str:
        message = "🔔 <b>New Lead</b>\n\n"
        for key, value in data.items():
            message += f"<b>{key}:</b> {value}\n"
        return message 