# Star Schema Data Model Documentation

This document outlines the dimensional modeling architecture for the **Logistics SLA & Delivery Operations BI Cockpit**. The data model follows a Kimball star schema methodology optimized for analytical query performance, tabular reporting, and Power BI VertiPaq engine compression.

**Source Dataset**: [Kaggle DataCo Global Supply Chain Dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

---

## 1. Conceptual & Physical Star Schema Architecture

```
                       +-----------------------------+
                       |        dim_calendar         |
                       +-----------------------------+
                       | PK  date_id (Date)          |
                       |     year                    |
                       |     quarter                 |
                       |     month                   |
                       |     month_name              |
                       |     year_month              |
                       +-----------------------------+
                                      |
                                      | 1
                                      |
                                      | * (order_date)
+-----------------------------+       |       +-----------------------------+
|     dim_shipping_modes      |       |       |         dim_regions         |
+-----------------------------+       |       +-----------------------------+
| PK  mode_id                 |       |       | PK  region_id               |
|     shipping_mode_name      |       |       |     order_region            |
|     sla_standard_days       |       |       |     market                  |
+-----------------------------+       |       +-----------------------------+
              \                       |                      /
               \ 1                    |                     / 1
                \                     |                    /
                 \                    |                   /
                  \ *                 |                  / *
              +-------------------------------------------------+
              |                 fact_shipments                  |
              +-------------------------------------------------+
              | PK  shipment_id (Order Item ID)                 |
              |     order_id                                    |
              | FK  order_date --------> dim_calendar.date_id   |
              |     shipping_date                               |
              | FK  mode_id -----------> dim_shipping_modes.id  |
              | FK  region_id ---------> dim_regions.region_id  |
              |     scheduled_days                              |
              |     real_days                                   |
              |     delay_days                                  |
              |     is_late                                     |
              |     is_on_time                                  |
              |     sales                                       |
              |     delivery_status                             |
              +-------------------------------------------------+
```

---

## 2. Table Relationships & Cardinality

| From Table (Dimension) | To Table (Fact) | Join Key | Cardinality | Cross-Filter Direction |
|---|---|---|---|---|
| `dim_calendar` | `fact_shipments` | `date_id` = `order_date` | 1-to-Many (`1:*`) | Single (Dimension filters Fact) |
| `dim_shipping_modes` | `fact_shipments` | `mode_id` = `mode_id` | 1-to-Many (`1:*`) | Single (Dimension filters Fact) |
| `dim_regions` | `fact_shipments` | `region_id` = `region_id` | 1-to-Many (`1:*`) | Single (Dimension filters Fact) |

---

## 3. Data Dictionary

### A. Fact Table: `fact_shipments`
Contains transaction-level shipment details, fulfillment timelines, and SLA metrics.

| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `shipment_id` | Integer | Primary Key | Unique shipment item identifier |
| `order_id` | Integer | Attribute | Associated customer order identifier |
| `order_date` | Date (YYYY-MM-DD) | Foreign Key | Date order was placed (`dim_calendar.date_id`) |
| `shipping_date` | Date (YYYY-MM-DD) | Attribute | Date parcel was shipped |
| `mode_id` | Integer | Foreign Key | Courier shipping method (`dim_shipping_modes.mode_id`) |
| `region_id` | Integer | Foreign Key | Destination region (`dim_regions.region_id`) |
| `scheduled_days` | Integer | Metric | Contracted / scheduled shipping days |
| `real_days` | Integer | Metric | Actual days taken to ship parcel |
| `delay_days` | Integer | Metric | Days exceeding SLA (`MAX(0, real_days - scheduled_days)`) |
| `is_late` | Integer (0/1) | Flag | 1 = Late delivery (SLA breach), 0 = On-time |
| `is_on_time` | Integer (0/1) | Flag | 1 = Delivered on-time / early, 0 = Late |
| `sales` | Decimal | Metric | Commercial sales value ($) |
| `delivery_status` | Text | Attribute | Status (`Late delivery`, `Advance shipping`, `Shipping on time`, `Shipping canceled`) |

### B. Dimension Table: `dim_shipping_modes`
Dimension table storing carrier shipping tiers and baseline SLA days.

| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `mode_id` | Integer | Primary Key | Unique mode identifier |
| `shipping_mode_name` | Text | Attribute | Carrier mode (`Standard Class`, `Second Class`, `First Class`, `Same Day`) |
| `sla_standard_days` | Integer | Attribute | Contractual baseline delivery window |

### C. Dimension Table: `dim_regions`
Geographic dimension mapping order regions to macro global markets.

| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `region_id` | Integer | Primary Key | Unique region identifier |
| `order_region` | Text | Attribute | Destination region (e.g. `Western Europe`, `Central America`) |
| `market` | Text | Attribute | Macro market (e.g. `Europe`, `LATAM`, `Pacific Asia`, `USCA`, `Africa`) |

### D. Dimension Table: `dim_calendar`
Role-playing calendar dimension for time intelligence and monthly trending.

| Column Name | Data Type | Key Type | Description |
|---|---|---|---|
| `date_id` | Date (YYYY-MM-DD) | Primary Key | ISO calendar date |
| `year` | Integer | Attribute | Calendar year |
| `quarter` | Text | Attribute | Calendar quarter (`Q1` to `Q4`) |
| `month` | Integer | Attribute | Month integer (1-12) |
| `month_name` | Text | Attribute | Month abbreviation (`Jan`, `Feb`, etc.) |
| `year_month` | Text | Attribute | Year-month formatted string (`YYYY-MM`) |
