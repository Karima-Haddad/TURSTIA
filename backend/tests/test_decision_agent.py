from agents.decision_agent import DecisionAgent

# Inputs simulés
top_similarity = 0.85
fraud_risk_level = "LOW"
best_scenario = "ACCEPT_WITH_GUARANTEE"
risk_result = {
    "risk_level": "MEDIUM",
    "default_probability": 0.25,
    "risk_factors": ["high_debt_ratio"]
}

agent = DecisionAgent()
decision = agent.decide(
    top_similarity=top_similarity,
    fraud_risk_level=fraud_risk_level,
    best_scenario=best_scenario,
    risk_result=risk_result
)

print("Decision finale :", decision)
