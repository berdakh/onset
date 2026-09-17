import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from app.common import banner, load

st.set_page_config(page_title="Onset · Report", layout="wide")
banner()
pts, tables, runs, reports, metrics = load()
pid = st.sidebar.selectbox("Patient", list(pts))
rep = reports[pid]
st.title(f"Onset Report — {pid} (v{rep.version})")
st.markdown(f"**Summary.** {rep.summary}")

st.subheader("Findings (top ranks with evidence)")
if rep.findings:
    st.table([{"contact": f.contact, "region": f.region, **{f"{m} rank": v for m, v in f.ranks.items()},
               "evidence windows (s)": ", ".join(f"{a:.0f}–{b:.0f}" for a, b in f.evidence)} for f in rep.findings])
else:
    st.write("No contact is top-ranked by every model.")

st.subheader("Disagreements — stated, not resolved")
if rep.disagreements:
    st.table([{"contact": f.contact, "region": f.region, **{f"{m} rank": v for m, v in f.ranks.items()},
               "evidence windows (s)": ", ".join(f"{a:.0f}–{b:.0f}" for a, b in f.evidence)} for f in rep.disagreements])
else:
    st.write("No top-ranked contact differs by five ranks or more.")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Data quality")
    for d in rep.data_quality:
        st.write("• " + d)
with c2:
    st.subheader("Limitations")
    for limitation in rep.limitations:
        st.write("• " + limitation)
st.success("There is no recommendation section. In the full system this report is written by a local language model "
           "and validated before storage: every cited prediction must exist, ranks must match the table, and directive "
           "language is rejected.")
