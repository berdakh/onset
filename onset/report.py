"""A structured, cited report built from rows, not from imagination.

The prototype uses a deterministic template so it runs with no GPU. The schema (findings with
prediction ids and evidence windows, disagreements stated not resolved, data quality,
limitations, and no recommendation field) is the same one the LLM fills in the full system.
"""

from dataclasses import dataclass, field

from onset.models import ContactScores, rank_of
from onset.synth import REGIONS, Patient


@dataclass
class Finding:
    contact: str
    region: str
    ranks: dict[str, int]
    evidence: list[tuple[float, float]]
    note: str


@dataclass
class Report:
    pid: str
    version: int
    summary: str
    findings: list[Finding]
    disagreements: list[Finding]
    data_quality: list[str]
    limitations: list[str] = field(default_factory=list)
    # no recommendation field, on purpose


def build(p: Patient, runs: dict[str, ContactScores], version: int = 1, k: int = 5, cohort_size: int = 5) -> Report:
    ranks = {name: rank_of(r.scores) for name, r in runs.items()}
    contacts = sorted(set().union(*(r.scores for r in runs.values())), key=lambda c: min(rk.get(c, 999) for rk in ranks.values()))
    findings, disagreements = [], []
    for c in contacts:
        rk = {m: ranks[m].get(c, 999) for m in ranks}
        ev = []
        for r in runs.values():
            ev += r.evidence.get(c, [])
        ev = sorted(set(ev))
        f = Finding(c, REGIONS[c[:2]], rk, ev,
                    "ranked " + ", ".join(f"{m}: {v}" for m, v in rk.items()) + f"; evidence in {len(ev)} windows")
        if max(rk.values()) - min(rk.values()) >= 5 and min(rk.values()) <= k:
            disagreements.append(f)
        elif max(rk.values()) <= k:
            findings.append(f)
    names = list(ranks)
    top_agree = [f.contact for f in findings if all(v <= k for v in f.ranks.values())]
    summary = (f"{len(names)} models ran on {p.pid}. Contacts ranked in the top {k} by every model: "
               + (", ".join(top_agree) if top_agree else "none")
               + f". Models disagree on {len(disagreements)} contact(s). "
               + f"{len(p.bad)} contacts were marked bad and excluded. "
               + "The report presents evidence; it contains no recommendation.")
    dq = [f"bad contacts excluded: {', '.join(sorted(p.bad))}", "units: microvolts (checked)",
          f"seizure annotated at {p.seizure[0]:.0f}-{p.seizure[1]:.0f} s; interictal epochs used for ranking"]
    lim = ["synthetic patient (prototype)", f"leave-one-patient-out on a {cohort_size}-patient cohort",
           "ranks are relative within this patient; no probabilities shown"]
    return Report(p.pid, version, summary, findings, disagreements, dq, lim)
