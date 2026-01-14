import os
import base64
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.db.models import SharedSecret
from app.schemas.share import ShareCreate
from app.core.config import settings

def create_shared_secret(db: Session, entry: ShareCreate) -> dict:
    # 1. Generate Ephemeral Key (never stored)
    key = AESGCM.generate_key(bit_length=256) # 32 bytes
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    # 2. Encrypt Content
    ciphertext = aesgcm.encrypt(nonce, entry.content.encode('utf-8'), None)
    
    # 3. Store (Nonce + Ciphertext)
    # We store nonce inside the blob for simplicity: [Nonce 12][Ciphertext...]
    # Using base64 for DB storage
    final_blob = base64.urlsafe_b64encode(nonce + ciphertext).decode('utf-8')
    
    secret_id = str(os.urandom(8).hex()) # Simple random ID or UUID
    # Actually models.py uses UUID default, let's use that or pass explicit ID.
    # models.py uses `default=generate_uuid` (string).
    
    expires = datetime.utcnow() + timedelta(minutes=entry.ttl_minutes)
    
    db_secret = SharedSecret(
        encrypted_content=final_blob,
        expires_at=expires
    )
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    
    # 4. Return Data
    # The client needs the KEY to decrypt.
    key_b64 = base64.urlsafe_b64encode(key).decode('utf-8')
    
    return {
        "uuid": db_secret.id,
        "share_url": f"{settings.API_V1_STR}/share/{db_secret.id}#{key_b64}",
        "secret_key": key_b64,
        "expires_at": expires
    }

def access_shared_secret(db: Session, secret_id: str) -> str:
    # 1. Find
    secret = db.query(SharedSecret).filter(SharedSecret.id == secret_id).first()
    if not secret:
        return None
    
    # 2. Check Expiry
    if secret.expires_at and secret.expires_at < datetime.utcnow():
        db.delete(secret)
        db.commit()
        return None
        
    # 3. Get Content (Encrypted)
    content = secret.encrypted_content
    
    # 4. DESTROY (Self-Destruct)
    db.delete(secret)
    db.commit()
    
    return content
