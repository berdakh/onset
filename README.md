# Onset — a presurgical evaluation workbench for epilepsy surgery

**Prototype on synthetic iEEG (MNE-Python).** Decision support, not diagnosis: reports show model ranks and the signal windows used as evidence; models' disagreements are reported, not averaged away;
there is no recommendation anywhere in the product. The clinician decides.

- **Python app (not yet hosted):** deploy this repo on [Streamlit Community Cloud](https://share.streamlit.io) — entry point `app/Home.py` (instructions below).
- **Project site + interactive mockup:** GitHub Pages serves `docs/` at `https://berdakh.github.io/onset/`.

## What is in the app
| Page | What you see |
|---|---|
| Patient | contact ranking from two models side by side, disagreement highlighted, evidence windows |
| Report | the structured cited report: findings, disagreements, data quality, limitations |
| Assistant | evidence-only Q&A; cites or refuses; try asking what to resect |
| Models | leave-one-patient-out evaluation: precision@3 and first-hit rank per patient |
| Data | how the synthetic cohort is generated with MNE and why each ingredient exists |
| Architecture | every component of the full system and which ones the prototype includes |
| Research | the lab, the gap, the two MSc theses and the principles they inherit |

## Run locally
```bash
git clone https://github.com/berdakh/onset && cd onset
python -m venv .venv && . .venv/bin/activate      # or: uv venv && . .venv/bin/activate
pip install -e ".[dev]"
streamlit run app/Home.py
```
First start builds and evaluates five synthetic patients and caches them. Startup time and memory use depend on the host.

The GitHub Pages website serves static HTML only. Its mockup uses fictional records and does not run the Python pipeline. The live Streamlit app needs a separate deployment from this same repository.

## Deploy the app free (Streamlit Community Cloud)
1. Push this repo to GitHub (public).
2. Go to share.streamlit.io → New app → pick the repo, branch `main`, main file `app/Home.py` → Deploy.
3. Put the resulting URL in `docs/index.html` (the "open the app" link) and in this README.

## Deploy the site (GitHub Pages)
Repository → Settings → Pages → Source: **GitHub Actions**. The `pages.yml` workflow publishes `docs/` on every push to `main`.

## Layout
```
onset/        synth.py (MNE cohort) · features.py · models.py · report.py · assistant.py · pipeline.py
app/          Home.py + pages/  (Streamlit)
docs/         project site and interactive mockup (GitHub Pages)
tests/        pytest
```

## Principles
1. No patient on both sides of a split.  2. Every score carries the window it looked at.
3. Disagreement is reported, not resolved.  4. No treatment recommendation exists in the schema.
5. Public or synthetic data first; real data only through de-identification.

Brain–Machine Interfaces Lab, Nazarbayev University · PI: Berdakh Abibullaev · MIT license.
