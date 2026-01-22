import pyotp
from typing import Tuple
from zxcvbn import zxcvbn
from fastapi import HTTPException

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def verify_totp(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

def get_totp_uri(secret: str, email: str, issuer_name: str = "SecurePass") -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=issuer_name)

def validate_password_strength(password: str, user_inputs: list = None) -> None:
    results = zxcvbn(password, user_inputs=user_inputs)
    if results["score"] < 3:
        feedback_parts = []
        if results["feedback"]["warning"]:
            feedback_parts.append(results["feedback"]["warning"])
        feedback_parts.extend(results["feedback"]["suggestions"])
        feedback = ", ".join(feedback_parts)
        
        raise HTTPException(
            status_code=400,
            detail=f"Password is too weak. Score: {results['score']}/4. {feedback}"
        )
