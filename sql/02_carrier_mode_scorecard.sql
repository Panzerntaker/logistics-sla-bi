SELECT 
    m.shipping_mode_name,
    m.sla_standard_days,
    COUNT(f.shipment_id) AS total_shipments,
    SUM(f.is_on_time) AS on_time_shipments,
    SUM(f.is_late) AS late_shipments,
    ROUND(100.0 * SUM(f.is_on_time) / COUNT(f.shipment_id), 2) AS otd_pct,
    ROUND(100.0 * SUM(f.is_late) / COUNT(f.shipment_id), 2) AS breach_rate_pct,
    ROUND(AVG(f.real_days), 2) AS avg_transit_days,
    ROUND(SUM(f.sales), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN f.is_late = 1 THEN f.sales ELSE 0 END), 2) AS delayed_revenue_at_risk,
    RANK() OVER (ORDER BY ROUND(100.0 * SUM(f.is_on_time) / COUNT(f.shipment_id), 2) DESC) AS otd_rank
FROM dim_shipping_modes m
JOIN fact_shipments f ON m.mode_id = f.mode_id
GROUP BY m.mode_id, m.shipping_mode_name, m.sla_standard_days
ORDER BY otd_rank;
