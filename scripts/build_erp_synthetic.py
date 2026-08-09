"""Generate synthetic Business Central-style ERP data and report visuals (public-safe)."""
from __future__ import annotations

import csv
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data" / "erp-synthetic"
IMG = ROOT / "assets" / "img" / "work" / "erp"

random.seed(7)
np.random.seed(7)

CUSTOMERS = [
    ("C-1001", "Northfield Parts"),
    ("C-1002", "Meridian Assemblies"),
    ("C-1003", "Coastal Components"),
    ("C-1004", "Summit Industrial"),
]
VENDORS = [
    ("V-2001", "Alloy Supplies Ltd"),
    ("V-2002", "Precision Fasteners"),
    ("V-2003", "Greenfield Plastics"),
]
ITEMS = [
    ("I-FG-01", "Finished assembly A", "Finished Good"),
    ("I-FG-02", "Finished assembly B", "Finished Good"),
    ("I-RM-01", "Raw material steel", "Raw Material"),
    ("I-RM-02", "Raw material polymer", "Raw Material"),
    ("I-SV-01", "Field service hour", "Service"),
]
LOCATIONS = ["MAIN", "WH-NORTH", "WH-SOUTH"]
PERIODS = [f"2026-{m:02d}" for m in range(1, 7)]


def build_dataset():
    DATA.mkdir(parents=True, exist_ok=True)

    sales_rows = []
    po_rows = []
    inv_rows = []
    val_rows = []
    so_id = 5000
    po_id = 7000

    for period in PERIODS:
        for cust_id, cust_name in CUSTOMERS:
            for _ in range(random.randint(2, 4)):
                item_id, item_name, item_type = random.choice(ITEMS)
                qty = random.randint(5, 40) if item_type != "Service" else random.randint(2, 16)
                unit = {
                    "Finished Good": random.uniform(180, 420),
                    "Raw Material": random.uniform(25, 90),
                    "Service": random.uniform(65, 110),
                }[item_type]
                amount = round(qty * unit, 2)
                status = random.choices(
                    ["Open", "Released", "Posted", "Partially shipped"],
                    weights=[0.15, 0.2, 0.5, 0.15],
                )[0]
                so_id += 1
                sales_rows.append(
                    {
                        "document_no": f"SO-{so_id}",
                        "period": period,
                        "customer_id": cust_id,
                        "customer_name": cust_name,
                        "item_id": item_id,
                        "item_name": item_name,
                        "item_type": item_type,
                        "qty": qty,
                        "amount_gbp": amount,
                        "status": status,
                        "dataset": "SYNTHETIC_PUBLIC_SAFE",
                    }
                )

        for vend_id, vend_name in VENDORS:
            for _ in range(random.randint(1, 3)):
                item_id, item_name, item_type = random.choice(
                    [i for i in ITEMS if i[2] != "Service"]
                )
                qty = random.randint(20, 120)
                unit = random.uniform(20, 95)
                amount = round(qty * unit, 2)
                days_open = random.randint(0, 45)
                status = "Open" if days_open > 7 else random.choice(["Open", "Received", "Invoiced"])
                po_id += 1
                po_rows.append(
                    {
                        "document_no": f"PO-{po_id}",
                        "period": period,
                        "vendor_id": vend_id,
                        "vendor_name": vend_name,
                        "item_id": item_id,
                        "item_name": item_name,
                        "qty": qty,
                        "amount_gbp": amount,
                        "days_open": days_open,
                        "status": status,
                        "dataset": "SYNTHETIC_PUBLIC_SAFE",
                    }
                )

    for loc in LOCATIONS:
        for item_id, item_name, item_type in ITEMS:
            if item_type == "Service":
                continue
            on_hand = random.randint(40, 380)
            unit_cost = random.uniform(18, 210)
            inv_rows.append(
                {
                    "as_of_period": "2026-06",
                    "location_code": loc,
                    "item_id": item_id,
                    "item_name": item_name,
                    "item_type": item_type,
                    "qty_on_hand": on_hand,
                    "unit_cost_gbp": round(unit_cost, 2),
                    "inventory_value_gbp": round(on_hand * unit_cost, 2),
                    "dataset": "SYNTHETIC_PUBLIC_SAFE",
                }
            )

    checks = [
        ("GL-BAL", "Trial balance nets to zero", "Pass", "Period close"),
        ("INV-NEG", "No negative on-hand quantities", "Pass", "Inventory"),
        ("SO-CUST", "Sales orders have valid customer", "Pass", "Sales"),
        ("PO-VEND", "Purchase orders have valid vendor", "Pass", "Purchasing"),
        ("POST-DATE", "Posted docs within open periods", "Warn", "Posting"),
        ("UOM-MAP", "Item UoM mapping complete", "Fail", "Master data"),
        ("DIM-COST", "Cost centre dimension populated", "Warn", "Dimensions"),
        ("AR-MATCH", "AR subledger vs G/L control", "Pass", "Finance"),
    ]
    for code, name, result, area in checks:
        val_rows.append(
            {
                "check_code": code,
                "check_name": name,
                "result": result,
                "area": area,
                "period": "2026-06",
                "dataset": "SYNTHETIC_PUBLIC_SAFE",
            }
        )

    def write(name, rows):
        path = DATA / name
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {path} rows={len(rows)}")

    write("fact_sales_orders.csv", sales_rows)
    write("fact_purchase_orders.csv", po_rows)
    write("fact_inventory.csv", inv_rows)
    write("dim_validation_checks.csv", val_rows)

    (DATA / "README.txt").write_text(
        "SYNTHETIC PUBLIC-SAFE ERP / BUSINESS CENTRAL-STYLE DATASET\n"
        "==========================================================\n"
        "Purpose: Demonstrate reporting, validation and stakeholder views\n"
        "around sales, purchasing and inventory — not employer BC data.\n\n"
        "Files:\n"
        "- fact_sales_orders.csv\n"
        "- fact_purchase_orders.csv\n"
        "- fact_inventory.csv\n"
        "- dim_validation_checks.csv\n\n"
        "Currency: GBP (synthetic)\n"
        "Disclaimer: Invented companies, items and figures only.\n",
        encoding="utf-8",
    )
    return sales_rows, po_rows, inv_rows, val_rows


def style_axes(ax, title: str):
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color="#0f3d4f", pad=10)
    ax.set_facecolor("#ffffff")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#c5d9e2")
    ax.spines["bottom"].set_color("#c5d9e2")
    ax.tick_params(colors="#5a6f7a", labelsize=9)
    ax.grid(axis="y", color="#d7e4ea", linewidth=0.8)


def watermark(fig):
    fig.text(
        0.99,
        0.01,
        "SYNTHETIC DATA · PUBLIC-SAFE · NOT EMPLOYER ERP",
        ha="right",
        va="bottom",
        fontsize=8,
        color="#e09f3e",
    )


def save(fig, name: str):
    IMG.mkdir(parents=True, exist_ok=True)
    path = IMG / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="#eef5f8")
    plt.close(fig)
    print(f"wrote {path}")


def chart_sales_by_customer(sales):
    period = "2026-06"
    totals = {}
    for r in sales:
        if r["period"] != period or r["status"] not in ("Posted", "Partially shipped", "Released"):
            continue
        totals[r["customer_name"]] = totals.get(r["customer_name"], 0) + float(r["amount_gbp"])
    names = list(totals.keys())
    values = [totals[n] / 1000 for n in names]

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.barh(names, values, color="#1a5f7a")
    style_axes(ax, "Sales order value by customer — Jun 2026 (synthetic)")
    ax.set_xlabel("GBP thousands")
    fig.text(0.12, 0.02, "BC-style sales documents · posted / released focus", fontsize=8, color="#5a6f7a")
    watermark(fig)
    save(fig, "01-sales-by-customer.png")


def chart_po_aging(pos):
    buckets = {"0-7 days": 0, "8-14 days": 0, "15-30 days": 0, "31+ days": 0}
    for r in pos:
        if r["status"] != "Open":
            continue
        d = int(r["days_open"])
        amt = float(r["amount_gbp"])
        if d <= 7:
            buckets["0-7 days"] += amt
        elif d <= 14:
            buckets["8-14 days"] += amt
        elif d <= 30:
            buckets["15-30 days"] += amt
        else:
            buckets["31+ days"] += amt

    labels = list(buckets.keys())
    values = [buckets[k] / 1000 for k in labels]

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.bar(labels, values, color=["#e09f3e", "#5a6f7a", "#123844", "#1a5f7a"])
    style_axes(ax, "Open purchase order aging — value by days open")
    ax.set_ylabel("GBP thousands (synthetic)")
    fig.text(0.12, 0.02, "Purchasing control view for UAT / operations reviews", fontsize=8, color="#5a6f7a")
    watermark(fig)
    save(fig, "02-po-aging.png")


def chart_inventory_value(inv):
    by_loc = {}
    for r in inv:
        loc = r["location_code"]
        by_loc[loc] = by_loc.get(loc, 0) + float(r["inventory_value_gbp"])
    labels = list(by_loc.keys())
    values = [by_loc[k] / 1000 for k in labels]

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.bar(labels, values, color="#1a5f7a")
    style_axes(ax, "Inventory value by location — as of Jun 2026")
    ax.set_ylabel("GBP thousands (synthetic)")
    fig.text(0.12, 0.02, "Location-level valuation from synthetic item ledger snapshot", fontsize=8, color="#5a6f7a")
    watermark(fig)
    save(fig, "03-inventory-by-location.png")


def chart_validation_board(vals):
    order = {"Pass": 0, "Warn": 1, "Fail": 2}
    rows = sorted(vals, key=lambda r: (order[r["result"]], r["area"]))

    fig, ax = plt.subplots(figsize=(10, 5.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(rows) + 1.5)
    ax.axis("off")
    ax.text(0.1, len(rows) + 0.85, "Period-close validation board — Jun 2026", fontsize=13, fontweight="bold", color="#0f3d4f")
    ax.text(0.1, len(rows) + 0.35, "Synthetic checks supporting UAT and reporting readiness", fontsize=9, color="#5a6f7a")

    colors = {"Pass": "#1a5f7a", "Warn": "#5a6f7a", "Fail": "#0f3d4f"}
    for i, r in enumerate(reversed(rows)):
        y = i + 0.35
        ax.add_patch(
            plt.Rectangle((0.1, y), 9.6, 0.85, fill=True, facecolor="#ffffff", edgecolor="#c5d9e2", linewidth=1)
        )
        ax.text(0.3, y + 0.42, r["check_code"], fontsize=9, fontweight="bold", color="#123844", va="center")
        ax.text(1.6, y + 0.42, r["check_name"], fontsize=9, color="#123844", va="center")
        ax.text(7.2, y + 0.42, r["area"], fontsize=8, color="#5a6f7a", va="center")
        ax.text(9.2, y + 0.42, r["result"].upper(), fontsize=9, fontweight="bold", color=colors[r["result"]], va="center", ha="right")

    watermark(fig)
    save(fig, "04-validation-board.png")


def chart_overview(sales, pos, inv, vals):
    period = "2026-06"
    sales_amt = sum(float(r["amount_gbp"]) for r in sales if r["period"] == period)
    open_po = sum(float(r["amount_gbp"]) for r in pos if r["status"] == "Open")
    inv_val = sum(float(r["inventory_value_gbp"]) for r in inv)
    fail_warn = sum(1 for r in vals if r["result"] in ("Fail", "Warn"))

    fig = plt.figure(figsize=(10, 5.8))
    fig.patch.set_facecolor("#eef5f8")
    fig.text(0.06, 0.94, "ERP Reporting Readiness — Synthetic BC-style", fontsize=16, fontweight="bold", color="#0f3d4f")
    fig.text(0.06, 0.895, "Sales · Purchasing · Inventory · Validation  |  Period: Jun 2026  |  Public-safe demo", fontsize=9, color="#5a6f7a")

    kpis = [
        ("Sales orders", f"£{sales_amt/1_000_000:.2f}m", "Document value"),
        ("Open POs", f"£{open_po/1000:.0f}k", "Purchasing backlog"),
        ("Inventory", f"£{inv_val/1_000_000:.2f}m", "On-hand value"),
        ("Open issues", str(fail_warn), "Warn + Fail checks"),
    ]
    for i, (label, val, sub) in enumerate(kpis):
        ax = fig.add_axes([0.06 + i * 0.23, 0.58, 0.20, 0.22])
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#c5d9e2")
        ax.set_facecolor("#ffffff")
        ax.text(0.08, 0.72, label.upper(), fontsize=8, color="#5a6f7a", transform=ax.transAxes)
        ax.text(0.08, 0.32, val, fontsize=15, fontweight="bold", color="#0f3d4f", transform=ax.transAxes)
        ax.text(0.08, 0.10, sub, fontsize=8, color="#5a6f7a", transform=ax.transAxes)

    # mini status mix
    axb = fig.add_axes([0.06, 0.12, 0.55, 0.36])
    statuses = {}
    for r in sales:
        if r["period"] != period:
            continue
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    labels = list(statuses.keys())
    counts = [statuses[k] for k in labels]
    axb.bar(labels, counts, color="#1a5f7a")
    style_axes(axb, "Sales document status mix")
    axb.set_ylabel("Count")

    axp = fig.add_axes([0.68, 0.12, 0.28, 0.36])
    result_counts = {"Pass": 0, "Warn": 0, "Fail": 0}
    for r in vals:
        result_counts[r["result"]] += 1
    axp.bar(list(result_counts.keys()), list(result_counts.values()), color=["#1a5f7a", "#5a6f7a", "#0f3d4f"])
    style_axes(axp, "Validation results")
    axp.set_ylabel("Checks")

    watermark(fig)
    save(fig, "05-report-overview.png")


def main():
    sales, pos, inv, vals = build_dataset()
    chart_sales_by_customer(sales)
    chart_po_aging(pos)
    chart_inventory_value(inv)
    chart_validation_board(vals)
    chart_overview(sales, pos, inv, vals)
    print("ERP Phase C assets ready")


if __name__ == "__main__":
    main()
