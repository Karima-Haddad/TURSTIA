# FastAPI (appel du pipeline)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.agents.learning_loop_agent import LearningLoopAgent

import json
from pathlib import Path
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends
from backend.database.security import get_current_user
from backend.database.auth import router as auth_router

# Initialisation de l'app FastAPI
app = FastAPI()

# Inclusion des routes d'authentification
app.include_router(auth_router, prefix="/auth")

# Configuration du CORS pour autoriser les requêtes depuis le frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model pour la requete de l'outcome
class OutcomeRequest(BaseModel):
    case_id: str
    outcome: str  
    loss_amount: float = 0.0

# Initialisation de l'agent de l'apprentissage
learning_agent = LearningLoopAgent()

# Endpoint pour soumettre l'oucome réel d'un dossier
@app.post("/outcome")
def submit_outcome(request: OutcomeRequest, user=Depends(get_current_user)):
    """
    Endpoint appelé quand l'outcome réel du dossier est connu.
    """

    try:
        result = learning_agent.run(
            case_id=request.case_id,
            outcome=request.outcome,
            loss_amount=request.loss_amount
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print(f"Error in submit_outcome: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Définition du fichier d’audit
AUDIT_LOG_FILE = Path("backend/logs/audit_log.jsonl")

# Endpoint pour récupérer les logs d'audit
@app.get("/audit")
def get_audit_logs(case_id: str = Query(None), user=Depends(get_current_user)):
    """
    Retourne les événements d'audit.
    Optionnellement filtrés par case_id.
    """

    if not AUDIT_LOG_FILE.exists():
        return []

    events = []

    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)

            if case_id:
                if event.get("case_id") == case_id:
                    events.append(event)
            else:
                events.append(event)

    return events
