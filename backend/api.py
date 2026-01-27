from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agents.risk_agent import RiskAgent
from backend.agents.scenario_agent import ScenarioAgent
from backend.agents.decision_agent import DecisionAgent

app = FastAPI()

# --- CORS pour Angular ---
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modèle de données ---
class ClientProfile(BaseModel):
    monthly_income: float
    monthly_expenses: float
    debt_ratio: float
    job_stability: float
    top_similarity: float

# --- Route d'évaluation ---
@app.post("/evaluate")
def evaluate(profile: ClientProfile):
    risk_agent = RiskAgent()
    risk_result = risk_agent.evaluate(profile.dict(), {"top_similarity": profile.top_similarity})

    scenario_agent = ScenarioAgent()
    scenario_result = scenario_agent.simulate({
        "ACCEPT": {"n": 10, "observed_default_rate": 0.1, "avg_loss_if_default": 1000},
        "REJECT": {"n": 5, "observed_default_rate": 0.3, "avg_loss_if_default": 5000},
        "ACCEPT_WITH_GUARANTEE": {"n": 8, "observed_default_rate": 0.15, "avg_loss_if_default": 2000}
    }, risk_result["default_probability"])

    decision_agent = DecisionAgent()
    decision_result = decision_agent.run(
        top_similarity=profile.top_similarity,
        fraud_result={"fraud_risk_level": "LOW", "fraud_similarity": 0.2, "anomaly_score": 0.1},
        scenario_result=scenario_result,
        risk_result=risk_result
    )

    return {
        "risk": risk_result,
        "scenario": scenario_result,
        "decision": decision_result
    }
