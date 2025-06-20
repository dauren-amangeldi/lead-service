from abc import ABC, abstractmethod
from typing import Dict, Any

class Consumer(ABC):
    @abstractmethod
    async def send_data(self, data: Dict[str, Any]) -> None:
        pass 