# Work evidence phases (locked)

Last updated: 9 August 2026

**Principle:** Home establishes trust and positioning. Work proves capability. Do not redesign the global IA — fill evidence over time.

---

## Status overview

| Phase | Status | Deliverable |
|-------|--------|-------------|
| **A** | **Done** | `work.html` shell, shared site chrome, 6 categories, honest empty states, Home link |
| **B1** | **Done** | Finance flagship scaffold: case page + architecture SVG + Work featured panel |
| **B2** | **Done** | Synthetic finance dataset + labelled report stills + CSV downloads |
| **C** | **Done** | ERP / BC-style synthetic dataset + flow SVG + labelled stills |
| **D** | **Done** | Telecom MSc synthetic bronze/silver/gold stills + case (GitHub still withheld) |
| **E** | **Done** | Short finance demo GIF on Work + finance case (not a live Power BI embed) |
| **F** | **Done** | On-site writing notes tied to finished cases; no empty Medium URLs |
| **+** | **Done** | Data Platforms Fabric walkthrough + Applied AI assessment framework |

---

## Category map (frozen)

1. **Finance Analytics** — `work/finance-reporting.html`  
2. **Data Platforms** — `work/fabric-finance-path.html`  
3. **ERP & Business Applications** — `work/erp-business-apps.html`  
4. **Applied AI** — `work/ai-opportunity.html`  
5. **Engineering & Research** — `work/telecom-anomaly.html`  
6. **Writing** — `work/writing-notes.html` (+ LinkedIn newsletter)

---

## Done means (definition)

- **A–C:** as previously locked (shell, finance stills, ERP stills).  
- **D done:** visitor sees synthetic layered pipeline stills + CSVs; no fake GitHub link.  
- **E done:** short labelled GIF of finance stills; not employer screenshots; `.pbix` still optional.  
- **F done:** writing accompanies finished artefacts on-site; external Medium links only when posts exist.

---

## Explicit non-goals (still in force)

- Fake impact metrics  
- Employer dashboards or internal architecture  
- Empty GitHub links  
- Medium links to posts that do not exist  
- Redesigning Home into a project gallery  

---

## Optional polish (not phase blockers)

- Native Power BI `.pbix` export from finance/ERP CSVs  
- Public GitHub for telecom when disclosure is cleared  
- Medium posts that expand the on-site writing notes  
- Live Power BI embed only after a solid public report exists  

---

## Generators

- `scripts/build_finance_synthetic.py`  
- `scripts/build_erp_synthetic.py`  
- `scripts/build_remaining_phases.py` (telecom, AI, Fabric, finance GIF)
