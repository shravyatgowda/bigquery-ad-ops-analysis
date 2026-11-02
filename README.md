# BigQuery Ad-Ops Performance Analysis and Impressions Forecast

An ad-operations style analysis: campaign KPIs (CTR, conversion rate, CPC, ROI) in BigQuery SQL, plus a simple moving-average forecast of next month's available ad impressions in Python. Outputs are CSVs ready for a Tableau or Power BI dashboard.

> **Data note:** `data/sample_ad_events.csv` is **synthetic** (random numbers) so the pipeline can be run and tested end to end. It says nothing about real campaigns. Replace it with a real public ad dataset before drawing conclusions, and record the dataset name and your real results in the Results section.

## Project layout

```
sql/                 BigQuery SQL (schema, KPIs, daily moving average, 30-day forecast)
src/analysis.py      KPIs + moving-average forecast + backtest (pandas)
src/generate_sample_data.py   builds the synthetic sample
tests/               pytest checks for the KPI and forecast logic
outputs/             generated CSVs for the dashboard (git-ignored)
```

## Input format

One row per campaign per day:

| column | type |
|---|---|
| event_date | date |
| campaign_id | string |
| impressions, clicks, conversions | integer |
| spend, revenue | number |

Map the columns of your chosen public dataset to this shape (rename or aggregate in a short script or in SQL).

## Run it locally (no cloud needed)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/generate_sample_data.py      # or drop your own CSV in data/
python src/analysis.py --input data/sample_ad_events.csv
pytest
```

Outputs in `outputs/`: `campaign_kpis.csv`, `daily_impressions.csv`, `forecast_next_30d.csv`.

## Run it in BigQuery

1. Create a Google Cloud project and enable BigQuery (the free sandbox is enough).
2. Replace `YOUR_PROJECT` in the files under `sql/`.
3. Run `sql/00_schema.sql`, then load your CSV:
   ```bash
   bq load --source_format=CSV --skip_leading_rows=1 ad_ops.ad_events data/your_file.csv
   ```
4. Run `01_campaign_kpis.sql`, `02_daily_impressions_ma.sql` and `03_forecast_next_30d.sql`, then export each result to CSV.

## Method

- **KPIs:** CTR = clicks / impressions, CVR = conversions / clicks, CPC = spend / clicks, ROI = (revenue - spend) / spend. Divisions are guarded against zero.
- **Forecast:** a flat forecast equal to the average of the last 7 days, repeated for 30 days. It is deliberately basic.
- **Backtest:** one-step-ahead moving-average predictions over the last 30 days, reported as MAPE.
- **Limits:** a flat moving average ignores weekly seasonality and trend. A natural next step is a seasonal method.

## Dashboard (Tableau Public or Power BI)

Connect to the CSVs in `outputs/` and build:
1. CTR and ROI by campaign (bar chart)
2. Daily impressions with the moving average (line chart)
3. The 30-day forecast appended to the history (line chart)

Add the public dashboard link here once published: `TODO`

## Results (fill in after running on a real dataset)

- Dataset used: `TODO`
- Top and bottom campaign by ROI: `TODO`
- Backtest MAPE: `TODO`
- Forecast for next 30 days: `TODO`
- One insight and the action it suggests: `TODO`

## License

MIT. See [LICENSE](LICENSE).
