from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    totp_secret = Column(String, nullable=True)
    
    vault_entries = relationship("VaultEntry", back_populates="user")

class VaultEntry(Base):
    __tablename__ = "vault_entries"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String, index=True)
    site_url = Column(String, nullable=True)
    encrypted_password = Column(String, nullable=False)
    
    # Link to User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="vault_entries")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SharedSecret(Base):
    __tablename__ = "shared_secrets"

    id = Column(String, primary_key=True, default=generate_uuid)
    encrypted_content = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
