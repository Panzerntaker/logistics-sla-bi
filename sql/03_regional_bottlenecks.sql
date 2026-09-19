WITH region_stats AS (
    SELECT 
        r.market,
        r.order_region,
        COUNT(f.shipment_id) AS total_shipments,
        SUM(f.is_late) AS late_shipments,
        ROUND(100.0 * SUM(f.is_late) / COUNT(f.shipment_id), 2) AS breach_rate_pct,
        SUM(f.delay_days) AS total_delay_days,
        ROUND(SUM(CASE WHEN f.is_late = 1 THEN f.sales ELSE 0 END), 2) AS delayed_revenue_at_risk
    FROM dim_regions r
    JOIN fact_shipments f ON r.region_id = f.region_id
    GROUP BY r.market, r.order_region
),
ranked AS (
    SELECT 
        market,
        order_region,
        total_shipments,
        late_shipments,
        breach_rate_pct,
        total_delay_days,
        delayed_revenue_at_risk,
        ROUND(100.0 * total_delay_days / SUM(total_delay_days) OVER (), 2) AS delay_share_pct,
        SUM(total_delay_days) OVER (ORDER BY total_delay_days DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_delay_days,
        ROUND(100.0 * SUM(total_delay_days) OVER (ORDER BY total_delay_days DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / SUM(total_delay_days) OVER (), 2) AS cum_delay_pct
    FROM region_stats
)
SELECT 
    market,
    order_region,
    total_shipments,
    late_shipments,
    breach_rate_pct,
    total_delay_days,
    delay_share_pct,
    cum_delay_pct,
    delayed_revenue_at_risk,
    CASE 
        WHEN cum_delay_pct <= 80.0 THEN 'Top 80% Bottleneck'
        WHEN LAG(cum_delay_pct, 1, 0.0) OVER (ORDER BY total_delay_days DESC) < 80.0 THEN 'Top 80% Bottleneck'
        ELSE 'Long-Tail Region'
    END AS pareto_tier
FROM ranked
ORDER BY total_delay_days DESC;
