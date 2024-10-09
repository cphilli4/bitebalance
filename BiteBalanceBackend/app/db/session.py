# Database session management
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)
db = client["bite_balance"]

async def check_db_connection():
  try:
    return await client.server_info()
  except ServerSelectionTimeoutError:
    return None