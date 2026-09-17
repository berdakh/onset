import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from app.common import banner, load
from onset.features import bipolar_data, bipolar_pairs
from onset.models import rank_of
from onset.synth import REGIONS

st.set_page_config(page_title="Onset · Patient", layout="wide")
banner()
pts, tables, runs, reports, metrics = load()
pid = st.sidebar.selectbox("Patient", list(pts))
p = pts[pid]
st.title(f"Patient {pid}")
st.caption(f"SEEG · {len(p.ch_names)} contacts · 10 min synthetic · seizure at {p.seizure[0]:.0f} s · bad: {', '.join(sorted(p.bad))}")

ranks = {name: rank_of(r.scores) for name, r in runs[pid].items()}
names = list(ranks)
rows = []
for c in runs[pid][names[0]].scores:
    rk = {n: ranks[n].get(c, None) for n in names}
    rows.append({"contact": c, "region": REGIONS[c[:2]], **{f"{n} rank": rk[n] for n in names},
                 "disagree": (max(v for v in rk.values() if v) - min(v for v in rk.values() if v)) >= 5,
                 "truth (hidden in a clinic)": "SOZ" if c in p.soz else ""})
df = pd.DataFrame(rows).sort_values(f"{names[-1]} rank")
k = st.sidebar.slider("Show top", 5, 46, 12)
show_truth = st.sidebar.checkbox("Reveal synthetic ground truth", value=False)
cols = [c for c in df.columns if show_truth or not c.startswith("truth")]


def style(row):
    return ["background-color:#FAEEDA" if row["disagree"] else "" for _ in row]


st.subheader("Contact ranking — evidence, not a recommendation")
st.dataframe(df[cols].head(k).style.apply(style, axis=1), use_container_width=True, hide_index=True)
st.caption("Amber rows: the models disagree by five ranks or more. Disagreement is a finding, not noise.")

st.subheader("Evidence window")
c = st.selectbox("Contact", df["contact"].head(k).tolist())
model = st.selectbox("Model", names, index=len(names) - 1)
ev = runs[pid][model].evidence.get(c, [])
if not ev:
    st.warning("No evidence window for this contact from this model.")
else:
    t0, t1 = st.selectbox("Window (s)", ev, format_func=lambda w: f"{w[0]:.0f}–{w[1]:.0f} s")
    pairs = bipolar_pairs(p.ch_names, p.bad)
    data = bipolar_data(p, pairs)
    sf = p.raw.info["sfreq"]
    fig, ax = plt.subplots(figsize=(10, 2.6))
    shown = [i for i, pr in enumerate(pairs) if c in (pr.a, pr.b)][:2]
    for i in shown:
        seg = data[i, int(t0 * sf): int(t1 * sf)]
        ax.plot([t0 + j / sf for j in range(len(seg))], seg, lw=0.6, label=pairs[i].name)
    ax.set_xlabel("s")
    ax.set_ylabel("µV")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title(f"{c} · {model} · window {t0:.0f}–{t1:.0f} s (bipolar)")
    st.pyplot(fig, clear_figure=True)
    st.caption("Windows are ordered by mean score across adjacent bipolar pairs for this contact. Contact ranks aggregate all eligible epochs.")
