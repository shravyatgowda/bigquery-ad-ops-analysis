-- Flat forecast: the mean of the last 7 days, repeated for the next 30 days.
WITH daily AS (
  SELECT event_date, SUM(impressions) AS impressions
  FROM `YOUR_PROJECT.ad_ops.ad_events`
  GROUP BY event_date
),
level AS (
  SELECT AVG(impressions) AS ma_7d
  FROM (SELECT impressions FROM daily ORDER BY event_date DESC LIMIT 7)
),
last_day AS (SELECT MAX(event_date) AS d FROM daily)
SELECT
  forecast_date,
  level.ma_7d AS forecast_impressions
FROM level, last_day,
  UNNEST(GENERATE_DATE_ARRAY(DATE_ADD(last_day.d, INTERVAL 1 DAY),
                             DATE_ADD(last_day.d, INTERVAL 30 DAY))) AS forecast_date
ORDER BY forecast_date;
