from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

import aiohttp
from aiohttp import ClientSession


@dataclass
class HttpClient:
    """Асинхронный HTTP клиент с поддержкой повторов и очередности запросов."""

    _session: ClientSession | None = None

    async def start(self) -> None:
        """Инициализирует HTTP-сессию."""
        if self._session is None:
            self._session = ClientSession()

    async def stop(self) -> None:
        """Закрывает HTTP-сессию."""
        if self._session:
            await self._session.close()
            self._session = None

    async def fetch_with_retry(
        self,
        url: str,
        method: str = "GET",
        retries: int = 3,
        timeout: int = 60,
        headers: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
    ):
        """
        Выполняет HTTP-запрос с заданным числом повторов в случае ошибки.

        Args:
            url (str): URL для запроса.
            method (str): HTTP-метод (GET, POST и т. д.).
            retries (int): Количество повторов в случае ошибки.
            timeout (int): Тайм-аут запроса в секундах.
            headers (Optional[Dict[str, str]]): Заголовки для запроса.
            json_data (Optional[Dict[str, Any]]): JSON-данные для отправки.

        Returns:
            bytes: Тело ответа.

        Raises:
            Exception: Последняя ошибка, если все попытки завершились неудачей.
        """
        assert self._session is not None, "HTTP-сессия не инициализирована. Вызовите start перед использованием."
        for attempt in range(1, retries + 1):
            try:
                async with self._session.request(
                    method,
                    url,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    headers=headers,
                    json=json_data,
                ) as response:
                    response.raise_for_status()
                    return await response.read()
            except Exception as e:
                if attempt == retries:
                    raise e
                await asyncio.sleep(2**attempt)  # Экспоненциальная задержка

    @property
    def session(self) -> ClientSession:
        """Возвращает текущую HTTP-сессию."""
        assert self._session is not None, "HTTP-сессия не инициализирована. Вызовите start перед использованием."
        return self._session


http_client = HttpClient()


def get_http_client() -> HttpClient:
    return http_client