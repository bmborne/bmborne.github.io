# Work page wireframe (design only)

**Status:** Phases locked — see `Docs/WORK_PHASES.md`  
**Done:** A, B1, C/D scaffolds · **Next:** B2 (Power BI screenshots)  
**Home:** v1.1 restrained CV · **Work:** evidence library with shared shell  
**Work categories:** Finance Analytics · Data Platforms · ERP & Business Applications · Applied AI · Engineering & Research · Writing  
**Date:** 9 August 2026  
**Depends on:** `BRAND_SOURCE_OF_TRUTH.md`, home CV one-pager  
**Goal:** Give UK recruiters proof in the claimed lanes without turning the home page into a project gallery.

---

## 1. Role of each page

| Page | Job | Recruiter question it answers |
|------|-----|-------------------------------|
| **Home** (`index.html`) | Identity, scope, experience, credentials | “Who is this and are they credible?” |
| **Work** (`work.html` — proposed) | Evidence gallery + featured case | “Can I see the skills in action?” |
| **Writing** (later / section on Work) | Judgment and learning narrative | “How do they think?” |

Home stays CV-like. Work is the visual proof layer.

**Home CTA (when Work ships):** one quiet text link under Selected work — e.g. `View work evidence →` — not a marketing hero.

---

## 2. URL and files (when approved)

```text
/
├── index.html                 (existing home)
├── work.html                  (new — gallery shell)
└── work/
    ├── finance-reporting.html     (case write-up — when ready)
    ├── erp-business-apps.html     (case write-up — when ready)
    └── telecom-anomaly.html       (case write-up — when ready)
```

Deep case pages can wait until the first artefact exists. **Phase 1 = `work.html` shell only.**

---

## 3. Desktop layout (wireframe)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│  Boniphace Mkindi          Data & Analytics Engineer          Home · Work │
├─────────────────┬────────────────────────────────────────────────────────┤
│                 │                                                        │
│  EVIDENCE       │  FEATURED                                              │
│                 │  ┌──────────────────────────────────────────────────┐  │
│  ○ Finance      │  │                                                  │  │
│  ● Data         │  │         [ large visual stage ]                   │  │
│  ○ ERP          │  │     screenshot / embed / GIF placeholder         │  │
│  ○ AI & eng.    │  │                                                  │  │
│  ○ Writing      │  └──────────────────────────────────────────────────┘  │
│                 │                                                        │
│                 │  Title of featured case                                │
│                 │  [Status chip]                                         │
│                 │                                                        │
│                 │  Problem (1–2 lines)                                   │
│                 │  My contribution (1–2 lines)                           │
│                 │  Stack (chips)                                         │
│                 │  Limitation / confidentiality note (1 line)            │
│                 │                                                        │
│                 │  [ Write-up ]  [ GitHub ]  [ Medium ]   ← only if real │
│                 │                                                        │
│                 │  ── More in this category ──                           │
│                 │  ┌────────┐ ┌────────┐ ┌────────┐                      │
│                 │  │ card 1 │ │ card 2 │ │ empty  │                      │
│                 │  └────────┘ └────────┘ └────────┘                      │
│                 │                                                        │
└─────────────────┴────────────────────────────────────────────────────────┘
│  Contact: email · LinkedIn · GitHub · Guildford   (same as home, once)   │
└──────────────────────────────────────────────────────────────────────────┘
```

**Proportions:** left rail ~28% · main stage ~72% (mirrors “sidebar secondary, narrative primary”).

**Visual language:** same grayscale system as home. Colour lives *inside* screenshots/embeds only.

**Mobile:** category chips in a horizontal row; featured stage full width; cards stack.

---

## 4. Left rail — categories

Exactly four proof lanes + Writing. No extra widgets.

| ID | Label | What belongs here |
|----|-------|-------------------|
| `finance` | Finance reporting | Power BI management reporting, P&L/variance/MTD/YTD, KPI definitions (synthetic or public-safe) |
| `data` | Microsoft data platform | Fabric / lakehouse / pipelines / semantic models — synthetic architecture and demos |
| `erp` | ERP & business apps | Business Central reporting, requirements, validation, adoption (public-safe) |
| `ai` | Applied AI & engineering | Anomaly detection, forecasting, AI opportunity frameworks, MSc engineering |
| `writing` | Writing | Medium / newsletter pieces tied to a finished mini-project |

Selecting a category updates the featured stage + “More in this category” cards (filter, not separate pages).

---

## 5. Featured stage — content contract

Every featured case must answer:

1. **Business context** (what decision or process)  
2. **Problem**  
3. **My contribution** (support / contribute / build — accurate verbs)  
4. **Artefact** (what they can see)  
5. **Limitation** (synthetic, public-safe, MSc, in progress)  
6. **Links** (only live URLs)

**Status chips (fixed vocabulary):**

- `Professional · public-safe`
- `Synthetic demo`
- `MSc research`
- `In progress`
- `Writing`

Never show a chip that implies completion you cannot defend.

---

## 6. Empty-state copy (per category)

Use these until a real artefact exists. Honest empty states beat fake dashboards.

### Finance reporting (default featured on launch)

**Featured title:** Multi-entity finance reporting (synthetic)  
**Chip:** `In progress`  
**Visual:** Grey stage with label *“Power BI screenshot placeholder — synthetic P&L / variance model”*  
**Problem:** Fragmented spreadsheet reporting makes P&L, variance and MTD/YTD hard to trust across entities.  
**My contribution:** Designing a public-safe synthetic model that mirrors group-reporting patterns without employer data.  
**Stack:** Power BI · DAX · star schema · management reporting  
**Limitation:** Demo not published yet. No live embed until the synthetic model is review-ready.  
**Actions:** none (or disabled “Coming soon”)  
**Empty card line:** First public finance demo in progress — synthetic multi-entity P&L and variance.

### Microsoft data platform

**Featured title:** Fabric finance analytics path (reference)  
**Chip:** `In progress`  
**Visual:** *“Architecture diagram placeholder — ERP → Fabric → semantic model → Power BI”*  
**Problem:** Ad-hoc extracts do not scale for governed group reporting.  
**My contribution:** Documenting a reference architecture and, later, a synthetic walkthrough.  
**Stack:** Microsoft Fabric · OneLake concepts · semantic models · Power BI  
**Limitation:** No employer Fabric estate will be shown. Diagrams and synthetic demos only.  
**Empty card line:** Reference architecture planned — synthetic data only.

### ERP & business apps

**Featured title:** ERP reporting & Business Central support  
**Chip:** `Professional · public-safe` (text-first until screenshots exist)  
**Visual:** *“Process / reporting touchpoints diagram placeholder”*  
**Problem:** ERP go-lives need clear reporting requirements, validation and adoption support.  
**My contribution:** Contributing data, reporting design, validation and stakeholder understanding — not leading full BC configuration.  
**Stack:** Dynamics 365 Business Central · reporting requirements · UAT support  
**Limitation:** No internal screens, mappings or client data.  
**Empty card line:** Public-safe write-up first; screenshots only if synthetic or approved.

### Applied AI & engineering

**Featured title:** Telecom operations anomaly detection  
**Chip:** `MSc research`  
**Visual:** *“Bronze / silver / gold flow diagram placeholder”*  
**Problem:** Operational telemetry needs safe extraction, anonymisation and testable detection workflows.  
**My contribution:** Safety-gated Python ETL/modelling patterns, layered data, tests and run controls.  
**Stack:** Python · data engineering · anomaly detection · privacy by design  
**Limitation:** Public GitHub link withheld until disclosure/governance are resolved.  
**Empty card line:** Engineering case page next; repository when cleared.

### Writing

**Featured title:** From project to article  
**Chip:** `Writing`  
**Visual:** none / simple typographic card  
**Copy:** Articles on Medium will follow finished mini-projects (e.g. FMVA concepts applied to a model, PL-300/DP-600 lessons tied to a demo) — not published ahead of artefacts.  
**Empty card line:** No posts linked yet. Build → screenshot on Work → then write.

---

## 7. Card grid rules

- Max **6** cards visible per category.  
- Prefer **1 featured + 0–2 cards** at launch over a wall of placeholders.  
- Card fields: thumbnail (or grey block), title, status chip, one-line outcome/intent.  
- No progress bars, no fake % impact, no “client logos.”

---

## 8. What we will not put on this page

- Employer financial values, internal architecture, credentials, access methods  
- Live Power BI embeds before the synthetic report is solid  
- Fabric GIFs of real discoverIE estates  
- Placeholder GitHub links to empty repos  
- Medium links to posts that do not exist yet  
- A second full CV repeating home content  

---

## 9. Build sequence (after wireframe approval)

| Phase | Deliverable | Recruiter value |
|-------|-------------|-----------------|
| **A** | `work.html` shell + categories + empty states + home link | Structure ready; honest “in progress” |
| **B** | First real Finance screenshots (synthetic P&L) | Highest UK market pull |
| **C** | ERP public-safe write-up page | Matches current role narrative |
| **D** | MSc anomaly page (+ GitHub when cleared) | Engineering credibility |
| **E** | Optional embed / short GIF for Finance or Data | “Skills in action” |
| **F** | Medium posts linked from the matching case | Thought leadership with proof |

---

## 10. Approval checklist

Please confirm or adjust:

1. **URL:** `work.html` at repo root — OK?  
2. **Default category on load:** Finance reporting — OK?  
3. **Left categories:** Finance / Data / ERP / AI / Writing — add/remove any?  
4. **Phase A now:** build the empty shell after approval — yes/no?  
5. **Home link wording:** `View work evidence →` — OK?

---

## 11. Decision summary

This design gives you a place to show Power BI, finance analysis, Fabric flows and engineering work **when artefacts exist**, without weakening the credible CV home page. Empty states stay honest so the page can ship before the demos are finished — which matches how strong UK candidates sequence proof: **structure → first synthetic finance demo → depth**.
