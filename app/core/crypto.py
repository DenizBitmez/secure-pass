import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Constants
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32  # 32 bytes for AES-256
ITERATIONS = 100000 # Enough for demonstration, cleaner would be higher but slower

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derives a 256-bit key from the master password using PBKDF2-HMAC-SHA256.
    This key is used for AES-GCM encryption/decryption.
    It is NEVER stored on disk.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(master_password.encode('utf-8'))

def encrypt_password(master_password: str, plaintext: str) -> str:
    """
    Encrypts plaintext using a key derived from the master password.
    Returns a base64 string containing: salt + nonce + ciphertext.
    
    Format: [Salt (16)][Nonce (12)][Ciphertext (variable + tag 16)]
    """
    salt = os.urandom(SALT_SIZE)
    key = derive_key(master_password, salt)
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    
    # Encrypt
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    
    # Combine all parts
    combined = salt + nonce + ciphertext
    return base64.urlsafe_b64encode(combined).decode('utf-8')

def decrypt_password(master_password: str, encrypted_data: str) -> str:
    try:
        data = base64.urlsafe_b64decode(encrypted_data)
        
        # Extract parts
        salt = data[:SALT_SIZE]
        nonce = data[SALT_SIZE:SALT_SIZE+NONCE_SIZE]
        ciphertext = data[SALT_SIZE+NONCE_SIZE:]
        
        key = derive_key(master_password, salt)
        aesgcm = AESGCM(key)
        
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
    except Exception as e:
        # Check for specific crypto errors if needed, but for ZK security, 
        # generic failure is often better to avoid oracle attacks, 
        # though explicit error helps debugging.
        raise ValueError("Decryption failed. Invalid password or corrupted data.") from e
