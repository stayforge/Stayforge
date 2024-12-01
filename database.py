from motor.motor_asyncio import AsyncIOMotorClient
import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
