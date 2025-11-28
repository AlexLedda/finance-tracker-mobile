import os
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["finance_tracker"]
users_collection = db["users"]

# Demo user credentials
demo_email = "demo@test.com"
demo_password = "Demo123!"

# Check if user already exists
existing_user = users_collection.find_one({"email": demo_email})

if existing_user:
    print(f"❌ User {demo_email} already exists in database!")
    print(f"✅ You can use these credentials to login:")
    print(f"   Email: {demo_email}")
    print(f"   Password: {demo_password}")
else:
    # Hash password
    hashed_password = pwd_context.hash(demo_password)
    
    # Create demo user
    demo_user = {
        "email": demo_email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    # Insert into database
    result = users_collection.insert_one(demo_user)
    
    print(f"🎉 Demo user created successfully!")
    print(f"✅ User ID: {result.inserted_id}")
    print(f"\n📱 Use these credentials to login:")
    print(f"   Email: {demo_email}")
    print(f"   Password: {demo_password}")

print("\n" + "="*50)
print("You can now test the Android app with these credentials!")
print("="*50)
