# Onset — a presurgical evaluation workbench for epilepsy surgery

**Prototype on synthetic iEEG (MNE-Python).** Decision support, not diagnosis: reports show model ranks and the signal windows used as evidence; models' disagreements are reported, not averaged away;
there is no recommendation anywhere in the product. The clinician decides.

- **Live Python app:** [Open Onset](https://berdakh-onset.streamlit.app/) — hosted on Streamlit Community Cloud from `app/Home.py` with Python 3.12.
- **The same methods on real recordings:** [Onset-HFO](https://onsetnu.streamlit.app/) — public iEEG from twenty patients who went to surgery, with the [results and limitations published](https://berdakh.github.io/onset-hfo/) rather than summarised. Code: [berdakh/onset-hfo](https://github.com/berdakh/onset-hfo).
- **Project site + interactive mockup:** GitHub Pages serves `docs/` at `https://berdakh.github.io/onset/`.

- **Clinical guide:** [Inside presurgical evaluation](https://berdakh.github.io/onset/clinical-guide.html) — what the workup actually involves, for readers coming from outside the clinic.
- **Illustrated tutorial:** [From iEEG to evidence](https://berdakh.github.io/onset/tutorial.html) — implementation walkthrough, worked examples, and an optional [Qwen agent lab](https://berdakh.github.io/onset/tutorial.html#qwen).

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

The GitHub Pages website serves static HTML only. Its mockup uses fictional records and does not run the Python pipeline. The live Streamlit app is deployed separately from this same repository.

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

## Four things that must stay in step with `berdakh/onset-hfo`

There are two repositories under one project name: this one, the teaching
prototype on a synthetic cohort, and
[Onset-HFO](https://github.com/berdakh/onset-hfo), the instrument on public
recordings of real patients. `onset-hfo/docs/DUPLICATION.md` measures what is
actually shared and says what must **not** be merged — there is no shared
Python and deliberately never will be. Four things must match.
**Anything not on this list is allowed to differ.**

1. The **standing disclaimer**'s structure and its no-recommendation sentence.
   The copy of record is `onset-hfo/app/panels.py`'s `DISCLAIMER_LEAD` /
   `DATA_SENTENCE` / `DISCLAIMER_TAIL`; `app/common.py` here carries the copy.
   Only `DATA_SENTENCE` differs, because only one of the two runs on real
   recordings — and this one's is the more important to get right.
2. The **shared page names**: `Home`, `Report`, `Assistant`, `Data`,
   `Architecture`, `Research`.
3. The **sidebar link row** — same destinations, same names, same order:
   Clinical guide · Implementation walkthrough · Results & docs · Onset
   project. The two entries after those differ by design.
4. `.streamlit/config.toml`, which carries a `TWIN FILE` header saying so.

No mechanism can enforce this across two repositories, and a submodule or a
published package would cost more than four items are worth. The honest
control is that the list is short, written down in both places, and each item
carries a comment naming its twin. **If you change one of the four, change it
in the other repository in the same sitting.** `tests/test_app.py` enforces
the half that lives here.

## Principles
1. No patient on both sides of a split.  2. Every score carries the window it looked at.
3. Disagreement is reported, not resolved.  4. No treatment recommendation exists in the schema.
5. Public or synthetic data first; real data only through de-identification.

Brain–Machine Interfaces Lab, Nazarbayev University · PI: Berdakh Abibullaev · MIT license.
