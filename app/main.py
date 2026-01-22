from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import vault, auth, share, generator
from app.core.config import settings
from app.db.session import engine
from app.db.models import Base
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter
from secure import Secure

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:;"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(vault.router, prefix=f"{settings.API_V1_STR}/vault", tags=["vault"])
app.include_router(share.router, prefix=f"{settings.API_V1_STR}/share", tags=["share"])
app.include_router(generator.router, prefix=f"{settings.API_V1_STR}/generator", tags=["generator"])

@app.get("/")
def root():
    return {"message": "Welcome to SecurePass API (v2). Now with Multi-User & 2FA support!"}
