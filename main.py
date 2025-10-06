# backend/main.py
from fastapi import FastAPI
from .db import Base, engine
from .auth import router as auth_router
from .routers import upload as upload_router

app = FastAPI(title="Academic Assignment Helper API")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(upload_router.router)
