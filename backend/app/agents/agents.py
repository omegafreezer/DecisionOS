import pandas as pd
from .base import AgentResult, RunContext
from ..services.data import quality_report
from ..services.ml import forecast, anomalies, daily_frame

class DataAnalystAgent:
    name = "DataAnalystAgent"
    def run(self, df, ctx):
        q = quality_report(df); ctx.record(self.name, "validate_data", q)
        total = float(df.revenue.sum())
        recent = float(df[df.date >= df.date.max() - pd.Timedelta(days=27)].revenue.sum())
        previous = float(df[(df.date < df.date.max() - pd.Timedelta(days=27)) & (df.date >= df.date.max() - pd.Timedelta(days=55))].revenue.sum())
        change = ((recent / previous) - 1) * 100 if previous else 0
        ctx.state["summary"] = {"total_revenue": total, "recent_28d": recent, "previous_28d": previous, "change_pct": change, "quality": q}
        ctx.record(self.name, "calculate_kpis", ctx.state["summary"])
        return AgentResult(self.name, f"Recent 28-day revenue changed {change:.2f}% versus the preceding 28-day period.", [{"metric":"revenue_change_pct","value":round(change,2)}], {"quality":q})

class ForecastAgent:
    name = "ForecastAgent"
    def run(self, df, ctx):
        result = forecast(df, 14); ctx.state["forecast"] = result
        ctx.record(self.name, "forecast_14_days", result["metrics"])
        return AgentResult(self.name, "Generated a 14-day revenue forecast using the trained regression pipeline.", result["forecast"][:5], result["metrics"])

class AnomalyAgent:
    name = "AnomalyAgent"
    def run(self, df, ctx):
        result = anomalies(df); ctx.state["anomalies"] = result
        ctx.record(self.name, "detect_anomalies", {"count":len(result)})
        return AgentResult(self.name, f"Detected {len(result)} high-priority daily KPI anomalies.", result)

class RootCauseAgent:
    name = "RootCauseAgent"
    def run(self, df, ctx):
        recent_start = df.date.max() - pd.Timedelta(days=27)
        prev_start = df.date.max() - pd.Timedelta(days=55)
        recent = df[df.date >= recent_start].groupby(["region","product"]).revenue.sum()
        prev = df[(df.date >= prev_start) & (df.date < recent_start)].groupby(["region","product"]).revenue.sum()
        comp = pd.concat([prev.rename("previous"), recent.rename("recent")], axis=1).fillna(0)
        comp["change_pct"] = ((comp.recent / comp.previous.replace(0, pd.NA)) - 1) * 100
        comp = comp.dropna().sort_values("change_pct")
        top = comp.head(5).reset_index()
        evidence = top.to_dict("records")
        ctx.state["root_causes"] = evidence
        ctx.record(self.name, "rank_root_cause_segments", evidence)
        if evidence:
            lead = evidence[0]
            text = f"The largest negative segment movement is {lead['region']} / Product {lead['product']} at {lead['change_pct']:.1f}% versus the prior comparison period."
        else:
            text = "No stable segment-level root cause was identified."
        return AgentResult(self.name, text, evidence)

class ScenarioAgent:
    name = "ScenarioAgent"
    def run(self, df, inventory_delta=0.0, price_delta=0.0, marketing_delta=0.0, ctx=None):
        daily = daily_frame(df)
        baseline = float(daily.revenue.tail(28).mean())
        # Transparent heuristic: scenario multipliers are intentionally simple and explainable.
        impact = 0.55 * inventory_delta + 0.35 * price_delta + 0.10 * marketing_delta
        projected = baseline * (1 + impact)
        result = {"baseline_daily_revenue": round(baseline,2), "projected_daily_revenue": round(projected,2), "estimated_change_pct": round(impact*100,2), "assumptions":{"inventory_elasticity":0.55,"price_elasticity":0.35,"marketing_elasticity":0.10}}
        if ctx:
            ctx.state["scenario"] = result; ctx.record(self.name, "simulate", result)
        return AgentResult(self.name, "Ran an explainable what-if scenario using documented elasticity assumptions.", [result])

class DecisionAgent:
    name = "DecisionAgent"
    def run(self, ctx):
        kpi = ctx.state.get("summary", {})
        root = ctx.state.get("root_causes", [])
        anomalies_ = ctx.state.get("anomalies", [])
        actions = []
        if root and root[0]["change_pct"] < -5:
            actions.append("Investigate the leading region/product segment and validate inventory availability before changing price.")
        if anomalies_:
            actions.append("Review the highest-severity anomalous dates with operations and data-quality owners.")
        actions.append("Use the scenario simulator before committing changes to inventory, price or marketing spend.")
        result = {"decision_id":ctx.decision_id,"headline":"Evidence-first operating actions generated.","actions":actions,"evidence":{"kpi":kpi,"top_root_causes":root[:3],"anomaly_count":len(anomalies_)},"trace":ctx.trace}
        ctx.state["decision"] = result; ctx.record(self.name, "compose_decision", {"action_count":len(actions)})
        return AgentResult(self.name, result["headline"], actions, {"decision_id":ctx.decision_id})
