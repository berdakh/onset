import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from app.common import banner, load
from onset.assistant import answer

st.set_page_config(page_title="Onset · Assistant", layout="wide")
banner()
pts, tables, runs, reports, metrics = load()
pid = st.sidebar.selectbox("Patient", list(pts))
st.title(f"Onset Assistant — {pid}")
st.caption("Evidence only · scope: this patient · in-memory evidence. In the prototype the assistant is rule-based; "
           "the full system uses a local open-weight model over the same tools.")

if "chat" not in st.session_state or st.session_state.get("chat_pid") != pid:
    st.session_state.chat = []
    st.session_state.chat_pid = pid
    for q in ["Which contacts have the strongest onset evidence?", "Where do the models disagree?",
              "Which contacts should we resect?"]:
        st.session_state.chat.append((q, *answer(q, pid, runs[pid], reports[pid])))

for q, a, trace, refused in st.session_state.chat:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        (st.warning if refused else st.write)(a)
        with st.expander("trace"):
            for t in trace:
                st.code(t)

q = st.chat_input("Ask about this patient's evidence (try a contact like LA3, or another patient id)")
if q:
    st.session_state.chat.append((q, *answer(q, pid, runs[pid], reports[pid])))
    st.rerun()
