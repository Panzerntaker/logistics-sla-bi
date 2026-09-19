# Power BI Desktop Dashboard Layout & Visual Specification

**Dashboard Title**: Logistics SLA & Delivery Operations BI Cockpit  
**Target Resolution**: 16:9 Widescreen Canvas (`1920 x 1080` or `1280 x 720` standard)  
**Target Audience**: VP of Supply Chain, Director of Logistics Operations, Carrier Relationship Managers.

---

## 1. ASCII Canvas Wireframe (Single-Page Executive Layout)

```
+---------------------------------------------------------------------------------------------------------+
| LOGISTICS SLA & DELIVERY OPERATIONS COCKPIT                                  Filters: [Year] [Quarter]  |
+------------------------------------+------------------------------------+-------------------------------+
| KPI CARD 1                         | KPI CARD 2                         | KPI CARD 3                    | KPI CARD 4
| Total Shipments                    | On-Time Delivery (OTD %)           | SLA Breach Rate %             | Revenue at Risk
| 11,250                             | 89.26% (Target: >=92.0%)           | 10.74% (Tol: <=8.0%)          | $1,191,895
+------------------------------------+------------------------------------+-------------------------------+
| PRIMARY NARRATIVE VISUAL (ANCHOR: 58% Width)                            | SUPPORTING VISUAL 1 (40% W)   |
| Visual: Line and Clustered Column Chart                                 | Visual: Clustered Bar Chart   |
| Title: Monthly Shipment Volume vs. SLA Breach Trend                     | Title: Courier Reliability    |
| (Volume on Y1, Breach Rate % on Y2, Month on X-Axis)                    | Scorecard (OTD % by Courier)  |
|                                                                         |                               |
|                                                                         |                               |
|                                                                         |                               |
+-------------------------------------------------------------------------+-------------------------------+
| SUPPORTING VISUAL 2 (58% Width)                                         | SUPPORTING VISUAL 3 (40% W)   |
| Visual: Pareto Dual-Axis Combo Chart                                    | Visual: Treemap               |
| Title: Route Corridor Bottleneck Pareto: Cumulative Delay Days          | Title: Root-Cause Driver      |
| (Corridor on X, Delay Days on Bar Y1, Cum % Line on Y2)                 | Breakdown for Delayed Parcels |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Global Palette & Typography Spec

- **Background**: Canvas background `#F4F6F9` (Light Slate Gray), Card backgrounds `#FFFFFF` with 2px corner radius and subtle drop shadow.
- **Primary Color (Corporate Navy)**: `#1E293B` (Headers, baseline bars, axis labels).
- **Accent / On-Time (Emerald Green)**: `#059669` (Target achieved, on-time indicators).
- **Warning / At-Risk (Amber Yellow)**: `#D97706` (Moderate breach rate, caution zones).
- **Critical / Breach (Crimson Red)**: `#DC2626` (SLA violations, revenue at risk, bottleneck bars).
- **Typography**: `Segoe UI` or `Aptos` (Standard Power BI system fonts):
  - Canvas Header: 20pt Bold (`#0F172A`)
  - KPI Card Callouts: 28pt Bold (`#1E293B`)
  - KPI Card Labels: 10pt Regular (`#64748B`)
  - Visual Titles: 12pt Bold (`#1E293B`)

---

## 3. Visual Configuration Specifications

### Row 1: Executive KPI Cards (Top Rail)

#### Card 1: Total Volume
- **Visual Type**: Card (New or Standard)
- **Field**: `[Total Shipments]`
- **Format / Title**: Total Shipments Dispatched
- **Callout Value**: Integer formatted (`11,250`)
- **Key Insight**: Overall fulfillment throughput across all 6 courier networks.

#### Card 2: On-Time Delivery Benchmark
- **Visual Type**: Card (New) with accent bar
- **Field**: `[OTD %]`
- **Reference Label**: Target: 92.00% (Variance: -2.74%)
- **Format / Title**: On-Time Delivery Rate (OTD %)
- **Callout Color**: `#DC2626` (Red if < 92%, Green if >= 92%)
- **Key Insight**: Primary operational contractual metric evaluating carrier timeliness.

#### Card 3: SLA Breach Exposure
- **Visual Type**: Card (New)
- **Field**: `[SLA Breach Rate %]`
- **Reference Label**: Max Tolerance: 8.00%
- **Format / Title**: SLA Breach Rate %
- **Callout Color**: `#DC2626`
- **Key Insight**: Proportion of dispatches failing service level agreements.

#### Card 4: Delayed Revenue at Risk
- **Visual Type**: Card (Standard)
- **Field**: `[Delayed Revenue at Risk]`
- **Format / Title**: Commercial Revenue at Risk
- **Callout Value**: Currency formatted (`$1,191,895`)
- **Key Insight**: Dollar value of merchandise stalled in late transit risking customer churn.

---

### Row 2: Operational Trend & Courier Performance

#### Visual 1 (Anchor): Monthly Shipment Volume vs. SLA Breach Trend
- **Visual Type**: Line and clustered column chart
- **X Axis**: `dim_calendar[month_name]` (Sorted by `dim_calendar[month_number]`)
- **Column Y Axis**: `[Total Shipments]` (Bar color: `#94A3B8`)
- **Line Y Axis**: `[SLA Breach Rate %]` (Line color: `#DC2626`, Stroke width: 3px)
- **Title**: `Monthly Shipment Volume vs. SLA Breach Trend: Severe Spike in Q4 Holiday Peak`
- **Key Insight**: Highlights Q4 delivery stress where breach rate jumps from ~9% to ~13.7%.

#### Visual 2 (Right Anchor): Courier Reliability Scorecard
- **Visual Type**: Clustered bar chart (Horizontal)
- **Y Axis**: `dim_couriers[courier_name]` (Sorted by `[OTD %]` descending)
- **X Axis**: `[OTD %]`
- **Data Labels**: Enabled, formatted as percentage (`##.0%`)
- **Reference Line**: Constant line at `92.0%` (Dashed, `#059669`)
- **Title**: `Courier Reliability Scorecard: Velocity Prime & SwiftHaul Lead; Titan Lags at 84.3%`
- **Key Insight**: Directly benchmarks carrier partners against the 92% SLA threshold.

---

### Row 3: Corridor Bottlenecks & Delay Drivers

#### Visual 3 (Left Bottom): Route Corridor Bottleneck Pareto
- **Visual Type**: Line and clustered column chart
- **X Axis**: `dim_routes[corridor_name]` (Sorted by `[Total Delay Days]` descending)
- **Column Y Axis**: `[Total Delay Days]` (Bar color: `#1E293B`)
- **Line Y Axis**: Cumulative % (Calculated DAX measure or custom column `cum_delay_pct`)
- **Reference Line**: Constant line at `80.0%` on Secondary Y-Axis
- **Title**: `Route Corridor Bottleneck Pareto: Top 7 Corridors Generate 81% of Cumulative Delay Days`
- **Key Insight**: Proves that focusing intervention on ORD-LAX and LAX-DFW resolves the majority of network delay impact.

#### Visual 4 (Right Bottom): Delay Root-Cause Driver Breakdown
- **Visual Type**: Treemap
- **Category**: `fact_shipments[delay_reason]` (Filtered where `delay_reason != 'None'`)
- **Values**: `[Total Delay Days]`
- **Color Saturation**: `[Delayed Revenue at Risk]`
- **Title**: `Root-Cause Driver Breakdown: Hub Sorting Congestion Dominates Network Delay`
- **Key Insight**: Pinpoints operational bottlenecks inside sorting facilities versus uncontrollable weather factors.

---

## 4. Interactive Slicers & Cross-Filtering
- **Quarter Slicer**: Buttons or dropdown (`Q1`, `Q2`, `Q3`, `Q4`) placed in top-right header.
- **Service Tier Slicer**: Horizontal pills (`Next-Day Air`, `Express Ground`, `Standard Freight`, `Regional Parcel`).
- **Interaction Rule**: Selecting a courier in the Scorecard filters the Route Pareto and Monthly Trend to reveal lane-specific performance.
