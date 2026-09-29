from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "retail_daily.csv"

def load_data() -> pd.DataFrame:
    if not DATA.exists():
        raise FileNotFoundError("Data not found. Run python scripts/generate_data.py")
    return pd.read_csv(DATA, parse_dates=["date"])

def quality_report(df: pd.DataFrame) -> dict:
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    negatives = int((df[["price","marketing_spend","inventory_units","units_sold","revenue"]] < 0).sum().sum())
    return {"rows": len(df), "columns": len(df.columns), "missing_cells": missing, "duplicate_rows": duplicates, "negative_numeric_values": negatives, "status": "PASS" if missing == duplicates == negatives == 0 else "CHECK"}
