import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "logistics.db")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "dashboard_overview.png")

conn = sqlite3.connect(DB_PATH)

courier_df = pd.read_sql_query(    SELECT cal.month_name, cal.month_number,
           ROUND(100.0 * SUM(s.is_sla_breached) / COUNT(*), 1) as breach_pct
    FROM fact_shipments s
    JOIN dim_calendar cal ON s.order_date = cal.date_key
    GROUP BY cal.month_number, cal.month_name
    ORDER BY cal.month_number
    SELECT r.corridor_name,
           SUM(s.delay_days) as total_delay_days
    FROM fact_shipments s
    JOIN dim_routes r ON s.route_id = r.route_id
    WHERE s.is_sla_breached = 1
    GROUP BY r.corridor_name
    ORDER BY total_delay_days ASC
""", conn)

conn.close()

fig = plt.figure(figsize=(13, 8), dpi=200)
fig.patch.set_facecolor("#f8f9fa")
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], hspace=0.35, wspace=0.25)

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor("#ffffff")
bars = ax1.barh(courier_df['courier_name'], courier_df['otd_pct'], color="#2b5c8f", height=0.55)
ax1.set_xlim(75, 100)
ax1.axvline(90, color="#d9534f", linestyle="--", alpha=0.7, label="90% Target")
ax1.set_title("On-Time Delivery (OTD %) by Courier", fontsize=11, fontweight="bold", pad=8)
ax1.set_xlabel("OTD %")
for bar in bars:
    w = bar.get_width()
    ax1.text(w + 0.3, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va="center", fontsize=9)
ax1.legend(loc="lower right")
ax1.grid(axis="x", alpha=0.3)

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor("#ffffff")
ax2.plot(monthly_df['month_name'], monthly_df['breach_pct'], marker="o", color="#d9534f", linewidth=2)
ax2.set_title("Monthly SLA Breach Rate Trend (%)", fontsize=11, fontweight="bold", pad=8)
ax2.set_ylabel("Breach Rate (%)")
ax2.set_ylim(5, 20)
plt.setp(ax2.get_xticklabels(), rotation=35, ha="right", fontsize=8)
for x, y in zip(monthly_df['month_name'], monthly_df['breach_pct']):
    ax2.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8)
ax2.grid(True, alpha=0.3)

ax3 = fig.add_subplot(gs[1, :])
ax3.set_facecolor("#ffffff")
colors = ["#2b5c8f" if d < 400 else "#d9534f" for d in route_df['total_delay_days']]
bars3 = ax3.barh(route_df['corridor_name'], route_df['total_delay_days'], color=colors, height=0.6)
ax3.set_title("Total Delay Days by Shipping Route (Red = Top Bottlenecks)", fontsize=11, fontweight="bold", pad=8)
ax3.set_xlabel("Cumulative Delay Days")
for bar in bars3:
    w = bar.get_width()
    ax3.text(w + 5, bar.get_y() + bar.get_height()/2, f"{int(w)} days", va="center", fontsize=9)
ax3.grid(axis="x", alpha=0.3)

plt.suptitle("Logistics SLA & Delivery Performance Dashboard", fontsize=15, fontweight="bold", y=0.98)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, bbox_inches="tight")
plt.close()
print(f"Generated dashboard overview at: {OUTPUT_PATH}")
