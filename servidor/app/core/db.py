from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from .config import settings

_client: Optional[AsyncIOMotorClient] = None

async def get_client() -> Optional[AsyncIOMotorClient]:
    global _client
    if _client is None and settings.MONGODB_URI:
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
    return _client

async def get_db() -> Optional[AsyncIOMotorDatabase]:
    client = await get_client()
    if client:
        return client[settings.MONGODB_DBNAME]
    return None