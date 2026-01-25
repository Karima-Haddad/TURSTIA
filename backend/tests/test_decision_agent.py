from backend.agents.decision_agent import DecisionAgent

def test_decision_agent():
    agent = DecisionAgent()

    # =========================
    # CAS 1 — NORMAL
    # =========================
    result_normal = agent.run(
        top_similarity=0.85,
        fraud_result={
            "fraud_risk_level": "LOW",
            "fraud_similarity": 0.2,
            "anomaly_score": 0.3
        },
        scenario_result={
            "best_scenario": "ACCEPT_WITH_GUARANTEE"
        },
        risk_result={
            "risk_level": "MEDIUM",
            "default_probability": 0.25
        }
    )
    print("NORMAL:", result_normal)

    # =========================
    # CAS 2 — COLD START
    # =========================
    result_cold = agent.run(
        top_similarity=0.30,   
        fraud_result={
            "fraud_risk_level": "LOW",
            "fraud_similarity": 0.1,
            "anomaly_score": 0.2
        },
        scenario_result={
            "best_scenario": "ACCEPT_WITH_GUARANTEE"
        },
        risk_result={
            "risk_level": "LOW",
            "default_probability": 0.10
        }
    )
    print("COLD START:", result_cold)

    # =========================
    # CAS 3 — FRAUD STOP
    # =========================
    result_fraud = agent.run(
        top_similarity=0.90,
        fraud_result={
            "fraud_risk_level": "HIGH",  # déclenche FRAUD_STOP
            "fraud_similarity": 0.92,
            "anomaly_score": 0.85
        },
        scenario_result={
            "best_scenario": "REJECT"
        },
        risk_result={
            "risk_level": "HIGH",
            "default_probability": 0.80
        }
    )
    print("FRAUD STOP:", result_fraud)


if __name__ == "__main__":
    test_decision_agent()
    print("DecisionAgent tests completed")

# def test_decision_agent():

#     agent = DecisionAgent()

#     # Cas NORMAL
#     result_normal = agent.run({
#         "top_similarity": 0.82,
#         "similar_fraud_cases": []
#     })
#     print("NORMAL:", result_normal)

#     # Cas COLD START
#     result_cold = agent.run({
#         "top_similarity": 0.5,
#         "similar_fraud_cases": []
#     })
#     print("COLD:", result_cold)

#     # Cas FRAUDE
#     result_fraud = agent.run({
#         "top_similarity": 0.92,
#         "similar_fraud_cases": [
#             {"case_id": "F-01", "score": 0.91}
#         ]
#     })
#     print("FRAUD:", result_fraud)


# if __name__ == "__main__":
#     test_decision_agent()
#     print('DecisionAgent tests completed')

# # Inputs simulés
# top_similarity = 0.85
# fraud_risk_level = "LOW"
# best_scenario = "ACCEPT_WITH_GUARANTEE"
# risk_result = {
#     "risk_level": "MEDIUM",
#     "default_probability": 0.25,
#     "risk_factors": ["high_debt_ratio"]
# }

# agent = DecisionAgent()
# decision = agent.decide(
#     top_similarity=top_similarity,
#     fraud_risk_level=fraud_risk_level,
#     best_scenario=best_scenario,
#     risk_result=risk_result
# )

# print("Decision finale :", decision)
