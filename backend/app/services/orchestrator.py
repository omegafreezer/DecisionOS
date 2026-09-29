from ..agents.agents import DataAnalystAgent, ForecastAgent, AnomalyAgent, RootCauseAgent, DecisionAgent, ScenarioAgent
from ..agents.base import RunContext
from .data import load_data

class DecisionOrchestrator:
    def run(self):
        df = load_data(); ctx = RunContext()
        results = [DataAnalystAgent().run(df,ctx), ForecastAgent().run(df,ctx), AnomalyAgent().run(df,ctx), RootCauseAgent().run(df,ctx), DecisionAgent().run(ctx)]
        return {"decision_id":ctx.decision_id,"results":[r.__dict__ for r in results],"trace":ctx.trace,"decision":ctx.state["decision"]}

    def scenario(self, inventory_delta, price_delta, marketing_delta):
        df = load_data(); ctx = RunContext()
        r = ScenarioAgent().run(df, inventory_delta, price_delta, marketing_delta, ctx)
        return {"decision_id":ctx.decision_id,"result":r.__dict__,"trace":ctx.trace}
