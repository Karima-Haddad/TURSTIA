class DecisionAgent:

    def decide(self, top_similarity, fraud_risk_level, best_scenario, risk_result):
        """
        Détermine la décision finale pour un dossier NORMAL
        """

        # --- Vérification mode NORMAL ---
        if fraud_risk_level != "LOW" or top_similarity < 0.75:
            return {"mode": "NON_NORMAL"}

        mode = "NORMAL"
        risk_level = risk_result["risk_level"]

        # --- Calcul confidence clair ---
        if risk_level == "LOW":
            confidence = top_similarity
        elif risk_level == "MEDIUM":
            confidence = top_similarity - 0.05
        else:  # HIGH
            confidence = top_similarity - 0.15

        confidence = round(max(confidence, 0), 2)

        # --- Conditions selon scénario ---
        if best_scenario == "ACCEPT":
            conditions = [
                "no_collateral",
                "max_amount=10000",
                "term<=36m"
            ]
        elif best_scenario == "ACCEPT_WITH_GUARANTEE":
            conditions = [
                "collateral_required",
                "max_amount=8000",
                "term<=24m"
            ]
        else:  # REJECT
            conditions = ["application_rejected"]

        return {
            "mode": mode,
            "final_decision": best_scenario,
            "confidence": confidence,
            "conditions": conditions
        }
