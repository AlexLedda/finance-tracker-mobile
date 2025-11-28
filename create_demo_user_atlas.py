import os
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB Atlas connection
MONGO_URL = "mongodb+srv://leddaalessandro336_db_user:Corneto123@cluster0.eczvwlq.mongodb.net/finance_tracker?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URL)
    db = client["finance_tracker"]
    users_collection = db["users"]
    
    # Test connection
    client.server_info()
    print("✅ Connected to MongoDB Atlas successfully!")
    
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
        
        print(f"🎉 Demo user created successfully on MongoDB Atlas!")
        print(f"✅ User ID: {result.inserted_id}")
        print(f"\n📱 Use these credentials to login:")
        print(f"   Email: {demo_email}")
        print(f"   Password: {demo_password}")
    
    print("\n" + "="*50)
    print("You can now test the Android/iOS app with these credentials!")
    print("="*50)
    
except Exception as e:
    print(f"❌ Error connecting to MongoDB Atlas: {str(e)}")
    print("\nPlease verify:")
    print("1. MongoDB Atlas URL is correct")
    print("2. Password is correct (Corneto123)")
    print("3. Network Access allows connections from anywhere (0.0.0.0/0)")
