from pydantic import BaseModel

from src.config.db_config import DbConfig
from src.config.server_config import ServerConfig


class Config(BaseModel):
    db_config: DbConfig
    server_config: ServerConfig
