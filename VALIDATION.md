# Release validation — 17 September 2026

Validated locally with Python 3.13, Streamlit 1.45.1, MNE 1.13.2, NumPy 2.1.3 and scikit-learn 1.6.1.

- Ruff: passed.
- Pytest: 13 tests passed, including evidence ranking/duration, report completeness, and assistant refusal/scope regressions.
- Streamlit AppTest: Home and all seven pages passed with no app exceptions.
- Patient selection and ground-truth toggle passed; assistant cross-patient refusal passed.
- Static website: both entry points returned HTTP 200; mockup JavaScript parsed and its HTML-escaping and patient-scope checks passed in QuickJS.
- Default five-patient cohort: reference precision@3 = 0.3333; tree precision@3 = 0.8.
- First-hit ranks: reference [3, 3, 1, 2, 12]; tree [1, 1, 1, 1, 1].
- Cohort computation took approximately 32 seconds on the validation machine.

## Repairs

Evidence now selects the highest-scored contact windows across adjacent bipolar pairs and preserves actual epoch duration. Reports retain all qualifying disagreements and use the actual cohort size. Findings described as consensus require all models to rank the contact in the top five. Assistant patient references are checked throughout the question; refusal matching includes ablation/resection variants. Static mockup questions are HTML-escaped. Broken deployment links and unsupported production claims were clarified. Existing lint failures and CI package installation were corrected.

## Limits

This is a synthetic research demo, not a clinically validated system. The rule-based assistant is not an LLM or a security boundary. Reports contain in-memory ranks/windows, not immutable database prediction IDs. The static mockup uses fictional data and includes illustrative/inert controls. GitHub Pages cannot execute the Python app; deploy app/Home.py separately on a Python hosting service from this same repository. Memory and startup behavior on the hosting service still require live verification. The original uncited research-review statistic was removed pending a source. Partner-cohort plans are supplied project context, not independently verified facts.
