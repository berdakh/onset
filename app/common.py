import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from onset.pipeline import build_all


@st.cache_resource(show_spinner="Building the synthetic cohort with MNE (about 30 s, once)…")
def load():
    return build_all()


# --------------------------------------------------------------------------
# The standing disclaimer -- copied from the canonical text
# --------------------------------------------------------------------------
#
# DUPLICATION.md item 5, in berdakh/onset-hfo. The copy of record lives in
# that repository's app/panels.py; this is the copy. The structure is fixed
# and the *only* part that may differ is DATA_SENTENCE, because that app runs
# on public recordings of real patients and this one does not.
#
# If you edit anything but DATA_SENTENCE here, edit the twin in the same
# sitting. See onset-hfo/docs/DUPLICATION.md, which carries both wordings side
# by side so neither has to be reconstructed.

#: Fixed. Names the thing and refuses the category, in that order. This app
#: did not say "not a medical device" at all before the two were aligned.
DISCLAIMER_LEAD = "Research prototype — not a medical device."

#: The one line that legitimately differs between the two apps, and the more
#: important of the two to get right: a reader who mistakes this cohort for
#: patients has been misled about the only thing that matters here.
DATA_SENTENCE = ("A synthetic five-patient cohort, generated at startup — there "
                 "is no patient data here, and nothing here is validated for "
                 "clinical use.")

#: Fixed. The evidence rule, then the sentence that matters most: the product
#: contains no recommendation, as against containing one that is hedged.
DISCLAIMER_TAIL = ("Every number cites the window it came from. There is no "
                   "recommendation anywhere in this product; the clinician "
                   "decides.")


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
        # Green where Onset-HFO's is amber, and deliberately so: the colour is
        # not on the four-item "stays in step" list, and it is the fastest way
        # to tell at a glance which instrument you are looking at -- synthetic
        # here, real patient recordings there.
        "<div style='background:#E1F5EE;color:#085041;padding:8px 14px;border-radius:8px;font-size:13px'>"
        f"<b>{DISCLAIMER_LEAD}</b> {DATA_SENTENCE} {DISCLAIMER_TAIL}</div>",
        unsafe_allow_html=True,
    )
