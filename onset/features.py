"""Bipolar montage, epoching, per-contact features. One recording at a time."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.signal import welch

from onset.synth import Patient

BANDS = {"delta": (1, 4), "theta": (4, 8), "alpha": (8, 13), "beta": (13, 30),
         "gamma": (30, 80), "hgamma": (80, 150)}


@dataclass
class Pair:
    name: str
    a: str
    b: str


def bipolar_pairs(names: list[str], bad: set[str]) -> list[Pair]:
    pairs = []
    for i, ch in enumerate(names[:-1]):
        nxt = names[i + 1]
        if ch[:2] == nxt[:2] and ch not in bad and nxt not in bad:
            pairs.append(Pair(f"{ch}-{nxt}", ch, nxt))
    return pairs


def bipolar_data(p: Patient, pairs: list[Pair]) -> np.ndarray:
    x = p.raw.get_data(units="uV")
    idx = {c: i for i, c in enumerate(p.ch_names)}
    return np.stack([x[idx[pr.a]] - x[idx[pr.b]] for pr in pairs])


def epoch_features(p: Patient, epoch_s: float = 10.0, interictal_only: bool = True) -> pd.DataFrame:
    """Return one row per (pair, epoch) with features; label = pair touches an SOZ contact."""
    sf = p.raw.info["sfreq"]
    pairs = bipolar_pairs(p.ch_names, p.bad)
    data = bipolar_data(p, pairs)
    step = int(epoch_s * sf)
    on, off = p.seizure
    rows = []
    for k, start in enumerate(range(0, data.shape[1] - step + 1, step)):
        t0 = start / sf
        if interictal_only and (t0 + epoch_s > on - 30 and t0 < off + 30):
            continue
        seg = data[:, start:start + step]
        f, pxx = welch(seg, sf, nperseg=int(sf))
        for j, pr in enumerate(pairs):
            x = seg[j]
            mad = np.median(np.abs(x - np.median(x))) + 1e-9
            row = {"pid": p.pid, "pair": pr.name, "a": pr.a, "b": pr.b, "epoch": k, "t0": t0, "t1": t0 + epoch_s,
                   "line_length": float(np.abs(np.diff(x)).sum() / len(x)),
                   "spike_rate": float((np.abs(x - np.median(x)) > 6 * mad).sum() / epoch_s),
                   "hfa_ratio": float(pxx[j, f >= 80].sum() / (pxx[j].sum() + 1e-12)),
                   "label": int(pr.a in p.soz or pr.b in p.soz)}
            for band, (lo, hi) in BANDS.items():
                m = (f >= lo) & (f < hi)
                row[f"bp_{band}"] = float(np.log(pxx[j, m].mean() + 1e-12))
            rows.append(row)
    return pd.DataFrame(rows)


FEATS = ["line_length", "spike_rate", "hfa_ratio"] + [f"bp_{b}" for b in BANDS]
