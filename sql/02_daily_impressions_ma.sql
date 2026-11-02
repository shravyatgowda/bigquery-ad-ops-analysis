-- Daily impressions with a 7-day trailing moving average.
WITH daily AS (
  SELECT event_date, SUM(impressions) AS impressions
  FROM `YOUR_PROJECT.ad_ops.ad_events`
  GROUP BY event_date
)
SELECT
  event_date,
  impressions,
  AVG(impressions) OVER (ORDER BY event_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
FROM daily
ORDER BY event_date;
