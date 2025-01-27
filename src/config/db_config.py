from pydantic import BaseModel, validator


class DbConfig(BaseModel):
    user: str
    password: str | None
    host: str
    port: int
    db_name: str

    @classmethod
    @validator('port', pre=True)
    def validate_port(cls, value):
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"Cannot convert {value} to an integer")
        return value
