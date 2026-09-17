import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from app.common import banner

st.set_page_config(page_title="Onset · Architecture", layout="wide")
banner()
st.title("Architecture: the full system and what this prototype includes")
st.graphviz_chart("""
digraph G { rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#F7F6F2", fontname="Helvetica", fontsize=11];
  ingest [label="Ingest\nBIDS iEEG (MNE)\nde-identification"]; db [label="Postgres + pgvector\nobject store"];
  feat [label="Features\nepochs · montage · version"]; models [label="Models\nregistry · contracts", fillcolor="#EEEDFE"];
  runs [label="Run service\n+ GPU worker"]; pred [label="Predictions + evidence\n(immutable)"];
  report [label="Report\nlocal LLM · validated", fillcolor="#E1F5EE"]; asst [label="Assistant\n4 read-only tools", fillcolor="#E1F5EE"];
  ui [label="Clinician UI"]; sec [label="Auth · audit · RLS", fillcolor="#FAEEDA"]; obs [label="Traces · metrics\nnightly chain", fillcolor="#FAEEDA"];
  ev [label="Evals · judge · budgets", fillcolor="#EEEDFE"];
  ingest -> db -> feat -> models -> runs -> pred; pred -> report -> ui; pred -> asst -> ui; ev -> report [style=dashed]; sec -> ui [style=dashed]; obs -> runs [style=dashed];
}
""")
st.markdown("""
| Component | Full system | This prototype |
|---|---|---|
| Data | BIDS ingest, de-identification, Postgres | synthetic MNE cohort in memory |
| Features | versioned Parquet, manifests | computed at start, same definitions |
| Models | registry (MLflow), `ModelContract`, thesis models | two baselines behind the same interface |
| Evaluation | LOPO, precision@k, calibration, model cards | LOPO, precision@3, first-hit rank |
| Predictions | immutable rows with evidence windows | in-memory, with evidence windows |
| Report | local Qwen writes; validator checks every citation; versioned | deterministic template, same schema, same rules |
| Assistant | local LLM over read-only, patient-scoped tools; cites or refuses | rule-based over the same evidence; cites or refuses |
| Security | roles, audit by middleware, row-level security, on-prem | not included (single user, no PHI) |
| Operations | containers, traces, budgets, nightly chain, incident drills | not included |
""")
st.caption("The prototype keeps every rule that matters to a clinician (cited evidence, disagreements stated, no recommendation) "
           "and leaves out everything that only matters once real data and real users exist.")
