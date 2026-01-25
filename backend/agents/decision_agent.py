# ======================================
# Decision & Policy Agent
# ======================================

from backend.config import (
    SIMILARITY_THRESHOLD,
    FRAUD_SIMILARITY_THRESHOLD
)


class DecisionAgent:

    def run(self, retrieval_result: dict):

        top_similarity = retrieval_result.get("top_similarity", 0.0)
        similar_fraud_cases = retrieval_result.get("similar_fraud_cases", [])

        # ===============================
        # FRAUD STOP
        # ===============================
        if similar_fraud_cases:
            max_fraud_score = max(c["score"] for c in similar_fraud_cases)

            if max_fraud_score >= FRAUD_SIMILARITY_THRESHOLD:
                return {
                    "mode": "FRAUD_STOP",
                    "confidence": round(max_fraud_score, 3),
                    "reason": "High similarity with known fraud cases"
                }

        # ===============================
        # COLD START
        # ===============================
        if top_similarity < SIMILARITY_THRESHOLD:
            return {
                "mode": "COLD_START",
                "confidence": round(top_similarity, 3),
                "reason": "No sufficiently similar historical cases",
                "human_validation_required": True
            }

        # ===============================
        # 3️⃣ NORMAL
        # ===============================
        return {
            "mode": "NORMAL",
            "confidence": round(top_similarity, 3),
            "reason": "Sufficient similarity with historical cases"
        }
