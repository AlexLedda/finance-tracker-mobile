from fastapi import APIRouter, Depends
from openai import OpenAI
import logging
from ..models.advice import AdviceRequest
from ..core.database import db
from ..core.config import settings
from ..core.security import get_current_user

router = APIRouter(prefix="/advice", tags=["advice"])
logger = logging.getLogger(__name__)

@router.post("")
async def get_advice(request: AdviceRequest, user_id: str = Depends(get_current_user)):
    # Get user's financial data
    transactions = await db.db.transactions.find({"user_id": user_id}).sort("date", -1).limit(50).to_list(50)
    budgets = await db.db.budgets.find({"user_id": user_id}).to_list(100)
    goals = await db.db.goals.find({"user_id": user_id}).to_list(100)
    
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
        # Use OpenAI directly
        openai_key = settings.OPENAI_API_KEY or settings.EMERGENT_LLM_KEY
        if not openai_key:
            return {
                "advice": "Servizio di consigli AI non configurato. Contatta l'amministratore."
            }
        
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un consulente finanziario esperto. Fornisci consigli pratici e personalizzati in italiano."},
                {"role": "user", "content": context}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        advice_text = response.choices[0].message.content
        return {"advice": advice_text}
    except Exception as e:
        logger.error(f"Error getting AI advice: {str(e)}")
        return {
            "advice": "Mi dispiace, non sono riuscito a generare consigli personalizzati. Riprova più tardi."
        }
