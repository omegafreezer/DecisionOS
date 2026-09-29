from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.metrics import mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "retail_daily.csv"
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["date"])
daily = df.groupby("date", as_index=False).agg(revenue=("revenue","sum"), units_sold=("units_sold","sum"), marketing_spend=("marketing_spend","sum"), inventory_units=("inventory_units","sum"), returns=("returns","sum"))
daily["dow"] = daily.date.dt.dayofweek
daily["month"] = daily.date.dt.month
daily["lag_1"] = daily.revenue.shift(1)
daily["lag_7"] = daily.revenue.shift(7)
daily = daily.dropna().reset_index(drop=True)
features = ["units_sold","marketing_spend","inventory_units","returns","dow","month","lag_1","lag_7"]
cut = int(len(daily) * .8)
train, test = daily.iloc[:cut], daily.iloc[cut:]
model = RandomForestRegressor(n_estimators=180, random_state=42, n_jobs=-1, min_samples_leaf=2)
model.fit(train[features], train.revenue)
pred = model.predict(test[features])
metrics = {"mae": float(mean_absolute_error(test.revenue, pred)), "r2": float(r2_score(test.revenue, pred)), "train_rows": len(train), "test_rows": len(test)}
joblib.dump((model, features), ART / "forecast.joblib")
(ART / "forecast_metrics.json").write_text(json.dumps(metrics, indent=2))

# Residual-free anomaly detector on daily business KPIs.
iso_features = ["revenue","units_sold","inventory_units","returns"]
anomaly = IsolationForest(contamination=.02, random_state=42)
anomaly.fit(daily[iso_features])
joblib.dump((anomaly, iso_features), ART / "anomaly.joblib")
print(json.dumps(metrics, indent=2))
