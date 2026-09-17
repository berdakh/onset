"""Build the cohort once and cache it: patients, feature tables, runs, reports."""

from functools import lru_cache

from onset import models, report
from onset.features import epoch_features
from onset.synth import cohort


@lru_cache(maxsize=1)
def build_all(n: int = 5, seed: int = 100):
    if n < 2:
        raise ValueError("Leave-one-patient-out evaluation requires at least two patients")
    pts = cohort(n, seed)
    tables = {p.pid: epoch_features(p) for p in pts}
    tree = models.leave_one_patient_out(tables)
    runs = {p.pid: {"reference-linelength": models.reference_ranker(tables[p.pid]), "soz-gbt": tree[p.pid]}
            for p in pts}
    reports = {p.pid: report.build(p, runs[p.pid], cohort_size=n) for p in pts}
    metrics = []
    for p in pts:
        for name, r in runs[p.pid].items():
            metrics.append({"pid": p.pid, "model": name,
                            "precision@3": models.top_k_precision(r.scores, p.soz, 3),
                            "first_hit_rank": models.first_hit_rank(r.scores, p.soz)})
    return {p.pid: p for p in pts}, tables, runs, reports, metrics
