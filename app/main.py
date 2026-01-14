from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import vault, auth, share, generator
from app.core.config import settings
from app.db.session import engine
from app.db.models import Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

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
