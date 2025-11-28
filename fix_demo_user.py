from pymongo import MongoClient

# MongoDB Atlas connection
MONGO_URL = "mongodb+srv://leddaalessandro336_db_user:Corneto123@cluster0.eczvwlq.mongodb.net/finance_tracker?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URL)
    db = client["finance_tracker"]
    users_collection = db["users"]
    
    # Update demo user to add name field
    result = users_collection.update_one(
        {"email": "demo@test.com"},
        {"$set": {"name": "Demo User"}}
    )
    
    if result.modified_count > 0:
        print("✅ Demo user updated successfully!")
        print(f"   Added field: name = 'Demo User'")
    else:
        print("⚠️ User not found or already has name field")
    
    # Verify the update
    user = users_collection.find_one({"email": "demo@test.com"})
    if user:
        print(f"\n📱 User details:")
        print(f"   Email: {user.get('email')}")
        print(f"   Name: {user.get('name')}")
        print(f"   Has password: {'password' in user}")
        print(f"\n✅ You can now login with:")
        print(f"   Email: demo@test.com")
        print(f"   Password: Demo123!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
