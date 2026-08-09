"""Generate remaining Work evidence: telecom, AI framework, Fabric walkthrough, demo GIF."""
from __future__ import annotations

import csv
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
random.seed(21)
np.random.seed(21)


def watermark(fig, text="SYNTHETIC DATA · PUBLIC-SAFE"):
    fig.text(0.99, 0.01, text, ha="right", va="bottom", fontsize=8, color="#e09f3e")


def style_axes(ax, title: str):
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color="#0f3d4f", pad=10)
    ax.set_facecolor("#ffffff")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#c5d9e2")
    ax.spines["bottom"].set_color("#c5d9e2")
    ax.tick_params(colors="#5a6f7a", labelsize=9)
    ax.grid(axis="y", color="#d7e4ea", linewidth=0.8)


def save(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="#eef5f8")
    plt.close(fig)
    print(f"wrote {path}")


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path} rows={len(rows)}")


# ---------------------------------------------------------------------------
# Telecom / Phase D
# ---------------------------------------------------------------------------

def build_telecom():
    data = ROOT / "assets" / "data" / "telecom-synthetic"
    img = ROOT / "assets" / "img" / "work" / "telecom"

    sites = [f"SITE-{i:03d}" for i in range(1, 13)]
    bronze, silver, gold = [], [], []
    ts = 0
    for day in range(14):
        for site in sites:
            for hour in range(0, 24, 2):
                ts += 1
                raw = round(random.uniform(40, 95) + (8 if random.random() < 0.04 else 0), 2)
                bronze.append(
                    {
                        "event_id": f"B-{ts:05d}",
                        "day_index": day,
                        "hour": hour,
                        "site_token": site,
                        "metric_raw": raw,
                        "layer": "bronze",
                        "pii_status": "tokenised",
                        "dataset": "SYNTHETIC_PUBLIC_SAFE",
                    }
                )
                cleaned = round(raw * random.uniform(0.98, 1.0), 2)
                silver.append(
                    {
                        "event_id": f"S-{ts:05d}",
                        "day_index": day,
                        "hour": hour,
                        "site_token": site,
                        "metric_clean": cleaned,
                        "dq_flag": "ok" if cleaned < 92 else "review",
                        "layer": "silver",
                        "dataset": "SYNTHETIC_PUBLIC_SAFE",
                    }
                )
                score = round(max(0, (cleaned - 78) / 20 + random.uniform(-0.05, 0.12)), 3)
                gold.append(
                    {
                        "event_id": f"G-{ts:05d}",
                        "day_index": day,
                        "hour": hour,
                        "site_token": site,
                        "anomaly_score": score,
                        "is_anomaly": int(score >= 0.75),
                        "layer": "gold",
                        "dataset": "SYNTHETIC_PUBLIC_SAFE",
                    }
                )

    tests = [
        ("T-01", "Bronze schema present", "Pass", "ingest"),
        ("T-02", "Site tokens only (no raw IDs)", "Pass", "privacy"),
        ("T-03", "Silver null rate < 1%", "Pass", "dq"),
        ("T-04", "Gold score in [0,1]", "Pass", "model"),
        ("T-05", "Run control: dry-run gate", "Pass", "ops"),
        ("T-06", "Production credentials absent", "Pass", "safety"),
        ("T-07", "Anomaly rate sanity band", "Warn", "model"),
    ]
    test_rows = [
        {
            "test_id": a,
            "test_name": b,
            "result": c,
            "area": d,
            "dataset": "SYNTHETIC_PUBLIC_SAFE",
        }
        for a, b, c, d in tests
    ]

    write_csv(data / "bronze_events.csv", bronze)
    write_csv(data / "silver_events.csv", silver)
    write_csv(data / "gold_scores.csv", gold)
    write_csv(data / "run_tests.csv", test_rows)
    (data / "README.txt").write_text(
        "SYNTHETIC TELECOM OPERATIONS ANOMALY DATASET\n"
        "============================================\n"
        "Public-safe layered demo (bronze / silver / gold).\n"
        "No operator environments, credentials or real network IDs.\n"
        "Site codes are invented tokens only.\n",
        encoding="utf-8",
    )

    # Layer volume chart
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.bar(["Bronze", "Silver", "Gold"], [len(bronze), len(silver), len(gold)], color="#1a5f7a")
    style_axes(ax, "Layered pipeline volume — synthetic telemetry events")
    ax.set_ylabel("Rows")
    fig.text(0.12, 0.02, "Same grain retained; controls add quality and scores", fontsize=8, color="#5a6f7a")
    watermark(fig, "SYNTHETIC · PUBLIC-SAFE · NOT OPERATOR DATA")
    save(fig, img / "01-layer-volumes.png")

    # Anomaly timeline (group mean score by day)
    by_day = {}
    for r in gold:
        by_day.setdefault(r["day_index"], []).append(float(r["anomaly_score"]))
    days = sorted(by_day)
    means = [sum(by_day[d]) / len(by_day[d]) for d in days]
    flags = [sum(1 for r in gold if r["day_index"] == d and r["is_anomaly"]) for d in days]

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.plot(days, means, color="#1a5f7a", linewidth=2.2, label="Mean anomaly score")
    ax.axhline(0.75, color="#e09f3e", linestyle="--", linewidth=1.2, label="Review threshold")
    style_axes(ax, "Mean anomaly score by day — synthetic gold layer")
    ax.set_xlabel("Day index")
    ax.set_ylabel("Score")
    ax.legend(frameon=False, fontsize=9)
    fig.text(0.12, 0.02, f"Flagged events across window: {sum(flags)}", fontsize=8, color="#5a6f7a")
    watermark(fig, "SYNTHETIC · PUBLIC-SAFE · NOT OPERATOR DATA")
    save(fig, img / "02-anomaly-timeline.png")

    # Test board
    fig, ax = plt.subplots(figsize=(10, 5.2))
    fig.patch.set_facecolor("#eef5f8")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(test_rows) + 1.5)
    ax.axis("off")
    ax.text(0.1, len(test_rows) + 0.85, "Run controls & automated tests", fontsize=13, fontweight="bold", color="#0f3d4f")
    ax.text(0.1, len(test_rows) + 0.35, "Safety-gated pipeline checks (synthetic)", fontsize=9, color="#5a6f7a")
    for i, r in enumerate(reversed(test_rows)):
        y = i + 0.35
        ax.add_patch(plt.Rectangle((0.1, y), 9.6, 0.85, fill=True, facecolor="#ffffff", edgecolor="#c5d9e2"))
        ax.text(0.3, y + 0.42, r["test_id"], fontsize=9, fontweight="bold", color="#123844", va="center")
        ax.text(1.5, y + 0.42, r["test_name"], fontsize=9, color="#123844", va="center")
        ax.text(7.0, y + 0.42, r["area"], fontsize=8, color="#5a6f7a", va="center")
        ax.text(9.2, y + 0.42, r["result"].upper(), fontsize=9, fontweight="bold", color="#1a5f7a", va="center", ha="right")
    watermark(fig, "SYNTHETIC · PUBLIC-SAFE · NOT OPERATOR DATA")
    save(fig, img / "03-run-controls.png")

    # Overview
    fig = plt.figure(figsize=(10, 5.6))
    fig.patch.set_facecolor("#eef5f8")
    fig.text(0.06, 0.92, "Telecom anomaly pipeline — synthetic overview", fontsize=16, fontweight="bold", color="#0f3d4f")
    fig.text(0.06, 0.875, "Bronze → Silver → Gold · privacy tokens · tests · run controls", fontsize=9, color="#5a6f7a")
    kpis = [
        ("Bronze rows", f"{len(bronze):,}"),
        ("Sites (tokens)", str(len(sites))),
        ("Anomalies", str(sum(int(r["is_anomaly"]) for r in gold))),
        ("Tests pass", f"{sum(1 for r in test_rows if r['result']=='Pass')}/{len(test_rows)}"),
    ]
    for i, (label, val) in enumerate(kpis):
        ax = fig.add_axes([0.06 + i * 0.23, 0.52, 0.20, 0.24])
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#c5d9e2")
        ax.set_facecolor("#ffffff")
        ax.text(0.08, 0.62, label.upper(), fontsize=8, color="#5a6f7a", transform=ax.transAxes)
        ax.text(0.08, 0.22, val, fontsize=16, fontweight="bold", color="#0f3d4f", transform=ax.transAxes)

    axb = fig.add_axes([0.06, 0.12, 0.88, 0.30])
    dq = sum(1 for r in silver if r["dq_flag"] == "review")
    axb.bar(["Clean", "DQ review"], [len(silver) - dq, dq], color=["#1a5f7a", "#e09f3e"])
    style_axes(axb, "Silver data-quality flags")
    axb.set_ylabel("Events")
    watermark(fig, "SYNTHETIC · PUBLIC-SAFE · NOT OPERATOR DATA")
    save(fig, img / "04-pipeline-overview.png")

    # Flow SVG maintained separately as colored static asset (assets/img/work/telecom-flow.svg)
    print("telecom stills ready (SVG kept as static colored asset)")


# ---------------------------------------------------------------------------
# Applied AI framework
# ---------------------------------------------------------------------------

def build_ai():
    data = ROOT / "assets" / "data" / "ai-framework"
    img = ROOT / "assets" / "img" / "work" / "ai"

    cases = [
        ("Forecast cash collection", 4, 3, 2, 2, "Pilot"),
        ("Invoice anomaly flags", 5, 4, 3, 2, "Pilot"),
        ("Auto-generate board packs", 3, 2, 4, 4, "Hold"),
        ("Chat over ERP tables", 2, 2, 5, 5, "Hold"),
        ("Demand forecast (SKU)", 4, 3, 3, 3, "Assess"),
        ("Vendor risk scoring", 3, 3, 3, 3, "Assess"),
    ]
    rows = []
    for name, value, readiness, complexity, risk, decision in cases:
        score = round((value * 2 + readiness * 2 - complexity - risk) / 4, 2)
        rows.append(
            {
                "use_case": name,
                "value": value,
                "data_readiness": readiness,
                "complexity": complexity,
                "operational_risk": risk,
                "priority_score": score,
                "decision": decision,
                "dataset": "SYNTHETIC_PUBLIC_SAFE",
            }
        )
    write_csv(data / "opportunity_scores.csv", rows)
    (data / "README.txt").write_text(
        "APPLIED AI OPPORTUNITY ASSESSMENT (SYNTHETIC EXAMPLES)\n"
        "=====================================================\n"
        "Scores 1-5 on value, readiness, complexity, risk.\n"
        "Decisions: Pilot / Assess / Hold. Not client AI systems.\n",
        encoding="utf-8",
    )

    # Score table visual
    fig, ax = plt.subplots(figsize=(10, 5.4))
    fig.patch.set_facecolor("#eef5f8")
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(rows) + 2)
    ax.text(0.2, len(rows) + 1.2, "AI opportunity assessment — synthetic scoring board", fontsize=13, fontweight="bold", color="#222")
    ax.text(0.2, len(rows) + 0.7, "Value · readiness · complexity · risk → Pilot / Assess / Hold", fontsize=9, color="#666")
    headers = ["Use case", "Val", "Ready", "Cx", "Risk", "Score", "Decision"]
    xs = [0.2, 4.4, 5.2, 6.1, 6.9, 7.8, 8.7]
    for x, h in zip(xs, headers):
        ax.text(x, len(rows) + 0.15, h, fontsize=8, fontweight="bold", color="#777")
    for i, r in enumerate(reversed(rows)):
        y = i + 0.25
        ax.add_patch(plt.Rectangle((0.15, y), 9.6, 0.85, fill=True, facecolor="#fff", edgecolor="#ddd"))
        vals = [r["use_case"], r["value"], r["data_readiness"], r["complexity"], r["operational_risk"], r["priority_score"], r["decision"]]
        for x, v in zip(xs, vals):
            ax.text(x, y + 0.4, str(v), fontsize=9, color="#222", va="center")
    watermark(fig)
    save(fig, img / "01-scoring-board.png")

    # Bubble-ish scatter value vs risk
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    fig.patch.set_facecolor("#eef5f8")
    for r in rows:
        ax.scatter(r["operational_risk"], r["value"], s=180 + 40 * r["data_readiness"], c="#1a5f7a", alpha=0.85)
        ax.text(r["operational_risk"] + 0.08, r["value"] + 0.08, r["decision"], fontsize=8, color="#555")
    style_axes(ax, "Value vs operational risk (bubble size ≈ data readiness)")
    ax.set_xlabel("Operational risk (1–5)")
    ax.set_ylabel("Business value (1–5)")
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    watermark(fig)
    save(fig, img / "02-value-risk.png")

    # Decision mix
    mix = {}
    for r in rows:
        mix[r["decision"]] = mix.get(r["decision"], 0) + 1
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.bar(list(mix.keys()), list(mix.values()), color="#1a5f7a")
    style_axes(ax, "Decision mix across assessed ideas")
    ax.set_ylabel("Use cases")
    watermark(fig)
    save(fig, img / "03-decision-mix.png")

    # Overview
    fig = plt.figure(figsize=(10, 5.4))
    fig.patch.set_facecolor("#eef5f8")
    fig.text(0.06, 0.92, "Applied AI opportunity frame", fontsize=16, fontweight="bold")
    fig.text(0.06, 0.875, "Choose automation only where value, readiness and risk justify it", fontsize=9, color="#555")
    for i, (label, val) in enumerate(
        [
            ("Ideas scored", str(len(rows))),
            ("Pilot", str(mix.get("Pilot", 0))),
            ("Assess", str(mix.get("Assess", 0))),
            ("Hold", str(mix.get("Hold", 0))),
        ]
    ):
        ax = fig.add_axes([0.06 + i * 0.23, 0.48, 0.20, 0.28])
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#ddd")
        ax.set_facecolor("#fff")
        ax.text(0.08, 0.62, label.upper(), fontsize=8, color="#777", transform=ax.transAxes)
        ax.text(0.08, 0.22, val, fontsize=18, fontweight="bold", transform=ax.transAxes)
    axb = fig.add_axes([0.06, 0.12, 0.88, 0.28])
    names = [r["use_case"] for r in rows]
    scores = [r["priority_score"] for r in rows]
    axb.barh(names, scores, color="#1a5f7a")
    style_axes(axb, "Priority score by use case")
    watermark(fig)
    save(fig, img / "04-framework-overview.png")


# ---------------------------------------------------------------------------
# Fabric walkthrough stills (from finance synthetic if present)
# ---------------------------------------------------------------------------

def build_fabric():
    img = ROOT / "assets" / "img" / "work" / "fabric"
    data = ROOT / "assets" / "data" / "fabric-synthetic"
    fact = ROOT / "assets" / "data" / "finance-synthetic" / "fact_finance.csv"
    rows = []
    if fact.exists():
        with fact.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    lineage = [
        ("Landing", "ERP-style CSV / files", "Raw synthetic facts"),
        ("Lakehouse", "Bronze tables", "Append-only history"),
        ("Warehouse", "Curated dims + facts", "Star schema"),
        ("Semantic", "Finance measures", "P&L / variance"),
        ("Power BI", "Management views", "Consumer layer"),
    ]
    write_csv(
        data / "reference_lineage.csv",
        [
            {
                "stage_order": i,
                "stage": a,
                "component": b,
                "purpose": c,
                "dataset": "SYNTHETIC_PUBLIC_SAFE",
            }
            for i, (a, b, c) in enumerate(lineage, 1)
        ],
    )
    (data / "README.txt").write_text(
        "FABRIC FINANCE ANALYTICS REFERENCE PATH\n"
        "======================================\n"
        "Conceptual walkthrough only. No employer Fabric estate.\n"
        "Uses the public synthetic finance facts as the illustrative source.\n",
        encoding="utf-8",
    )

    fig, ax = plt.subplots(figsize=(10, 4.8))
    fig.patch.set_facecolor("#eef5f8")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.text(0.3, 3.5, "Fabric reference path — synthetic finance walkthrough", fontsize=13, fontweight="bold")
    for i, (stage, comp, purpose) in enumerate(lineage):
        x = 0.3 + i * 1.9
        ax.add_patch(plt.Rectangle((x, 1.2), 1.7, 1.8, fill=True, facecolor="#fff" if i < 4 else "#1a5f7a", edgecolor="#888"))
        tc = "#222" if i < 4 else "#f2f2f2"
        mc = "#555" if i < 4 else "#bdbdbd"
        ax.text(x + 0.85, 2.5, stage, ha="center", fontsize=10, fontweight="bold", color=tc)
        ax.text(x + 0.85, 2.1, comp, ha="center", fontsize=8, color=mc)
        ax.text(x + 0.85, 1.6, purpose, ha="center", fontsize=7, color=mc)
        if i < 4:
            ax.annotate("", xy=(x + 1.85, 2.1), xytext=(x + 1.7, 2.1), arrowprops=dict(arrowstyle="->", color="#888"))
    watermark(fig, "SYNTHETIC REFERENCE · NO EMPLOYER ESTATE")
    save(fig, img / "01-lineage-board.png")

    # Row counts by stage (illustrative)
    n = len(rows) if rows else 810
    stages = ["Landing", "Bronze", "Curated", "Semantic*", "Report views"]
    # semantic/report are conceptual
    counts = [n, n, n, 1, 4]
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig.patch.set_facecolor("#eef5f8")
    ax.bar(stages, counts, color="#1a5f7a")
    style_axes(ax, "Illustrative object counts along the path")
    ax.set_ylabel("Rows / objects")
    fig.text(0.12, 0.02, "*Semantic = model object; report views = published stills", fontsize=8, color="#666")
    watermark(fig, "SYNTHETIC REFERENCE · NO EMPLOYER ESTATE")
    save(fig, img / "02-object-counts.png")

    fig = plt.figure(figsize=(10, 5.4))
    fig.patch.set_facecolor("#eef5f8")
    fig.text(0.06, 0.92, "Fabric finance analytics path", fontsize=16, fontweight="bold")
    fig.text(0.06, 0.875, "Governed path from ERP-style sources to management reporting (synthetic)", fontsize=9, color="#555")
    for i, (label, val) in enumerate(
        [
            ("Source rows", f"{n:,}"),
            ("Stages", "5"),
            ("Entities", "3 OpCos"),
            ("Scenarios", "3"),
        ]
    ):
        ax = fig.add_axes([0.06 + i * 0.23, 0.48, 0.20, 0.28])
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#ddd")
        ax.set_facecolor("#fff")
        ax.text(0.08, 0.62, label.upper(), fontsize=8, color="#777", transform=ax.transAxes)
        ax.text(0.08, 0.22, val, fontsize=16, fontweight="bold", transform=ax.transAxes)
    axb = fig.add_axes([0.06, 0.12, 0.88, 0.28])
    axb.axis("off")
    axb.text(0.0, 0.7, "Governance notes (reference)", fontsize=11, fontweight="bold", color="#222")
    axb.text(0.0, 0.35, "Reusable definitions · lineage from landing to report · no ad-hoc extract as system of record", fontsize=9, color="#555")
    axb.text(0.0, 0.05, "This is a conceptual walkthrough, not a live Fabric workspace screenshot.", fontsize=8, color="#777")
    watermark(fig, "SYNTHETIC REFERENCE · NO EMPLOYER ESTATE")
    save(fig, img / "03-path-overview.png")
    print("fabric stills ready (SVG kept as static colored asset)")


# ---------------------------------------------------------------------------
# Phase E — short GIF from finance stills
# ---------------------------------------------------------------------------

def build_gif():
    try:
        from PIL import Image
    except ImportError:
        print("Pillow missing — installing via pip not attempted; skip GIF")
        return

    src_dir = ROOT / "assets" / "img" / "work" / "finance"
    frames_files = [
        src_dir / "04-report-overview.png",
        src_dir / "01-entity-variance.png",
        src_dir / "02-group-trend.png",
        src_dir / "03-pnl-bridge.png",
    ]
    frames = []
    target = (960, 540)
    for p in frames_files:
        if not p.exists():
            continue
        im = Image.open(p).convert("RGB")
        im.thumbnail(target, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", target, (244, 244, 244))
        canvas.paste(im, ((target[0] - im.width) // 2, (target[1] - im.height) // 2))
        frames.append(canvas)
    if len(frames) < 2:
        print("Not enough finance frames for GIF")
        return
    out = ROOT / "assets" / "img" / "work" / "finance" / "finance-demo.gif"
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=1400,
        loop=0,
        optimize=True,
    )
    print(f"wrote {out}")


def main():
    build_telecom()
    build_ai()
    build_fabric()
    build_gif()
    print("Remaining phase assets ready")


if __name__ == "__main__":
    main()
