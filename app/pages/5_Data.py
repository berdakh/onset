import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import matplotlib.pyplot as plt
import streamlit as st

from app.common import banner, load

st.set_page_config(page_title="Onset · Data", layout="wide")
banner()
pts, tables, runs, reports, metrics = load()
st.title("The synthetic cohort (MNE)")
st.markdown("""
Each virtual patient is an `mne.io.RawArray` with 48 SEEG channels (6 depth electrodes × 8 contacts), 512 Hz, 10 minutes:

| Ingredient | Why it is there |
|---|---|
| 1/f (pink) background | real iEEG is dominated by low frequencies; features must survive it |
| Interictal spikes, ~30/min on SOZ contacts, ~1/min elsewhere | the classic interictal biomarker |
| High-frequency bursts (120 Hz) on SOZ contacts | a stand-in for high-frequency oscillations |
| One seizure: low-voltage fast activity at the SOZ, spreading to neighbours after 3 s and to the hippocampus after 8 s | the ictal onset pattern; annotated, excluded from interictal ranking |
| Two bad contacts per patient (disconnected / saturated) | must be excluded and listed, never silently dropped |
| Labeled SOZ (three contiguous contacts on one electrode) | ground truth for honest evaluation |

Real data enters the full system through BIDS ingestion and de-identification; the same features and contracts apply.
""")
pid = st.selectbox("Patient", list(pts))
p = pts[pid]
sf = p.raw.info["sfreq"]
x = p.raw.get_data(units="uV")
t0 = st.slider("Start (s)", 0, 590, int(p.seizure[0]) - 5)
chs = st.multiselect("Channels", p.ch_names, default=sorted(p.soz) + [c for c in p.ch_names if c not in p.soz][:3])
fig, ax = plt.subplots(figsize=(11, 4))
for k, c in enumerate(chs):
    i = p.ch_names.index(c)
    seg = x[i, int(t0 * sf): int((t0 + 10) * sf)]
    ax.plot([t0 + j / sf for j in range(len(seg))], seg / 200 + k, lw=0.6)
ax.set_yticks(range(len(chs)))
ax.set_yticklabels(chs)
ax.set_xlabel("s")
ax.axvspan(p.seizure[0], p.seizure[1], color="#7F77DD", alpha=0.12)
st.pyplot(fig, clear_figure=True)
st.caption("Shaded: annotated seizure. Toggle the ground truth on the Patient page to compare with the rankings.")
