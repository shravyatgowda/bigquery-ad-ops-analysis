import pandas as pd
from src.analysis import campaign_kpis, forecast, daily_impressions


def _df():
    return pd.DataFrame({
        "event_date": pd.to_datetime(["2026-01-01", "2026-01-02"] * 2),
        "campaign_id": ["A", "A", "B", "B"],
        "impressions": [1000, 1000, 500, 500],
        "clicks": [20, 30, 5, 5],
        "conversions": [2, 3, 1, 0],
        "spend": [10.0, 10.0, 4.0, 6.0],
        "revenue": [30.0, 30.0, 5.0, 5.0],
    })


def test_ctr_and_roi():
    k = campaign_kpis(_df()).set_index("campaign_id")
    assert abs(k.loc["A", "ctr"] - 0.025) < 1e-9
    assert abs(k.loc["A", "roi"] - 2.0) < 1e-9   # (60-20)/20
    assert abs(k.loc["B", "roi"] - 0.0) < 1e-9   # (10-10)/10


def test_forecast_is_flat_moving_average():
    d = daily_impressions(_df(), window=2)
    f = forecast(d, window=2, horizon=5)
    assert len(f) == 5
    assert f["forecast_impressions"].nunique() == 1
    assert f["forecast_date"].min() == pd.Timestamp("2026-01-03")
