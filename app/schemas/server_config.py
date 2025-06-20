from datetime import datetime

from pydantic import BaseModel


class ServerConfigBase(BaseModel):
    name: str
    keyword: str
    status_id: int | None = None


class ServerConfigCreate(ServerConfigBase):
    pass


class ServerConfig(ServerConfigBase):
    id: int

    class Config:
        from_attributes = True 