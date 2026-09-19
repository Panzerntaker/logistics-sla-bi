SELECT 
    c.year,
    c.month,
    c.month_name,
    COUNT(f.shipment_id) AS total_shipments,
    SUM(f.is_on_time) AS on_time_shipments,
    SUM(f.is_late) AS late_shipments,
    ROUND(100.0 * SUM(f.is_on_time) / COUNT(f.shipment_id), 2) AS otd_pct,
    ROUND(100.0 * SUM(f.is_late) / COUNT(f.shipment_id), 2) AS breach_rate_pct,
    ROUND(AVG(f.real_days), 2) AS avg_transit_days,
    ROUND(SUM(f.sales), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN f.is_late = 1 THEN f.sales ELSE 0 END), 2) AS delayed_revenue_at_risk
FROM fact_shipments f
JOIN dim_calendar c ON f.order_date = c.date_id
WHERE c.year BETWEEN 2015 AND 2017
GROUP BY c.year, c.month, c.month_name
ORDER BY c.year, c.month;
