# SecurePass - Zero-Knowledge Password Vault & Security Suite

SecurePass is a secure, backend-focused password manager API demonstrating **Zero-Knowledge Architecture**, **Multi-Factor Authentication**, and **Secure Sharing**. Built with FastAPI and advanced cryptography (AES-256-GCM, Argon2, RSA/JWT).

## Key Features

### 1. Zero-Knowledge Vault
The core philosophy of SecurePass is that the server **knows nothing**. 
- **No Master Password Storage**: Your Vault Key is derived on-the-fly (`PBKDF2-SHA256`) and never stored.
- **AES-256-GCM Encryption**: Data is encrypted/decrypted only in memory during the request cycle.
- **Isolate Architecture**: Even if the DB is stolen, vault entries are mere blobs of random noise without the user's master password.

### 2. Multi-User & Advanced Auth
- **JWT Architecture**: Stateless authentication using secure JSON Web Tokens.
- **Argon2 Hashing**: Passwords are hashed using the state-of-the-art Argon2 algorithm (superior to bcrypt/PBKDF2).
- **User Isolation**: Strict database-level isolation ensures users can access *only* their own data.

### 3. Two-Factor Authentication (2FA)
- **Time-based OTP (TOTP)**: Compatible with Google Authenticator, Authy, Microsoft Authenticator.
- **End-to-End Flow**: Setup (QR Code) -> Verify -> Enable -> Enforce.

### 4. Secure Sharing (Self-Destruct)
- **Ephemeral Links**: Share sensitive data via a link that self-destructs after **one single view**.
- **Transparent Encryption**: The server generates a random key, gives it to the creator, and forgets it. The key is in the URL hash, never stored in the DB.

### 5. Utilities
- **Password Generator**: Cryptographically strong random password generator (using OS `secrets` source).
- **Health Checks**: Integration with `zxcvbn` (entropy) and `Have I Been Pwned` (breach check).

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

## Quick Start Guide

### Step 1: Register & Login
1. `POST /auth/register`: Create an account.
2. `POST /auth/login`: Log in to receive your **Bearer Token** (JWT). 
   *(In Swagger UI, click "Authorize" button and use your credentials).*

### Step 2: Secure Your Account (Optional)
1. `POST /auth/2fa/setup`: Get your TOTP Secret / QR URI.
2. `POST /auth/2fa/enable`: Enter the code from your Authenticator app to activate protection.

### Step 3: Use the Vault
1. `POST /vault/`: Add a password (requires your transient **Master Password**).
2. `POST /vault/{id}/reveal`: Decrypt and view a password.
3. `GET /vault/`: List your encrypted entries.

### Step 4: Share Securely
1. `POST /share/create`: Send text, get a unique self-destruct link.
2. `GET /share/{uuid}`: Open the link (Data is deleted immediately after!).

### Step 5: Utilities
1. `GET /generator/generate`: Create a strong password.
2. `POST /vault/check-health`: Test your password strength.

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
