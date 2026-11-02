-- Campaign-level KPIs: CTR, conversion rate, cost per click, ROI.
SELECT
  campaign_id,
  SUM(impressions)  AS impressions,
  SUM(clicks)       AS clicks,
  SUM(conversions)  AS conversions,
  SUM(spend)        AS spend,
  SUM(revenue)      AS revenue,
  SAFE_DIVIDE(SUM(clicks), SUM(impressions))                 AS ctr,
  SAFE_DIVIDE(SUM(conversions), SUM(clicks))                 AS cvr,
  SAFE_DIVIDE(SUM(spend), SUM(clicks))                       AS cpc,
  SAFE_DIVIDE(SUM(revenue) - SUM(spend), SUM(spend))         AS roi
FROM `YOUR_PROJECT.ad_ops.ad_events`
GROUP BY campaign_id
ORDER BY roi DESC;
