import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from onset.pipeline import build_all


@st.cache_resource(show_spinner="Building the synthetic cohort with MNE (about 30 s, once)…")
def load():
    return build_all()


def banner():
    st.sidebar.markdown(
        # The first four entries are the shared link row: same names, same
        # order, in this app and in Onset-HFO's. See that repository's
        # docs/DUPLICATION.md. The last two necessarily differ -- they point
        # at the other instrument and at this repository's code.
        "[Clinical guide](https://berdakh.github.io/onset/clinical-guide.html) · "
        "[Implementation walkthrough](https://berdakh.github.io/onset/tutorial.html) · "
        "[Results & docs](https://berdakh.github.io/onset-hfo/) · "
        "[Onset project](https://berdakh.github.io/onset/) · "
        "[Onset-HFO app](https://onsetnu.streamlit.app/) · "
        "[Code](https://github.com/berdakh/onset)"
    )
    st.markdown(
        "<div style='background:#E1F5EE;color:#085041;padding:8px 14px;border-radius:8px;font-size:13px'>"
        "Decision support prototype on <b>synthetic data</b>. Every number cites a prediction and an evidence window. "
        "No recommendation exists in this product; the clinician decides.</div>",
        unsafe_allow_html=True,
    )
