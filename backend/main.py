from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Credit Decision API")

# Autoriser Angular 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/evaluate")
def evaluate(payload: dict):
    case_id = payload.get("case_id", "")

    if case_id == "FRAUD":
        return {
            "mode": "FRAUD",
            "decision": "REJECT",
            "confidence": 0.95,
            "explanation": "High similarity with known fraud cases."
        }

    if case_id == "COLD":
        return {
            "mode": "COLD_START",
            "decision": "HUMAN_REVIEW",
            "confidence": 0.50,
            "explanation": "No similar cases found."
        }

    # NORMAL par défaut
    return {
        "mode": "NORMAL",
        "decision": "ACCEPT_WITH_GUARANTEE",
        "confidence": 0.87,
        "explanation": "Decision based on similar historical cases."
    }

