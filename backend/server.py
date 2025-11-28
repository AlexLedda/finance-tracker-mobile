from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import bcrypt
import jwt
from bson import ObjectId
from openai import OpenAI

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT config
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24 * 30  # 30 days

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")
security = HTTPBearer()

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    token: str

class Transaction(BaseModel):
    id: Optional[str] = None
    user_id: str
    type: str  # income or expense
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionCreate(BaseModel):
    type: str
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime

class Budget(BaseModel):
    id: Optional[str] = None
    user_id: str
    category: str
    limit: float
    spent: float = 0
    period: str  # monthly, weekly
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BudgetCreate(BaseModel):
    category: str
    limit: float
    period: str

class Goal(BaseModel):
    id: Optional[str] = None
    user_id: str
    name: str
    target_amount: float
    current_amount: float = 0
    deadline: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GoalCreate(BaseModel):
    name: str
    target_amount: float
    deadline: datetime

class AdviceRequest(BaseModel):
    context: Optional[str] = None

# Helper functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Auth endpoints
@api_router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_dict = {
        "email": user.email,
        "password": hash_password(user.password),
        "name": user.name,
        "created_at": datetime.utcnow()
    }
    result = await db.users.insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    token = create_token(user_id)
    return UserResponse(
        id=user_id,
        email=user.email,
        name=user.name,
        token=token
    )

@api_router.post("/auth/login", response_model=UserResponse)
async def login(user: UserLogin):
    # Find user
    db_user = await db.users.find_one({"email": user.email})
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

# Transaction endpoints
@api_router.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, user_id: str = Depends(get_current_user)):
    trans_dict = transaction.dict()
    trans_dict["user_id"] = user_id
    trans_dict["created_at"] = datetime.utcnow()
    
    result = await db.transactions.insert_one(trans_dict)
    
    # Update budget if expense
    if transaction.type == "expense":
        await db.budgets.update_one(
            {"user_id": user_id, "category": transaction.category},
            {"$inc": {"spent": transaction.amount}}
        )
    
    trans_dict["id"] = str(result.inserted_id)
    return Transaction(**trans_dict)

@api_router.get("/transactions", response_model=List[Transaction])
async def get_transactions(user_id: str = Depends(get_current_user)):
    transactions = await db.transactions.find({"user_id": user_id}).sort("date", -1).to_list(1000)
    return [Transaction(id=str(t["_id"]), **{k: v for k, v in t.items() if k != "_id"}) for t in transactions]

@api_router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str, user_id: str = Depends(get_current_user)):
    result = await db.transactions.delete_one({"_id": ObjectId(transaction_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}

# Budget endpoints
@api_router.post("/budgets", response_model=Budget)
async def create_budget(budget: BudgetCreate, user_id: str = Depends(get_current_user)):
    # Check if budget exists for category
    existing = await db.budgets.find_one({"user_id": user_id, "category": budget.category})
    if existing:
        raise HTTPException(status_code=400, detail="Budget already exists for this category")
    
    budget_dict = budget.dict()
    budget_dict["user_id"] = user_id
    budget_dict["spent"] = 0
    budget_dict["created_at"] = datetime.utcnow()
    
    result = await db.budgets.insert_one(budget_dict)
    budget_dict["id"] = str(result.inserted_id)
    return Budget(**budget_dict)

@api_router.get("/budgets", response_model=List[Budget])
async def get_budgets(user_id: str = Depends(get_current_user)):
    budgets = await db.budgets.find({"user_id": user_id}).to_list(1000)
    return [Budget(id=str(b["_id"]), **{k: v for k, v in b.items() if k != "_id"}) for b in budgets]

@api_router.put("/budgets/{budget_id}", response_model=Budget)
async def update_budget(budget_id: str, budget: BudgetCreate, user_id: str = Depends(get_current_user)):
    update_dict = budget.dict()
    result = await db.budgets.update_one(
        {"_id": ObjectId(budget_id), "user_id": user_id},
        {"$set": update_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    updated = await db.budgets.find_one({"_id": ObjectId(budget_id)})
    return Budget(id=str(updated["_id"]), **{k: v for k, v in updated.items() if k != "_id"})

@api_router.delete("/budgets/{budget_id}")
async def delete_budget(budget_id: str, user_id: str = Depends(get_current_user)):
    result = await db.budgets.delete_one({"_id": ObjectId(budget_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"message": "Budget deleted"}

# Goal endpoints
@api_router.post("/goals", response_model=Goal)
async def create_goal(goal: GoalCreate, user_id: str = Depends(get_current_user)):
    goal_dict = goal.dict()
    goal_dict["user_id"] = user_id
    goal_dict["current_amount"] = 0
    goal_dict["created_at"] = datetime.utcnow()
    
    result = await db.goals.insert_one(goal_dict)
    goal_dict["id"] = str(result.inserted_id)
    return Goal(**goal_dict)

@api_router.get("/goals", response_model=List[Goal])
async def get_goals(user_id: str = Depends(get_current_user)):
    goals = await db.goals.find({"user_id": user_id}).to_list(1000)
    return [Goal(id=str(g["_id"]), **{k: v for k, v in g.items() if k != "_id"}) for g in goals]

@api_router.put("/goals/{goal_id}/contribute")
async def contribute_to_goal(goal_id: str, amount: float, user_id: str = Depends(get_current_user)):
    result = await db.goals.update_one(
        {"_id": ObjectId(goal_id), "user_id": user_id},
        {"$inc": {"current_amount": amount}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    updated = await db.goals.find_one({"_id": ObjectId(goal_id)})
    return Goal(id=str(updated["_id"]), **{k: v for k, v in updated.items() if k != "_id"})

@api_router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str, user_id: str = Depends(get_current_user)):
    result = await db.goals.delete_one({"_id": ObjectId(goal_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal deleted"}

# AI Advice endpoint
@api_router.post("/advice")
async def get_advice(request: AdviceRequest, user_id: str = Depends(get_current_user)):
    # Get user's financial data
    transactions = await db.transactions.find({"user_id": user_id}).sort("date", -1).limit(50).to_list(50)
    budgets = await db.budgets.find({"user_id": user_id}).to_list(100)
    goals = await db.goals.find({"user_id": user_id}).to_list(100)
    
    # Calculate statistics
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    
    # Build context for AI
    context = f"""Analizza la situazione finanziaria dell'utente e fornisci 3-5 consigli pratici in italiano.

Dati finanziari:
- Entrate totali: €{total_income:.2f}
- Spese totali: €{total_expenses:.2f}
- Bilancio: €{total_income - total_expenses:.2f}
- Numero di transazioni: {len(transactions)}
- Budget attivi: {len(budgets)}
- Obiettivi di risparmio: {len(goals)}
"""
    
    if budgets:
        context += "\nBudget:\n"
        for b in budgets:
            percentage = (b["spent"] / b["limit"] * 100) if b["limit"] > 0 else 0
            context += f"- {b['category']}: {b['spent']:.2f}€ / {b['limit']:.2f}€ ({percentage:.1f}%)\n"
    
    if goals:
        context += "\nObiettivi:\n"
        for g in goals:
            percentage = (g["current_amount"] / g["target_amount"] * 100) if g["target_amount"] > 0 else 0
            context += f"- {g['name']}: {g['current_amount']:.2f}€ / {g['target_amount']:.2f}€ ({percentage:.1f}%)\n"
    
    if request.context:
        context += f"\nRichiesta specifica: {request.context}\n"
    
    context += "\nFornisci consigli pratici e personalizzati per migliorare la gestione finanziaria."
    
    try:
        # Use OpenAI with Emergent LLM key
        chat = LlmChat(
            api_key=os.environ['EMERGENT_LLM_KEY'],
            session_id=f"advice_{user_id}_{datetime.utcnow().isoformat()}",
            system_message="Sei un consulente finanziario esperto. Fornisci consigli pratici e personalizzati in italiano."
        )
        chat.with_model("openai", "gpt-4o-mini")
        
        user_message = UserMessage(text=context)
        response = await chat.send_message(user_message)
        
        return {"advice": response}
    except Exception as e:
        logging.error(f"Error getting AI advice: {str(e)}")
        return {
            "advice": "Mi dispiace, non sono riuscito a generare consigli personalizzati. Riprova più tardi."
        }

# Stats endpoint
@api_router.get("/stats")
async def get_stats(user_id: str = Depends(get_current_user)):
    # Get all transactions
    transactions = await db.transactions.find({"user_id": user_id}).to_list(1000)
    
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expenses
    
    # Category breakdown
    category_expenses = {}
    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            category_expenses[category] = category_expenses.get(category, 0) + t["amount"]
    
    # Recent transactions (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_transactions = [t for t in transactions if t["date"] >= thirty_days_ago]
    recent_income = sum(t["amount"] for t in recent_transactions if t["type"] == "income")
    recent_expenses = sum(t["amount"] for t in recent_transactions if t["type"] == "expense")
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "category_expenses": category_expenses,
        "recent_income": recent_income,
        "recent_expenses": recent_expenses,
        "transaction_count": len(transactions)
    }

@api_router.get("/")
async def root():
    return {"message": "FinanceTracker API is running"}

# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
