from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ IMPORTS CORRECTS (depuis backend)
from backend.agents.fraud_agent import FraudAgent
from backend.agents.decision_agent_fraud_cold import DecisionAgentFraudCold
from backend.agents.explanation_agent import ExplanationAgent
from backend.agents.audit_agent import AuditAgent

from backend.qdrant.client import get_qdrant_client
from qdrant_client.models import VectorParams, Distance

app = FastAPI(title="Credit Decision API")

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
VECTOR_SIZE = 2


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
        "explanation": "No fraud detected"
    }