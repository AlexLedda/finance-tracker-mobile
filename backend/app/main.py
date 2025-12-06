from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .core.config import settings
from .core.database import db
from .routers import auth, transactions, budgets, goals, stats, advice

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up...")
    db.connect()
    yield
    # Shutdown
    logger.info("Shutting down...")
    db.close()

app = FastAPI(lifespan=lifespan)

# CORS structure - allow all for now as per original, but cleaner
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router
app.include_router(auth.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(budgets.router, prefix="/api")
app.include_router(goals.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(advice.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "FinanceTracker API is running"}
