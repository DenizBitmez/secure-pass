from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class VaultEntryBase(BaseModel):
    site_name: str
    site_url: Optional[str] = None

class VaultEntryCreate(VaultEntryBase):
    site_password: Optional[str] = None
    master_password: Optional[str] = None
    encrypted_password: Optional[str] = None 

class VaultEntryRead(VaultEntryBase):
    id: int
    created_at: datetime
    encrypted_password: Optional[str] = None # Include this so client can decrypt!
    
    class Config:
        from_attributes = True

class VaultEntryDecrypted(VaultEntryRead):
    decrypted_password: str

class VaultRevealRequest(BaseModel):
    master_password: str

class PasswordHealthCheck(BaseModel):
    password: str

class PasswordHealthResponse(BaseModel):
    score: int
    feedback: Optional[list[str]] = None
    is_pwned: bool
    pwned_count: int = 0
