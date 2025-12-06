from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from ..models.user import UserCreate, UserLogin, UserResponse
from ..core.database import db
from ..core.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    # Check if user exists
    existing_user = await db.db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_dict = {
        "email": user.email,
        "password": hash_password(user.password),
        "name": user.name,
        "created_at": datetime.now(timezone.utc)
    }
    result = await db.db.users.insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    token = create_token(user_id)
    return UserResponse(
        id=user_id,
        email=user.email,
        name=user.name,
        token=token
    )

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    # Find user
    db_user = await db.db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = str(db_user["_id"])
    token = create_token(user_id)
    return UserResponse(
        id=user_id,
        email=db_user["email"],
        name=db_user["name"],
        token=token
    )
