from pydantic import BaseModel, HttpUrl
from typing import Optional

class URLCreateRequest(BaseModel):
    original_url: HttpUrl  # Validates that the input is a proper URL
    expiration_time: Optional[int] = None  # Optional expiration time in seconds

class URLCreateResponse(BaseModel):
    short_url: str  # The generated short URL to return to the client
