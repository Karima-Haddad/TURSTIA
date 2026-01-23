from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.document_agent import run_document_agent


app = FastAPI(title="Credit Decision API",debug=True)

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

"""@app.post("/api/evaluate")
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
"""
@app.post("/api/document-agent/test")
def test_document_agent(payload: dict = Body(...)):
    case_id = payload.get("case_id")
    documents = payload.get("documents", [])
    applicant_form = payload.get("applicant_form", {})

    try:
        result = run_document_agent(
            case_id=case_id,
            documents=documents,
            applicant_form=applicant_form
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document agent error: {str(e)}")

    return {
        "case_id": case_id,
        "document_analysis": result
    }
