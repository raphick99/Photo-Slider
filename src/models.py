from pydantic import BaseModel


class RuntimeConfig(BaseModel):
    display_time: float


class PhotoResponse(BaseModel):
    photo_url: str
