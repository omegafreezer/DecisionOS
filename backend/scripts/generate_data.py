from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "retail_daily.csv"

rng = np.random.default_rng(42)
dates = pd.date_range("2025-01-01", "2026-06-30", freq="D")
regions = ["North", "South", "East", "West"]
channels = ["Online", "Store"]
products = ["A", "B", "C", "D", "E"]
rows = []
for d in dates:
    trend = 1 + 0.0007 * (d - dates[0]).days
    season = 1 + 0.12 * np.sin(2 * np.pi * d.dayofyear / 365)
    for region in regions:
        for channel in channels:
            for product in products:
                base = 1800 * trend * season
                region_factor = {"North": 1.05, "South": .95, "East": 1.15, "West": .90}[region]
                channel_factor = 1.25 if channel == "Online" else .85
                product_factor = {"A": 1.30, "B": 1.10, "C": .95, "D": .80, "E": .70}[product]
                price = {"A": 42, "B": 35, "C": 28, "D": 22, "E": 18}[product] * rng.normal(1, .03)
                marketing = max(100, rng.normal(600, 100))
                inventory = max(10, rng.normal(800, 120))
                demand = base * region_factor * channel_factor * product_factor
                units = max(1, rng.poisson(demand / 60))
                if d >= pd.Timestamp("2026-05-20") and region == "North" and product == "A":
                    inventory *= .55
                    units = int(units * .72)
                revenue = units * price
                returns = max(0, int(rng.binomial(units, .035)))
                rows.append([d, region, channel, product, round(price,2), round(marketing,2), round(inventory,2), units, returns, round(revenue,2)])

df = pd.DataFrame(rows, columns=["date","region","channel","product","price","marketing_spend","inventory_units","units_sold","returns","revenue"])
df.to_csv(OUT, index=False)
print(f"Wrote {len(df):,} rows to {OUT}")
