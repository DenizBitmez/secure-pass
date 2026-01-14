from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShareCreate(BaseModel):
    content: str
    ttl_minutes: int = 60 # Default to 1 hour (if not read)

class ShareResponse(BaseModel):
    uuid: str
    share_url: str
    secret_key: str # The key needed to decrypt, returned ONCE
    expires_at: datetime

class ShareContentResponse(BaseModel):
    encrypted_content: str
    # Client must assume responsibility to decrypt this using the key they have
    warning: str = "This message has been destroyed from the server."
