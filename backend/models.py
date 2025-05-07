from pydantic import BaseModel


class RuntimeConfig(BaseModel):
    display_time: float
