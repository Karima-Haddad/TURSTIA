import base64
from pathlib import Path
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pprint
import traceback
from agents.document_agent import run_document_agent

app = FastAPI(title="Credit Decision API",debug=True)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

# Autoriser Angular 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    try:
        print("\n🔥 /api/document-agent/test CALLED 🔥\n")
        pprint.pprint(payload)

        case_id = payload.get("case_id")
        documents = payload.get("documents", [])
        applicant_form = payload.get("applicant_form", {})

        result = run_document_agent(
            case_id=case_id,
            documents=documents
        )

        return {
            "case_id": case_id,
            "document_analysis": result
        }

    except Exception as e:
        print("❌ DOCUMENT AGENT ERROR")
        traceback.print_exc()

        return {
            "error": "DOCUMENT_AGENT_FAILED",
            "message": str(e)
        }