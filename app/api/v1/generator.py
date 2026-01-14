from fastapi import APIRouter, Query
from app.services import generator_service
from pydantic import BaseModel

router = APIRouter()

class GeneratedPassword(BaseModel):
    password: str
    length: int

@router.get("/generate", response_model=GeneratedPassword)
def generate_password(
    length: int = Query(16, ge=8, le=128),
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True
):
    pwd = generator_service.generate_strong_password(
        length=length,
        include_uppercase=uppercase,
        include_digits=digits,
        include_symbols=symbols
    )
    return {"password": pwd, "length": len(pwd)}
