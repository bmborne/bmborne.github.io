"""Generate synthetic multi-entity finance data and report visuals (public-safe)."""
from __future__ import annotations

import csv
import random
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data" / "finance-synthetic"
IMG = ROOT / "assets" / "img" / "work" / "finance"

random.seed(42)
np.random.seed(42)


def build_dataset() -> list[dict]:
    DATA.mkdir(parents=True, exist_ok=True)
    entities = [("OPCO_A", "North Ops"), ("OPCO_B", "Central Ops"), ("OPCO_C", "South Ops")]
    accounts = [
        ("REV_PROD", "Product revenue", "Revenue"),
        ("REV_SERV", "Service revenue", "Revenue"),
        ("COGS", "Cost of sales", "COGS"),
        ("OPEX_SGA", "SG&A", "OpEx"),
        ("OPEX_RD", "R&D", "OpEx"),
    ]
    periods = [f"2025-{m:02d}" for m in range(1, 13)] + [f"2026-{m:02d}" for m in range(1, 7)]
    base_map = {
        "REV_PROD": 420000,
        "REV_SERV": 180000,
        "COGS": 260000,
        "OPEX_SGA": 110000,
        "OPEX_RD": 55000,
    }
    scale_map = {"OPCO_A": 1.0, "OPCO_B": 0.72, "OPCO_C": 0.55}

    rows: list[dict] = []
    for ent_id, ent_name in entities:
        for acc_id, acc_name, acc_type in accounts:
            base = base_map[acc_id] * scale_map[ent_id]
            for i, period in enumerate(periods):
                season = 1 + 0.08 * ((i % 12) / 11)
                actual = round(base * season * random.uniform(0.94, 1.08), 2)
                budget = round(base * season * random.uniform(0.98, 1.05), 2)
                forecast = round(((actual + budget) / 2) * random.uniform(0.97, 1.03), 2)
                for scenario, amount in (
                    ("Actual", actual),
                    ("Budget", budget),
                    ("Forecast", forecast),
                ):
                    rows.append(
                        {
                            "entity_id": ent_id,
                            "entity_name": ent_name,
                            "account_id": acc_id,
                            "account_name": acc_name,
                            "account_type": acc_type,
                            "period": period,
                            "scenario": scenario,
                            "amount_gbp": amount,
                            "currency": "GBP",
                            "dataset": "SYNTHETIC_PUBLIC_SAFE",
                        }
                    )

    fact = DATA / "fact_finance.csv"
    with fact.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with (DATA / "dim_entity.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["entity_id", "entity_name", "region"])
        w.writeheader()
        for e, n in entities:
            w.writerow({"entity_id": e, "entity_name": n, "region": n.split()[0]})

    with (DATA / "dim_account.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["account_id", "account_name", "account_type", "sort_order"])
        w.writeheader()
        for i, (a, n, t) in enumerate(accounts, 1):
            w.writerow({"account_id": a, "account_name": n, "account_type": t, "sort_order": i})

    (DATA / "README.txt").write_text(
        "SYNTHETIC PUBLIC-SAFE FINANCE DATASET\n"
        "====================================\n"
        "Purpose: Multi-entity management reporting demo (P&L, variance, MTD/YTD).\n"
        "Not employer data. Figures are invented for portfolio evidence.\n\n"
        "Files:\n"
        "- fact_finance.csv\n"
        "- dim_entity.csv\n"
        "- dim_account.csv\n\n"
        f"Rows in fact_finance: {len(rows)}\n"
        "Currency: GBP (synthetic)\n",
        encoding="utf-8",
    )
    print(f"dataset rows={len(rows)} -> {fact}")
    return rows


def load_fact(rows: list[dict] | None = None):
    if rows is None:
        with (DATA / "fact_finance.csv").open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    for r in rows:
        r["amount_gbp"] = float(r["amount_gbp"])
    return rows


def sum_filter(rows, **filters):
    total = 0.0
    for r in rows:
        if all(r[k] == v for k, v in filters.items()):
            total += r["amount_gbp"]
    return total


def pnl_for(rows, entity_name: str | None, period: str, scenario: str):
    def s(acc_type=None, account_id=None):
        total = 0.0
        for r in rows:
            if r["period"] != period or r["scenario"] != scenario:
                continue
            if entity_name and r["entity_name"] != entity_name:
                continue
            if acc_type and r["account_type"] != acc_type:
                continue
            if account_id and r["account_id"] != account_id:
                continue
            total += r["amount_gbp"]
        return total

    rev = s(acc_type="Revenue")
    cogs = s(account_id="COGS")
    opex = s(acc_type="OpEx")
    gp = rev - cogs
    op = gp - opex
    return {"Revenue": rev, "COGS": cogs, "Gross profit": gp, "OpEx": opex, "Operating profit": op}


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
        "SYNTHETIC DATA · PUBLIC-SAFE · NOT EMPLOYER REPORTING",
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


def chart_entity_variance(rows):
    period = "2026-06"
    entities = ["North Ops", "Central Ops", "South Ops"]
    actual = []
    budget = []
    for e in entities:
        a = pnl_for(rows, e, period, "Actual")["Operating profit"]
        b = pnl_for(rows, e, period, "Budget")["Operating profit"]
        actual.append(a / 1000)
        budget.append(b / 1000)

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    x = np.arange(len(entities))
    w = 0.36
    ax.bar(x - w / 2, actual, w, label="Actual", color="#1a5f7a")
    ax.bar(x + w / 2, budget, w, label="Budget", color="#e09f3e")
    style_axes(ax, "Operating profit by entity — Actual vs Budget (Jun 2026)")
    ax.set_xticks(x)
    ax.set_xticklabels(entities)
    ax.set_ylabel("GBP thousands (synthetic)")
    ax.legend(frameon=False, fontsize=9)
    fig.text(0.12, 0.02, "Management view · multi-entity · synthetic OpCos", fontsize=8, color="#5a6f7a")
    watermark(fig)
    save(fig, "01-entity-variance.png")


def chart_trend(rows):
    periods = [f"2025-{m:02d}" for m in range(1, 13)] + [f"2026-{m:02d}" for m in range(1, 7)]
    actual, budget = [], []
    for p in periods:
        actual.append(pnl_for(rows, None, p, "Actual")["Operating profit"] / 1000)
        budget.append(pnl_for(rows, None, p, "Budget")["Operating profit"] / 1000)

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.plot(periods, actual, color="#1a5f7a", linewidth=2.2, label="Actual")
    ax.plot(periods, budget, color="#e09f3e", linewidth=2.0, linestyle="--", label="Budget")
    style_axes(ax, "Group operating profit trend — Actual vs Budget")
    ax.set_ylabel("GBP thousands (synthetic)")
    ax.set_xticks(periods[::2])
    ax.tick_params(axis="x", rotation=45)
    ax.legend(frameon=False, fontsize=9)
    fig.text(0.12, 0.02, "YTD path across synthetic group total", fontsize=8, color="#5a6f7a")
    watermark(fig)
    save(fig, "02-group-trend.png")


def chart_pnl_bridge(rows):
    period = "2026-06"
    act = pnl_for(rows, None, period, "Actual")
    bud = pnl_for(rows, None, period, "Budget")
    labels = ["Budget OP", "Rev var", "COGS var", "OpEx var", "Actual OP"]
    rev_var = (act["Revenue"] - bud["Revenue"]) / 1000
    cogs_var = -((act["COGS"] - bud["COGS"]) / 1000)  # lower COGS helps
    opex_var = -((act["OpEx"] - bud["OpEx"]) / 1000)
    values = [
        bud["Operating profit"] / 1000,
        rev_var,
        cogs_var,
        opex_var,
        act["Operating profit"] / 1000,
    ]

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    colors = ["#e09f3e", "#1a5f7a", "#1a5f7a", "#1a5f7a", "#1a5f7a"]
    ax.bar(labels, values, color=colors)
    style_axes(ax, "P&L variance bridge — Budget to Actual (Jun 2026)")
    ax.set_ylabel("GBP thousands (synthetic)")
    fig.text(0.12, 0.02, "Illustrative bridge from semantic measures (synthetic)", fontsize=8, color="#5a6f7a")
    watermark(fig)
    save(fig, "03-pnl-bridge.png")


def chart_report_mock(rows):
    """Single composed 'report page' still."""
    period = "2026-06"
    act = pnl_for(rows, None, period, "Actual")
    bud = pnl_for(rows, None, period, "Budget")

    fig = plt.figure(figsize=(10, 5.8))
    fig.patch.set_facecolor("#eef5f8")
    fig.text(0.06, 0.94, "Group Management Reporting", fontsize=16, fontweight="bold", color="#0f3d4f")
    fig.text(0.06, 0.895, "Synthetic multi-entity finance model  |  Period: Jun 2026  |  Scenario: Actual vs Budget", fontsize=9, color="#5a6f7a")

    # KPI cards
    kpis = [
        ("Revenue", act["Revenue"], act["Revenue"] - bud["Revenue"]),
        ("Gross profit", act["Gross profit"], act["Gross profit"] - bud["Gross profit"]),
        ("Operating profit", act["Operating profit"], act["Operating profit"] - bud["Operating profit"]),
    ]
    for i, (label, val, var) in enumerate(kpis):
        x0 = 0.06 + i * 0.30
        ax = fig.add_axes([x0, 0.62, 0.27, 0.20])
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#c5d9e2")
        ax.set_facecolor("#ffffff")
        ax.text(0.06, 0.70, label.upper(), fontsize=8, color="#5a6f7a", transform=ax.transAxes)
        ax.text(0.06, 0.28, f"£{val/1_000_000:.2f}m", fontsize=16, fontweight="bold", color="#0f3d4f", transform=ax.transAxes)
        sign = "+" if var >= 0 else ""
        ax.text(0.06, 0.08, f"vs budget {sign}£{var/1000:.0f}k", fontsize=8, color="#5a6f7a", transform=ax.transAxes)

    # small entity bars
    axb = fig.add_axes([0.06, 0.12, 0.55, 0.40])
    entities = ["North Ops", "Central Ops", "South Ops"]
    actual = [pnl_for(rows, e, period, "Actual")["Operating profit"] / 1000 for e in entities]
    budget = [pnl_for(rows, e, period, "Budget")["Operating profit"] / 1000 for e in entities]
    x = np.arange(len(entities))
    axb.bar(x - 0.18, actual, 0.36, color="#1a5f7a", label="Actual")
    axb.bar(x + 0.18, budget, 0.36, color="#e09f3e", label="Budget")
    style_axes(axb, "Operating profit by OpCo")
    axb.set_xticks(x)
    axb.set_xticklabels(entities)
    axb.set_ylabel("£000")
    axb.legend(frameon=False, fontsize=8)

    # account mix
    axp = fig.add_axes([0.68, 0.12, 0.28, 0.40])
    rev_prod = sum_filter(rows, period=period, scenario="Actual", account_id="REV_PROD")
    rev_serv = sum_filter(rows, period=period, scenario="Actual", account_id="REV_SERV")
    axp.pie(
        [rev_prod, rev_serv],
        labels=["Product", "Service"],
        colors=["#1a5f7a", "#e09f3e"],
        textprops={"fontsize": 8, "color": "#123844"},
    )
    axp.set_title("Revenue mix", loc="left", fontsize=11, fontweight="bold", color="#0f3d4f")

    watermark(fig)
    save(fig, "04-report-overview.png")


def main():
    rows = build_dataset()
    rows = load_fact(rows)
    chart_entity_variance(rows)
    chart_trend(rows)
    chart_pnl_bridge(rows)
    chart_report_mock(rows)
    print("B2 assets ready")


if __name__ == "__main__":
    main()
