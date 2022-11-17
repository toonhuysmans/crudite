from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from app.routers import router as crudite_router

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(crudite_router)