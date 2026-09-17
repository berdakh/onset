"""Two baseline rankers and honest evaluation (leave-one-patient-out)."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

from onset.features import FEATS


@dataclass
class ContactScores:
    pid: str
    model: str
    version: str
    scores: dict[str, float]  # contact -> score
    evidence: dict[str, list[tuple[float, float]]]  # contact -> windows (t0, t1)


def _pairs_to_contacts(df: pd.DataFrame, col: str) -> dict[str, float]:
    per_pair = df.groupby(["pair", "a", "b"])[col].mean().reset_index()
    out: dict[str, list[float]] = {}
    for _, r in per_pair.iterrows():
        out.setdefault(r["a"], []).append(r[col])
        out.setdefault(r["b"], []).append(r[col])
    return {c: float(np.mean(v)) for c, v in out.items()}


def _evidence(df: pd.DataFrame, col: str, k: int = 3) -> dict[str, list[tuple[float, float]]]:
    # Aggregate each contact/window just as contact scores aggregate adjacent pairs.
    expanded = pd.concat([
        df[["a", "t0", "t1", col]].rename(columns={"a": "contact"}),
        df[["b", "t0", "t1", col]].rename(columns={"b": "contact"}),
    ])
    windows = expanded.groupby(["contact", "t0", "t1"], as_index=False)[col].mean()
    windows = windows.sort_values([col, "t0"], ascending=[False, True])
    return {
        contact: [(float(r.t0), float(r.t1)) for r in group.head(k).itertuples()]
        for contact, group in windows.groupby("contact", sort=False)
    }


def reference_ranker(df: pd.DataFrame) -> ContactScores:
    """Rank contacts by mean line length. No learning; the floor every model must beat."""
    pid = df["pid"].iloc[0]
    return ContactScores(pid, "reference-linelength", "1", _pairs_to_contacts(df, "line_length"),
                         _evidence(df, "line_length"))


def train_tree(train: pd.DataFrame, seed: int = 7) -> GradientBoostingClassifier:
    pos = train["label"].sum()
    w = np.where(train["label"] == 1, (len(train) - pos) / max(pos, 1), 1.0)
    m = GradientBoostingClassifier(n_estimators=150, max_depth=3, learning_rate=0.05, random_state=seed)
    m.fit(train[FEATS], train["label"], sample_weight=w)
    return m


def tree_scores(model: GradientBoostingClassifier, df: pd.DataFrame) -> ContactScores:
    df = df.copy()
    df["score"] = model.predict_proba(df[FEATS])[:, 1]
    pid = df["pid"].iloc[0]
    return ContactScores(pid, "soz-gbt", "1", _pairs_to_contacts(df, "score"), _evidence(df, "score"))


def leave_one_patient_out(tables: dict[str, pd.DataFrame]) -> dict[str, ContactScores]:
    out = {}
    for pid, test in tables.items():
        train = pd.concat([t for q, t in tables.items() if q != pid])
        out[pid] = tree_scores(train_tree(train), test)
    return out


def top_k_precision(scores: dict[str, float], truth: set[str], k: int) -> float:
    ranked = sorted(scores, key=scores.get, reverse=True)[:k]
    return sum(c in truth for c in ranked) / k


def first_hit_rank(scores: dict[str, float], truth: set[str]) -> int:
    ranked = sorted(scores, key=scores.get, reverse=True)
    return next((i for i, c in enumerate(ranked, 1) if c in truth), len(ranked) + 1)


def rank_of(scores: dict[str, float]) -> dict[str, int]:
    return {c: i for i, c in enumerate(sorted(scores, key=scores.get, reverse=True), 1)}
