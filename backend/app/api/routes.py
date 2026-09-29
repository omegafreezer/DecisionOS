from fastapi import APIRouter
from pydantic import BaseModel, Field
from ..services.data import load_data, quality_report
from ..services.ml import forecast, anomalies
from ..services.orchestrator import DecisionOrchestrator

router = APIRouter(prefix="/api")

class ScenarioRequest(BaseModel):
    inventory_delta: float = Field(0, description="Relative change, e.g. 0.15 for +15%")
    price_delta: float = Field(0, description="Relative change, e.g. -0.05 for -5%")
    marketing_delta: float = Field(0, description="Relative change, e.g. 0.10 for +10%")

@router.get("/summary")
def summary():
    df = load_data(); daily = df.groupby("date", as_index=False).revenue.sum()
    return {"latest_date":df.date.max().strftime("%Y-%m-%d"),"total_revenue":round(float(df.revenue.sum()),2),"average_daily_revenue":round(float(daily.revenue.mean()),2),"quality":quality_report(df)}

@router.get("/forecast")
def get_forecast(): return forecast(load_data(), 14)

@router.get("/anomalies")
def get_anomalies(): return {"anomalies": anomalies(load_data())}

@router.get("/root-cause")
def root_cause():
    return DecisionOrchestrator().run()["results"][3]

@router.post("/simulate")
def simulate(req: ScenarioRequest):
    return DecisionOrchestrator().scenario(req.inventory_delta, req.price_delta, req.marketing_delta)

@router.post("/decision")
def decision(): return DecisionOrchestrator().run()

@router.get("/audit/{decision_id}")
def audit(decision_id: str):
    result = DecisionOrchestrator().run()
    return {"requested_decision_id":decision_id,"note":"Demo endpoint re-runs the deterministic workflow; production would persist traces in an audit store.","trace":result["trace"]}
