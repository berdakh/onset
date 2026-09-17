import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import streamlit as st

from app.common import banner, load

st.set_page_config(page_title="Onset · Models", layout="wide")
banner()
pts, tables, runs, reports, metrics = load()
st.title("Models and evaluation")
st.markdown("""
Two deliberately plain rankers. The point of the platform is that any conformant model plugs in behind the
same contract; the theses replace these.

- **reference-linelength** — rank contacts by mean line length of interictal bipolar epochs. No learning. The floor every model must beat.
- **soz-gbt** — gradient-boosted trees on per-epoch features (line length, spike proxy, high-frequency ratio, six band powers),
  trained **leave-one-patient-out**: for each patient, train on the other four, score the held-out one. No patient is ever on both sides.

**Metrics a surgeon would accept**, per patient: *precision@3* (of the three top-ranked contacts, how many are truly in the SOZ)
and *first-hit rank* (how far down the list the first true SOZ contact appears).
""")
m = pd.DataFrame(metrics)
st.dataframe(m.pivot(index="pid", columns="model", values=["precision@3", "first_hit_rank"]), use_container_width=True)
st.dataframe(m.groupby("model")[["precision@3", "first_hit_rank"]].mean().round(2), use_container_width=True)
st.subheader("Feature table (first patient, first rows)")
st.dataframe(next(iter(tables.values())).head(12), use_container_width=True)
st.info("On real data the numbers will be worse and the story will be the same: honest folds, per-patient metrics, "
        "and a reference that is hard to beat by accident.")
