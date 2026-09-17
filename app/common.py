import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from onset.pipeline import build_all


@st.cache_resource(show_spinner="Building the synthetic cohort with MNE (about 30 s, once)…")
def load():
    return build_all()


def banner():
    st.markdown(
        "<div style='background:#E1F5EE;color:#085041;padding:8px 14px;border-radius:8px;font-size:13px'>"
        "Decision support prototype on <b>synthetic data</b>. Every number cites a prediction and an evidence window. "
        "No recommendation exists in this product; the clinician decides.</div>",
        unsafe_allow_html=True,
    )
