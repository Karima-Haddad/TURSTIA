# backend/agents/risk_agent.py

class RiskAgent:

    def evaluate(self, client_profile, llm_summary):
        income = client_profile["monthly_income"]
        expenses = client_profile["monthly_expenses"]
        debt_ratio = client_profile["debt_ratio"]
        job_stability = client_profile["job_stability"]

        risk = 0.1

        if debt_ratio > 0.5:
            risk += 0.15

        if expenses > income * 0.6:
            risk += 0.1

        if job_stability < 0.5:
            risk += 0.15

        similarity = llm_summary["top_similarity"]

        if similarity > 0.7:
            risk -= 0.05
        else:
            risk += 0.05

        # Clamp between 0 and 1
        risk = min(max(risk, 0), 1)

        # Risk level
        if risk < 0.2:
            level = "LOW"
        elif risk < 0.4:
            level = "MEDIUM"
        else:
            level = "HIGH"

        # Risk factors
        risk_factors = []
        if debt_ratio > 0.5:
            risk_factors.append("high_debt_ratio")
        if expenses > income * 0.6:
            risk_factors.append("high_expenses")
        if job_stability < 0.5:
            risk_factors.append("low_job_stability")

        return {
            "risk_score": round(risk, 2),
            "risk_level": level,
            "default_probability": round(risk, 2),  # <-- Ajouté
            "risk_factors": risk_factors,
            "llm_insights_used": True
        }
