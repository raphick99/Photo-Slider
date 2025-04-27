from pydantic import BaseModel


class RuntimeConfig(BaseModel):
	refresh_interval: float
