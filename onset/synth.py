"""Synthetic SEEG patients built with MNE.

Each patient: 6 depth electrodes x 8 contacts (48 monopolar channels), 1/f background,
interictal spikes (much more frequent on SOZ contacts), high-frequency bursts on SOZ
contacts, and one seizure with low-voltage fast activity starting at the SOZ and spreading
to neighbours. Everything is labeled, so the models can be evaluated honestly.
"""

from dataclasses import dataclass, field

import mne
import numpy as np

ELECTRODES = ["LA", "LH", "LB", "RA", "RH", "RB"]
N_CONTACTS = 8
REGIONS = {"LA": "L amygdala", "LH": "L hippocampus", "LB": "L temporal pole",
           "RA": "R amygdala", "RH": "R hippocampus", "RB": "R temporal pole"}


@dataclass
class Patient:
    pid: str
    raw: mne.io.RawArray
    soz: set[str]
    bad: set[str]
    seizure: tuple[float, float]  # onset, offset seconds
    meta: dict = field(default_factory=dict)

    @property
    def ch_names(self) -> list[str]:
        return self.raw.ch_names


def _pink(n: int, rng: np.random.Generator) -> np.ndarray:
    white = rng.standard_normal(n)
    f = np.fft.rfftfreq(n)
    f[0] = f[1]
    spec = np.fft.rfft(white) / np.sqrt(f)
    x = np.fft.irfft(spec, n)
    return x / x.std()


def _spike(sfreq: float, rng: np.random.Generator) -> np.ndarray:
    n = int(0.07 * sfreq)
    t = np.linspace(-1, 1, n)
    return -np.exp(-(t * 3) ** 2) * (1 + 0.3 * rng.standard_normal()) * 6.0  # ~6x baseline


def make_patient(pid: str, seed: int, sfreq: float = 512.0, duration_s: float = 600.0,
                 n_soz: int = 3, seizure_at: float = 420.0) -> Patient:
    rng = np.random.default_rng(seed)
    names = [f"{e}{i}" for e in ELECTRODES for i in range(1, N_CONTACTS + 1)]
    n = int(sfreq * duration_s)
    data = np.zeros((len(names), n))
    # choose a contiguous SOZ on one electrode
    soz_elec = rng.choice(ELECTRODES[:3])
    start = int(rng.integers(1, N_CONTACTS - n_soz + 1))
    soz = {f"{soz_elec}{i}" for i in range(start, start + n_soz)}
    bad = set(rng.choice([c for c in names if c not in soz], size=2, replace=False))
    spike = _spike(sfreq, rng)
    for ci, ch in enumerate(names):
        x = _pink(n, rng) * 25.0  # microvolts
        rate_per_min = 30.0 if ch in soz else (4.0 if ch[:2] == soz_elec else 1.0)
        n_spikes = rng.poisson(rate_per_min * duration_s / 60)
        for pos in rng.integers(0, n - len(spike), size=n_spikes):
            x[pos:pos + len(spike)] += spike * 40.0
        if ch in soz:  # brief high-frequency bursts
            for pos in rng.integers(0, n - int(0.2 * sfreq), size=int(duration_s / 4)):
                tt = np.arange(int(0.2 * sfreq)) / sfreq
                x[pos:pos + len(tt)] += 12.0 * np.sin(2 * np.pi * 120 * tt) * np.hanning(len(tt))
            x += 4.0 * _pink(n, rng)  # a little extra broadband irritability
        if ch in bad:
            x = x * 0.02 + rng.standard_normal(n) * 400.0  # saturated / disconnected
        data[ci] = x
    # seizure: LVFA at SOZ from seizure_at, spreading to same-electrode neighbours after 3 s,
    # then to the same-side hippocampus after 8 s; 40 s long, amplitude ramps up
    on, off = seizure_at, seizure_at + 40.0
    t = np.arange(n) / sfreq
    for ci, ch in enumerate(names):
        if ch in bad:
            continue
        delay = None
        if ch in soz:
            delay = 0.0
        elif ch[:2] == soz_elec:
            delay = 3.0
        elif ch[0] == soz_elec[0] and ch[1] == "H":
            delay = 8.0
        if delay is None:
            continue
        m = (t >= on + delay) & (t < off)
        tt = t[m] - (on + delay)
        ramp = np.clip(tt / 6.0, 0, 1)
        lvfa = 15.0 * ramp * np.sin(2 * np.pi * (28 - 10 * ramp) * tt)  # fast, slowing, growing
        data[ci, m] += lvfa
    info = mne.create_info(names, sfreq, ch_types="seeg")
    raw = mne.io.RawArray(data * 1e-6, info, verbose="error")  # MNE stores volts
    raw.info["bads"] = sorted(bad)
    raw.set_annotations(mne.Annotations([on], [off - on], ["seizure"]))
    return Patient(pid, raw, soz, bad, (on, off),
                   meta={"seed": seed, "soz_electrode": soz_elec, "sfreq": sfreq})


def cohort(n: int = 5, seed: int = 100) -> list[Patient]:
    return [make_patient(f"P{i + 1:02d}", seed + i) for i in range(n)]
