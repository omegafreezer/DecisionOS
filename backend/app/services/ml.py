from pathlib import Path
import json
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts"

def _forecast_bundle():
    return joblib.load(ART / "forecast.joblib")

def _anomaly_bundle():
    return joblib.load(ART / "anomaly.joblib")

def daily_frame(df):
    out = df.groupby("date", as_index=False).agg(revenue=("revenue","sum"), units_sold=("units_sold","sum"), marketing_spend=("marketing_spend","sum"), inventory_units=("inventory_units","sum"), returns=("returns","sum"))
    out["dow"] = out.date.dt.dayofweek
    out["month"] = out.date.dt.month
    out["lag_1"] = out.revenue.shift(1)
    out["lag_7"] = out.revenue.shift(7)
    return out.dropna().reset_index(drop=True)

def forecast(df, horizon=14):
    model, features = _forecast_bundle()
    daily = daily_frame(df)
    history = daily.copy()
    rows = []
    for _ in range(horizon):
        d = history.date.iloc[-1] + pd.Timedelta(days=1)
        r = history.iloc[-1]
        row = {"date": d, "units_sold": r.units_sold, "marketing_spend": r.marketing_spend, "inventory_units": r.inventory_units, "returns": r.returns, "dow": d.dayofweek, "month": d.month, "lag_1": history.revenue.iloc[-1], "lag_7": history.revenue.iloc[-7]}
        y = float(model.predict(pd.DataFrame([row])[features])[0])
        row["revenue"] = y
        history = pd.concat([history, pd.DataFrame([row])], ignore_index=True)
        rows.append({"date": d.strftime("%Y-%m-%d"), "revenue": round(y, 2)})
    metrics = json.loads((ART / "forecast_metrics.json").read_text())
    return {"forecast": rows, "metrics": metrics}

def anomalies(df, limit=12):
    model, features = _anomaly_bundle()
    daily = daily_frame(df)
    daily["score"] = model.decision_function(daily[features])
    daily["is_anomaly"] = model.predict(daily[features]) == -1
    out = daily[daily.is_anomaly].sort_values("score").head(limit)
    return [{"date": r.date.strftime("%Y-%m-%d"), "revenue": round(r.revenue,2), "units_sold": int(r.units_sold), "inventory_units": round(r.inventory_units,1), "score": round(float(r.score),4)} for r in out.itertuples()]
