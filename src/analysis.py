"""Ad-ops analysis: campaign KPIs (CTR, CVR, CPC, ROI) and a simple
moving-average forecast of daily impressions.

Input CSV columns: event_date, campaign_id, impressions, clicks, conversions, spend, revenue
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED = ["event_date", "campaign_id", "impressions", "clicks", "conversions", "spend", "revenue"]


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["event_date"])
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def campaign_kpis(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("campaign_id", as_index=False)[
        ["impressions", "clicks", "conversions", "spend", "revenue"]
    ].sum()
    g["ctr"] = g["clicks"] / g["impressions"].replace(0, np.nan)
    g["cvr"] = g["conversions"] / g["clicks"].replace(0, np.nan)
    g["cpc"] = g["spend"] / g["clicks"].replace(0, np.nan)
    g["roi"] = (g["revenue"] - g["spend"]) / g["spend"].replace(0, np.nan)
    return g.sort_values("roi", ascending=False).reset_index(drop=True)


def daily_impressions(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    d = df.groupby("event_date", as_index=False)["impressions"].sum().sort_values("event_date")
    d["ma"] = d["impressions"].rolling(window).mean()
    return d


def backtest_mape(daily: pd.DataFrame, window: int = 7, holdout: int = 30) -> float:
    """One-step-ahead: predict each held-out day with the mean of the previous `window` days."""
    s = daily["impressions"].reset_index(drop=True)
    preds, actual = [], []
    for t in range(len(s) - holdout, len(s)):
        preds.append(s.iloc[t - window:t].mean())
        actual.append(s.iloc[t])
    preds, actual = np.array(preds), np.array(actual)
    return float(np.mean(np.abs(actual - preds) / actual))


def forecast(daily: pd.DataFrame, window: int = 7, horizon: int = 30) -> pd.DataFrame:
    level = daily["impressions"].tail(window).mean()
    start = daily["event_date"].max() + pd.Timedelta(days=1)
    dates = pd.date_range(start, periods=horizon, freq="D")
    return pd.DataFrame({"forecast_date": dates, "forecast_impressions": level})


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/sample_ad_events.csv")
    p.add_argument("--outdir", default="outputs")
    p.add_argument("--window", type=int, default=7)
    p.add_argument("--horizon", type=int, default=30)
    a = p.parse_args()

    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    df = load(a.input)

    kpis = campaign_kpis(df)
    daily = daily_impressions(df, a.window)
    fc = forecast(daily, a.window, a.horizon)
    mape = backtest_mape(daily, a.window)

    kpis.to_csv(out / "campaign_kpis.csv", index=False)
    daily.to_csv(out / "daily_impressions.csv", index=False)
    fc.to_csv(out / "forecast_next_30d.csv", index=False)

    print(kpis.round(4).to_string(index=False))
    print(f"\nBacktest MAPE (last 30 days, {a.window}-day moving average): {mape:.2%}")
    print(f"Forecast total for next {a.horizon} days: {fc['forecast_impressions'].sum():,.0f} impressions")


if __name__ == "__main__":
    main()
