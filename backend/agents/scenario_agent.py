# backend/agents/scenario_agent.py
class ScenarioAgent:
    """
    ScenarioAgent (Personne 3) : simule les scénarios de décision en respectant la politique bancaire prudente.
    Règles principales :
    - default_probability < 0.18 : ACCEPT
    - 0.18 <= default_probability <= 0.32 : ACCEPT_WITH_GUARANTEE
    - default_probability > 0.32 : REJECT
    """

    def simulate(self, stats_by_decision, default_probability):
        scenario_table = []
        best_scenario = None

        # Politique prudente hackathon
        if default_probability < 0.18:
            best_scenario = "ACCEPT"
        elif default_probability <= 0.32:
            best_scenario = "ACCEPT_WITH_GUARANTEE"
        else:
            best_scenario = "REJECT"

        # Construire tableau des scénarios avec verdicts
        for scenario, stats in stats_by_decision.items():
            observed_default_rate = stats.get("observed_default_rate", 0)
            avg_loss = stats.get("avg_loss_if_default", 0)

            # Calcul perte attendue (même si stats manquent, on prend 0)
            expected_loss = observed_default_rate * avg_loss if observed_default_rate is not None else 0

            # Verdict basé sur default_probability et prudence
            if scenario == best_scenario:
                verdict = "Best"
            elif default_probability < 0.32 and scenario == "REJECT":
                verdict = "Trade-off"
            elif default_probability > 0.32 and scenario != "REJECT":
                verdict = "Trade-off"
            else:
                verdict = "Reject"

            scenario_table.append({
                "scenario": scenario,
                "similar_cases": stats.get("n", stats.get("count", 0)),
                "observed_default_rate": observed_default_rate,
                "avg_loss_if_default": avg_loss,
                "expected_loss": round(expected_loss, 2),
                "verdict": verdict
            })

        return {
            "scenario_table": scenario_table,
            "best_scenario": best_scenario
        }
