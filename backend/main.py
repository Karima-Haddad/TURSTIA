import base64
from pathlib import Path
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ✅ IMPORTS CORRECTS (depuis backend)
from backend.agents.fraud_agent import FraudAgent
from backend.agents.decision_agent_fraud_cold import DecisionAgentFraudCold
from backend.agents.explanation_agent import ExplanationAgent
from backend.agents.audit_agent import AuditAgent

from backend.qdrant.client import get_qdrant_client
from qdrant_client.models import VectorParams, Distance

app = FastAPI(title="Credit Decision API")
import pprint
import traceback
from backend.agents.document_agent import run_document_agent
from backend.agents.document_agent import run_document_agent
from backend.agents.profile_fusion_agent import build_final_profile


app = FastAPI(title="Credit Decision API",debug=True)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agents
fraud_agent = FraudAgent()
decision_agent = DecisionAgentFraudCold()
explanation_agent = ExplanationAgent()
audit_agent = AuditAgent()

COLLECTION_NAME = "credit_cases"
VECTOR_SIZE = 384


@app.on_event("startup")
def startup_event():
    """
    Initialisation Qdrant AU DÉMARRAGE
    """
    try:
        qdrant = get_qdrant_client()

        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )

        print("✅ Qdrant connecté et collection prête")

    except Exception as e:
        print("⚠️ Qdrant non disponible au démarrage")
        print(e)


@app.get("/health")
def health():
    return {"status": "ok"}



@app.post("/api/evaluate")
def evaluate(payload: dict):
    case_id = payload.get("case_id", "")
    top_similarity = payload.get("top_similarity", 0.0)
    retrieval_result = payload.get("retrieval_result", {})

    fraud_result = fraud_agent.evaluate(retrieval_result)

    decision = decision_agent.decide(
        top_similarity=top_similarity,
        fraud_risk=fraud_result["fraud_risk"]
    )

    if decision:
        explanation = explanation_agent.explain(decision)
        audit_log = audit_agent.log(case_id, decision)

        return {
            "case_id": case_id,
            "mode": decision["mode"],
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "explanation": explanation,
            "audit": audit_log
        }

    return {
        "case_id": case_id,
        "mode": "NORMAL",
        "decision": "CONTINUE_PIPELINE",
        "confidence": 0.8,
        "explanation": "No fraud detected",

    }

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

@app.post("/api/complete-evaluation")
def complete_evaluation(payload: dict = Body(...)):

    case_id = payload.get("case_id")
    applicant_form = payload.get("applicant_form", {})
    loan_request = payload.get("loan_request", {})
    documents = payload.get("documents", [])

    # 🔹 AGENT 1
    doc_analysis = run_document_agent(
        case_id=case_id,
        documents=documents
    )

    # 🔹 AGENT 2
    fusion_result = build_final_profile(
        case_id=case_id,
        applicant_form=applicant_form,
        loan_request=loan_request,
        doc_signals=doc_analysis.doc_signals
    )

    return {
        "case_id": case_id,
        "document_analysis": doc_analysis,
        "profile_fusion": fusion_result
    }