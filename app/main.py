from fastapi import FastAPI
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

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(vault.router, prefix=f"{settings.API_V1_STR}/vault", tags=["vault"])
app.include_router(share.router, prefix=f"{settings.API_V1_STR}/share", tags=["share"])
app.include_router(generator.router, prefix=f"{settings.API_V1_STR}/generator", tags=["generator"])

@app.get("/")
def root():
    return {"message": "Welcome to SecurePass API (v2). Now with Multi-User & 2FA support!"}
