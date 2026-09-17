from onset import models
from onset.features import epoch_features
from onset.pipeline import build_all
from onset.synth import make_patient


def test_patient_shape():
    p = make_patient("T1", 1, duration_s=120.0, seizure_at=60.0)
    assert len(p.ch_names) == 48 and len(p.soz) == 3 and len(p.bad) == 2
    assert p.raw.get_data(units="uV").std() > 5


def test_features_label_and_no_seizure_epochs():
    p = make_patient("T1", 1, duration_s=180.0, seizure_at=100.0)
    df = epoch_features(p)
    assert df["label"].sum() > 0 and (df["t0"] < 60).any()
    assert not ((df["t0"] > 70) & (df["t0"] < 140)).any()


def test_reference_beats_chance():
    precs = []
    for seed in (2, 3, 4):
        p = make_patient(f"T{seed}", seed, duration_s=240.0, seizure_at=200.0)
        r = models.reference_ranker(epoch_features(p))
        precs.append(models.top_k_precision(r.scores, p.soz, 3))
    assert sum(precs) / len(precs) > 3 / 46  # chance level for 3 of 46 contacts


def test_pipeline_and_report():
    pts, tables, runs, reports, metrics = build_all(n=3, seed=5)
    rep = reports["P01"]
    assert rep.summary and not hasattr(rep, "recommendation")
    assert all(m["precision@3"] >= 0 for m in metrics)
