import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.getcwd())

from app.core.crypto import encrypt_password, decrypt_password, derive_key
from app.services import health_service, pwned_service
from app.db.session import SessionLocal, engine, Base
from app.schemas.vault import VaultEntryCreate
from app.services import vault_service

def test_crypto():
    print("\n[TEST] Testing Core Crypto...")
    master = "secure-master-password"
    secret = "my-secret-data"
    
    # 1. Encrypt
    encrypted = encrypt_password(master, secret)
    print(f"  e.g. Encrypted: {encrypted[:50]}...")
    assert encrypted != secret
    
    # 2. Decrypt
    decrypted = decrypt_password(master, encrypted)
    assert decrypted == secret
    print("  [PASS] Encryption/Decryption round-trip success.")

    # 3. Wrong password
    try:
        decrypt_password("wrong-password", encrypted)
        print("  [FAIL] Decrypted with wrong password?!")
    except Exception:
        print("  [PASS] Failed to decrypt with wrong password (Expected).")

def test_health():
    print("\n[TEST] Testing Health Service...")
    res = health_service.check_password_strength("correct horse battery staple")
    print(f"  Score: {res['score']} (Expected high)")
    assert res['score'] >= 3
    print("  [PASS] Health Service zxcvbn check.")

async def test_pwned():
    print("\n[TEST] Testing Pwned Service...")
    # 'password' is known to be pwned millions of times
    count = await pwned_service.check_pwned_password("password")
    print(f"  'password' count: {count}")
    assert count > 0
    print("  [PASS] Pwned Service detected 'password'.")

def test_vault_db():
    print("\n[TEST] Testing Vault Service & DB...")
    # Reset DB
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        entry = VaultEntryCreate(
            site_name="Test Bank",
            site_url="https://bank.com",
            site_password="super-secret-bank-password",
            master_password="my-master-key"
        )
        
        # Create
        db_entry = vault_service.create_vault_entry(db, entry)
        print(f"  Created entry ID: {db_entry.id}")
        
        # Verify ZK (Check raw DB data)
        print(f"  Raw Encrypted Data: {db_entry.encrypted_password[:20]}...")
        assert "super-secret-bank-password" not in db_entry.encrypted_password
        print("  [PASS] Plaintext not found in DB object.")
        
        # Retrieve
        decrypted = vault_service.get_vault_entry(db, db_entry.id, "my-master-key")
        assert decrypted["decrypted_password"] == "super-secret-bank-password"
        print("  [PASS] Decryption via Service success.")
        
    finally:
        db.close()

async def main():
    test_crypto()
    test_health()
    await test_pwned()
    test_vault_db()
    print("\n[ALL TESTS PASSED] SecurePass Logic Verified.")

if __name__ == "__main__":
    asyncio.run(main())
