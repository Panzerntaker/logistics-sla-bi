# Executive Logistics SLA & Delivery Operations KPI Report

**Reporting Scope**: Kaggle DataCo Global Supply Chain (180,519 shipments)  
**Database**: `data/logistics.db` (SQLite 3 Star Schema)  
**Timeframe**: 2015 - 2017 Operational History  

---

## 1. High-Level Executive Dashboard

| Metric | Value | Operational Benchmark | Status |
|---|---|---|---|
| **Total Shipments Evaluated** | 180,519 | - | Completed |
| **On-Time Delivery (OTD %)** | **45.17%** | >= 50.00% | Under Target (-4.83%) |
| **SLA Breach Rate** | **54.83%** | <= 50.00% | Critical (+4.83%) |
| **Total Late / Breached Shipments** | 98,977 | - | High Delay Concentration |
| **Total Gross Sales** | $36,784,735.01 | - | Global Volume |
| **Delayed Revenue at Risk** | **$20,126,395.27** | - | 54.7% Total Value Exposed |
| **Average Actual Transit Days** | 3.50 Days | <= 3.00 Days | +0.50 Days Above Target |

---

## 2. Carrier Mode Performance Scorecard

| Shipping Mode | Total Shipments | On-Time Deliveries | Late Deliveries | OTD % | Breach Rate % | Delayed Revenue at Risk |
|---|---|---|---|---|---|---|
| **Standard Class** | 107,752 | 66,729 | 41,023 | **61.93%** | 38.07% | $8,364,603.22 |
| **Same Day** | 9,737 | 5,283 | 4,454 | **54.26%** | 45.74% | $876,276.87 |
| **Second Class** | 35,216 | 8,229 | 26,987 | **23.37%** | 76.63% | $5,477,446.33 |
| **First Class** | 27,814 | 1,301 | 26,513 | **4.68%** | 95.32% | $5,408,068.46 |

### Core Operational Takeaways:
1. **First Class & Second Class Failure**:
   - `First Class` mode exhibits a catastrophic **95.32% SLA breach rate** (only 4.68% on-time). Scheduled expectations (1 day) are misaligned with actual fulfillment logistics.
   - `Second Class` mode exhibits a **76.63% breach rate**, exposing over **$5.48M** in customer orders to late arrivals.
2. **Standard Class Relative Reliability**:
   - `Standard Class` represents **59.7% of total network volume** and achieves the highest OTD rate at **61.93%**.

---

## 3. Regional Bottleneck Pareto (Top 5 Late Shipment Hubs)

| Market | Order Region | Total Shipments | Late Shipments | Breach Rate % | Total Delay Days | Delayed Revenue at Risk | Pareto Tier |
|---|---|---|---|---|---|---|---|
| **LATAM** | Central America | 28,341 | 15,518 | 54.75% | 26,187 | $3,110,260.17 | Top 80% Bottleneck |
| **Europe** | Western Europe | 27,109 | 15,140 | 55.85% | 25,839 | $3,292,013.58 | Top 80% Bottleneck |
| **LATAM** | South America | 14,935 | 8,111 | 54.31% | 13,807 | $1,606,545.89 | Top 80% Bottleneck |
| **Pacific Asia** | Oceania | 10,148 | 5,482 | 54.02% | 9,226 | $1,079,244.36 | Top 80% Bottleneck |
| **Pacific Asia** | Southeast Asia | 9,539 | 5,297 | 55.53% | 8,865 | $1,073,898.37 | Top 80% Bottleneck |

---

## 4. Immediate Operational Recommendations

1. **SLA Timeline Recalibration**:
   - Recalibrate contractual SLA promises for `First Class` and `Second Class` shipping modes. Current scheduled transit times are unrealistic given customs and cross-border transit constraints.
2. **Targeted Regional Interventions**:
   - Central America and Western Europe account for over **30,000 late deliveries** combined. Deploy dedicated regional fulfillment nodes to reduce transit legs.
3. **Automated Delay Exception Alerts**:
   - Implement real-time tracking triggers in Power BI / ERP when orders exceed scheduled dispatch time by > 24 hours.
