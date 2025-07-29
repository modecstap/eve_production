from pydantic import BaseModel, validator


class DbConfig(BaseModel):
    user: str
    password: str | None
    host: str
    port: int
    db_name: str
