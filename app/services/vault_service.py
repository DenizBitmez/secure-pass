from sqlalchemy.orm import Session
from app.db.models import VaultEntry
from app.schemas.vault import VaultEntryCreate
from app.core.crypto import encrypt_password, decrypt_password

def create_vault_entry(db: Session, entry: VaultEntryCreate, user_id: int) -> VaultEntry:
    encrypted_data = encrypt_password(entry.master_password, entry.site_password)
    
    db_entry = VaultEntry(
        site_name=entry.site_name,
        site_url=entry.site_url,
        encrypted_password=encrypted_data,
        user_id=user_id
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_vault_entry(db: Session, entry_id: int, master_password: str, user_id: int) -> dict:
    db_entry = db.query(VaultEntry).filter(
        VaultEntry.id == entry_id,
        VaultEntry.user_id == user_id
    ).first()
    
    if not db_entry:
        return None
    
    # Decrypt
    try:
        decrypted_pwd = decrypt_password(master_password, db_entry.encrypted_password)
    except Exception:
        return None

    return {
        "id": db_entry.id,
        "site_name": db_entry.site_name,
        "site_url": db_entry.site_url,
        "created_at": db_entry.created_at,
        "decrypted_password": decrypted_pwd
    }

def list_vault_entries(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(VaultEntry).filter(
        VaultEntry.user_id == user_id
    ).offset(skip).limit(limit).all()
