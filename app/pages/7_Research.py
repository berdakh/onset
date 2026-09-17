import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from app.common import banner

st.set_page_config(page_title="Onset · Research", layout="wide")
banner()
st.title("Research programme")
st.markdown("""
**Lab.** Brain–Machine Interfaces Laboratory, School of Computing and Artificial Intelligence, Nazarbayev University.
PI: Berdakh Abibullaev. Focus: deep learning for EEG/iEEG signal processing, BCI, clinical translation for epilepsy.

**The gap Onset addresses.** The proposed research explores how localization models can be compared within a reproducible workflow.
Onset demonstrates that workflow on synthetic data: baseline models in, structured reports and evidence-scoped answers out.
Clinical integration and external validation remain future work.

**Two MSc theses (2026–27)**
- *ML for seizure-onset-zone localization from iEEG* — implements `ModelContract`: scores per contact plus evidence windows;
  evaluated leave-one-patient-out with the platform's harness; a model card with intended and non-intended use.
- *Agentic orchestration of the iEEG analysis pipeline with open-weight LLMs* — implements `PipelineStep`s and an orchestrator
  that composes them, with an LLM choosing which steps to run and never bypassing a contract; grounded reporting.

**Principles the students inherit**
1. No patient on both sides of a split; normalization fit on training patients only.
2. Every score comes with the window it looked at, or an empty evidence list and a note saying so.
3. Disagreement between methods is reported, not averaged away.
4. Nothing in the system recommends treatment; the clinician decides.
5. Public data first; partner-center data only through de-identification.

**Data.** OpenNeuro iEEG datasets (public, BIDS) for development; 15+ patients from a partner medical center to follow, de-identified.

**Contact.** For collaboration or to see the full system, contact the PI.
""")
