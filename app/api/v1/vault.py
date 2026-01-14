from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.models import User
from app.api import deps
from app.schemas.vault import (
    VaultEntryCreate, 
    VaultEntryRead, 
    VaultEntryDecrypted, 
    VaultRevealRequest,
    PasswordHealthCheck,
    PasswordHealthResponse
)
from app.services import vault_service, health_service, pwned_service

router = APIRouter()

@router.post("/", response_model=VaultEntryRead)
def create_entry(
    entry: VaultEntryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return vault_service.create_vault_entry(db, entry, current_user.id)

@router.get("/", response_model=List[VaultEntryRead])
def list_entries(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    List vault entries for current user.
    """
    return vault_service.list_vault_entries(db, current_user.id, skip, limit)

@router.post("/{entry_id}/reveal", response_model=VaultEntryDecrypted)
def reveal_password(
    entry_id: int, 
    request: VaultRevealRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retrieve and decrypt a specific password.
    Ensures user owns the entry.
    """
    entry = vault_service.get_vault_entry(db, entry_id, request.master_password, current_user.id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found or decryption failed")
    return entry

@router.post("/check-health", response_model=PasswordHealthResponse)
async def check_health(
    check: PasswordHealthCheck,
    current_user: User = Depends(deps.get_current_user) # Optional: Can be public or protected
):
    """
    Analyze password strength.
    """
    strength = health_service.check_password_strength(check.password)
    pwned_count = await pwned_service.check_pwned_password(check.password)
    
    return {
        "score": strength["score"],
        "feedback": strength["feedback"],
        "is_pwned": pwned_count > 0,
        "pwned_count": pwned_count
    }
