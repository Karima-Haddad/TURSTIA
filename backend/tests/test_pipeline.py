# backend/tests/test_pipeline.py

from agents.risk_agent import RiskAgent
from agents.scenario_agent import ScenarioAgent
from agents.decision_agent import DecisionAgent

# ------------------------------
# 1️⃣ Inputs simulés (extrait d'un dossier complet)
# ------------------------------
final_profile = {
    "monthly_income": 4200,
    "monthly_expenses": 2100,
    "debt_ratio": 0.41,
    "stability_score": 0.88
}

llm_summary = {
    "top_similarity": 0.89
}

stats_by_decision = {
    "ACCEPT": {
        "n": 10,
        "observed_default_rate": 0.10,
        "avg_loss_if_default": 3800
    },
    "REJECT": {
        "n": 5,
        "avg_loss_if_default": 0
    },
    "ACCEPT_WITH_GUARANTEE": {
        "n": 15,
        "observed_default_rate": 0.20,
        "avg_loss_if_default": 2500
    }
}


fraud_risk_level = "LOW"

# ------------------------------
# 2️⃣ RiskAgent
# ------------------------------
risk_agent = RiskAgent()
risk_result = risk_agent.evaluate(
    client_profile={
        "monthly_income": final_profile["monthly_income"],
        "monthly_expenses": final_profile["monthly_expenses"],
        "debt_ratio": final_profile["debt_ratio"],
        "job_stability": final_profile["stability_score"]
    },
    llm_summary=llm_summary
)

print("→ RiskAgent :", risk_result)

# ------------------------------
# 3️⃣ ScenarioAgent
# ------------------------------
scenario_agent = ScenarioAgent()
scenario_result = scenario_agent.simulate(stats_by_decision, risk_result["default_probability"])

print("→ ScenarioAgent :", scenario_result)

# ------------------------------
# 4️⃣ DecisionAgent
# ------------------------------
decision_agent = DecisionAgent()
decision_result = decision_agent.decide(
    top_similarity=llm_summary["top_similarity"],
    fraud_risk_level=fraud_risk_level,
    best_scenario=scenario_result["best_scenario"],
    risk_result=risk_result
)

print("→ DecisionAgent :", decision_result)

# ------------------------------
# ✅ Résultat final
# ------------------------------
print("\n🎯 Pipeline complet terminé !")
print("Decision finale :", decision_result)
