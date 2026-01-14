# SecurePass - Zero-Knowledge Password Vault

SecurePass is a secure, backend-focused password manager API demonstrating **Zero-Knowledge Architecture**. Built with FastAPI and advanced cryptography standard (AES-256-GCM).

## Zero-Knowledge Architecture

The core philosophy of SecurePass is that the server **knows nothing**. 

1. **No Master Password Storage**: Unlike traditional systems, your Master Password is NEVER stored in our database (not even hashed!).
2. **Transient Encryption Keys**: 
    - When you make a request, you send your Master Password.
    - The server instantaneously derives a 256-bit encryption key using `PBKDF2-HMAC-SHA256` with a unique salt.
    - This key is used *only* for that specific request (Encryption/Decryption) and immediately discarded from memory.
3. **Encrypted at Rest**: The database only stores encrypted blobs (`Salt` + `Nonce` + `Ciphertext`). Without the Master Password (which only YOU know), this data is mathematically impossible to decrypt.

> Even if the server is compromised and the database is stolen, attackers cannot access your passwords.

## Technical Stack

- **Framework**: FastAPI (High performance async framework)
- **Cryptography**: `cryptography` library (AES-GCM, PBKDF2)
- **Security**: "Have I Been Pwned" K-Anonymity API Integration
- **Validation**: Pydantic Models
- **Database**: SQLite (scalable to PostgreSQL)

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DenizBitmez/secure-pass.git
   cd secure-pass
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## API Usage Examples

### 1. Add a Password (Secure Store)
**POST** `/api/v1/vault/`
```json
{
  "site_name": "Facebook",
  "site_url": "https://facebook.com",
  "site_password": "MySuperSecretPassword123!",
  "master_password": "my-vault-master-key"
}
```

### 2. Reveal a Password
**POST** `/api/v1/vault/{id}/reveal`
```json
{
  "master_password": "my-vault-master-key"
}
```

### 3. Check Password Health
**POST** `/api/v1/vault/check-health`
```json
{
  "password": "correct horse battery staple"
}
```
