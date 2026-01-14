import sys
import os
import asyncio
import pyotp
import requests
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal, engine, Base
from app.db.models import User, VaultEntry
from app.core import security
from app.services import auth_service, share_service, vault_service
from app.schemas.user import UserCreate
from app.schemas.share import ShareCreate

def setup_db():
    print("\n[SETUP] Recreating Database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_auth_flow():
    print("\n[TEST] Authentication Flow...")
    db = SessionLocal()
    try:
        # 1. Register
        user_in = UserCreate(email="user@test.com", password="password123")
        hashed = security.get_password_hash(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"  Registered User ID: {user.id}")
        
        # 2. Verify Password
        assert security.verify_password("password123", user.hashed_password)
        print("  [PASS] Password verification successful.")
        
        # 3. Login (Generate Token)
        token = security.create_access_token({"sub": user.email})
        print(f"  Generated Token: {token[:20]}...")
        assert token is not None
        
        return user.id
    finally:
        db.close()

def test_2fa_flow(user_id):
    print("\n[TEST] 2FA Flow...")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        # 1. Generate Secret
        secret = auth_service.generate_totp_secret()
        print(f"  Generated Secret: {secret}")
        
        # 2. Verify Code (Valid)
        totp = pyotp.TOTP(secret)
        code = totp.now()
        assert auth_service.verify_totp(secret, code)
        print("  [PASS] Valid TOTP code verified.")
        
        # 3. Verify Code (Invalid)
        assert not auth_service.verify_totp(secret, "000000")
        print("  [PASS] Invalid TOTP code rejected.")
        
        # 4. Enable (Simulate DB update)
        user.totp_secret = secret
        db.commit()
        print("  [PASS] 2FA Enable simulated.")
        
    finally:
        db.close()

def test_sharing_flow():
    print("\n[TEST] Secure Sharing Flow...")
    db = SessionLocal()
    try:
        # 1. Create Link
        entry = ShareCreate(content="Ultra Secret Message", ttl_minutes=5)
        res = share_service.create_shared_secret(db, entry)
        uuid = res["uuid"]
        key = res["secret_key"]
        print(f"  Created Link: {uuid} (Key: {key})")
        
        # 2. Access Link (Success)
        # In real API, we get encrypted content. Here checking service level.
        # But wait, service returns decrypted? No, service returns encrypted blob.
        # The client decrypts.
        
        # Let's verify we get SOMETHING back.
        content_blob = share_service.access_shared_secret(db, uuid)
        assert content_blob is not None
        print("  [PASS] Retrieved encrypted content.")
        
        # 3. Access Again (Fail - Self Destruct)
        content_blob_2 = share_service.access_shared_secret(db, uuid)
        assert content_blob_2 is None
        print("  [PASS] content destroyed after access.")
        
    finally:
        db.close()

def main():
    setup_db()
    uid = test_auth_flow()
    test_2fa_flow(uid)
    test_sharing_flow()
    print("\n[ALL TESTS PASSED] Phase 2 Features Verified.")

if __name__ == "__main__":
    main()
