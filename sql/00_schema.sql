-- Create a dataset and table for ad events.
-- Replace YOUR_PROJECT with your Google Cloud project id.
CREATE SCHEMA IF NOT EXISTS `YOUR_PROJECT.ad_ops`;

CREATE OR REPLACE TABLE `YOUR_PROJECT.ad_ops.ad_events` (
  event_date   DATE,
  campaign_id  STRING,
  impressions  INT64,
  clicks       INT64,
  conversions  INT64,
  spend        NUMERIC,
  revenue      NUMERIC
);
-- Load a CSV with the same columns, for example:
-- bq load --source_format=CSV --skip_leading_rows=1 ad_ops.ad_events data/sample_ad_events.csv
