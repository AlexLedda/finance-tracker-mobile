from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    def connect(self):
        client_options = {}
        
        # Check if we need to use the CA bundle for AWS DocumentDB
        if "docdb" in settings.MONGO_URL or "aws" in settings.MONGO_URL or settings.ENVIRONMENT == "production":
             # If the CA bundle exists, use it
             import os
             if os.path.exists(settings.AWS_CA_BUNDLE_PATH):
                 client_options["tlsCAFile"] = settings.AWS_CA_BUNDLE_PATH
                 client_options["tls"] = True
        
        self.client = AsyncIOMotorClient(settings.MONGO_URL, **client_options)
        self.db = self.client[settings.DB_NAME]

    def close(self):
        if self.client:
            self.client.close()

db = Database()

async def get_db():
    try:
        yield db.db
    finally:
        pass  # Motor client is managed by lifespan, no per-request cleanup needed for the connection itself usually

