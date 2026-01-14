from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.share import ShareCreate, ShareResponse, ShareContentResponse
from app.services import share_service

router = APIRouter()

@router.post("/create", response_model=ShareResponse)
def create_share_link(
    entry: ShareCreate,
    db: Session = Depends(get_db)
):
    return share_service.create_shared_secret(db, entry)

@router.get("/{uuid}", response_model=ShareContentResponse)
def access_share_link(
    uuid: str,
    db: Session = Depends(get_db)
):
    """
    Access a shared secret.
    WARNING: This action destroys the secret on the server!
    Returns the encrypted blob. The client must decrypt it using the key fragment from the URL.
    """
    content = share_service.access_shared_secret(db, uuid)
    if not content:
        raise HTTPException(status_code=404, detail="Link expired or already visited.")
    
    return {"encrypted_content": content}
