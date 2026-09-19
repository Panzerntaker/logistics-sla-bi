
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "logistics.db")
SQL_DIR = os.path.join(BASE_DIR, "sql")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "executive_logistics_kpi.md")


def run_query(conn, query_file):
    path = os.path.join(SQL_DIR, query_file)
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    cur = conn.cursor()
    cur.execute(sql)
    headers = [d[0] for d in cur.description]
    rows = cur.fetchall()
    return headers, rows


def format_table(headers, rows):
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        formatted_row = [
            f"{val:,.2f}" if isinstance(val, float) else f"{val:,}" if isinstance(val, int) else str(val)
            for val in row
        ]
        lines.append("| " + " | ".join(formatted_row) + " |")
    return "\n".join(lines)


def generate_report():
    conn = sqlite3.connect(DB_PATH)

    h_sla, r_sla = run_query(conn, "01_sla_breach_rate.sql")

    h_courier, r_courier = run_query(conn, "02_courier_scorecard.sql")

    h_pareto, r_pareto = run_query(conn, "03_bottleneck_pareto.sql")

    cur = conn.cursor()
    cur.execute(
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Executive KPI report generated at: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_report()
