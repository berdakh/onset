import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from app.common import banner, load

st.set_page_config(page_title="Onset", page_icon="🧠", layout="wide")
banner()
st.title("Onset")
st.subheader("A presurgical evaluation workbench for epilepsy surgery — prototype")
st.markdown("""
**What this is.** A working prototype of Onset built on a *synthetic* iEEG cohort generated with
[MNE-Python](https://mne.tools). Five virtual patients, 48 SEEG contacts each, with labeled seizure
onset zones, interictal spikes, high-frequency bursts, one seizure, and two bad contacts per patient.
Two baseline models rank contacts; a report cites its evidence; an assistant answers with evidence or refuses.

**What it is not.** Not a diagnostic device, not a new localization model, not real patient data.
Onset organizes evidence. The clinician decides. There is no recommendation anywhere in the product.

**How to read the pages (left sidebar):**
1. **Patient** — contact ranking from two models side by side, disagreement highlighted, evidence windows you can open.
2. **Report** — the structured, cited report; findings, disagreements, data quality, limitations.
3. **Assistant** — ask about a contact or the evidence; try asking what to resect.
4. **Models** — how the rankers are evaluated (leave-one-patient-out, precision@3, first-hit rank).
5. **Data** — how the synthetic cohort is made and why each ingredient is there.
6. **Architecture** — every component of the full system and which ones this prototype includes.
7. **Research** — the two MSc theses and where they plug in.
""")
pts, tables, runs, reports, metrics = load()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Synthetic patients", len(pts))
c2.metric("Contacts per patient", len(next(iter(pts.values())).ch_names))
c3.metric("Models", len(next(iter(runs.values()))))
c4.metric("Reports", len(reports))
st.info("Everything on these pages is computed live from the synthetic cohort when the app starts (about 30 s).")
