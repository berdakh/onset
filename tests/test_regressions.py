import pandas as pd
import pytest

from onset.assistant import answer
from onset.models import ContactScores, _evidence
from onset.report import Report, build
from onset.synth import Patient


def test_evidence_uses_highest_windows_and_actual_duration():
    df = pd.DataFrame([
        {"a": "LA1", "b": "LA2", "t0": t, "t1": t + 5, "score": score}
        for t, score in [(0, 1), (5, 10), (10, 2), (15, 9)]
    ])
    assert _evidence(df, "score", k=2)["LA1"] == [(5, 10), (15, 20)]


@pytest.mark.parametrize("question", ["Ablate LA3?", "Resection of LA3?", "Remove LA3?"])
def test_assistant_refuses_treatment(question):
    rep = Report("P01", 1, "", [], [], [])
    assert answer(question, "P01", {}, rep)[2]


@pytest.mark.parametrize("question", ["Patient 04 LA3", "P01 and P04 LA3", "P04 LA3"])
def test_assistant_checks_all_patient_references(question):
    rep = Report("P01", 1, "", [], [], [])
    result = answer(question, "P01", {}, rep)
    assert result[2] and "patient on screen" in result[0]


def test_report_includes_all_top_rank_disagreements():
    contacts = [f"LA{i}" for i in range(1, 9)] + [f"LH{i}" for i in range(1, 9)]
    orders = [contacts, contacts[8:] + contacts[:8]]
    runs = {
        str(i): ContactScores("P01", str(i), "1", {c: 16-j for j, c in enumerate(order)}, {})
        for i, order in enumerate(orders)
    }
    patient = Patient("P01", None, set(), set(), (420, 460))
    report = build(patient, runs, cohort_size=3)
    assert len(report.disagreements) == 10
    assert not report.findings
    assert "10 contact(s)" in report.summary
    assert "3-patient" in report.limitations[1]
