"""Create a SYNTHETIC ad events file so the pipeline can be tested end to end.

The numbers are random and mean nothing. Replace data/sample_ad_events.csv
with a real public ad dataset before drawing any conclusions.
"""
import argparse
import numpy as np
import pandas as pd


def generate(days: int = 120, campaigns: int = 5, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-01-01", periods=days, freq="D")
    rows = []
    for c in range(1, campaigns + 1):
        base = rng.integers(40_000, 120_000)
        ctr = rng.uniform(0.01, 0.04)
        cvr = rng.uniform(0.02, 0.08)
        cpc = rng.uniform(0.2, 0.8)
        value = rng.uniform(8, 25)
        for i, d in enumerate(dates):
            weekly = 1 + 0.15 * np.sin(2 * np.pi * (d.dayofweek) / 7)
            trend = 1 + 0.002 * i
            impressions = int(base * weekly * trend * rng.normal(1, 0.06))
            clicks = int(impressions * ctr * rng.normal(1, 0.08))
            conversions = int(clicks * cvr * rng.normal(1, 0.1))
            spend = round(clicks * cpc, 2)
            revenue = round(conversions * value, 2)
            rows.append((d.date().isoformat(), f"C{c:03d}", impressions, clicks, conversions, spend, revenue))
    return pd.DataFrame(
        rows,
        columns=["event_date", "campaign_id", "impressions", "clicks", "conversions", "spend", "revenue"],
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="data/sample_ad_events.csv")
    a = p.parse_args()
    generate().to_csv(a.out, index=False)
    print(f"wrote {a.out}")
