"""An evidence-only assistant for the prototype: rule-based, patient-scoped, cites or refuses.
The full system replaces the rules with a local LLM over the same four read-only tools."""

import re

from onset.models import ContactScores, rank_of
from onset.report import Report
from onset.synth import REGIONS

DIRECTIVE = re.compile(r"\b(resect\w*|remov\w*|ablat\w*|should we|recommend\w*|operat\w*|surg\w*)\b", re.IGNORECASE)


def answer(q: str, pid: str, runs: dict[str, ContactScores], report: Report) -> tuple[str, list[str], bool]:
    """Return (text, trace, refused)."""
    if DIRECTIVE.search(q):
        return ("I don't make treatment recommendations. The evidence shows where the models place "
                "onset activity and where they disagree; the decision is the clinical team's.",
                ["output filter: directive language in the question; no tool called"], True)
    m = re.search(r"\b([LR][AHB]\d)\b", q.upper())
    other = re.findall(r"\b(?:P|PATIENT\s+)(\d{1,2})\b", q.upper())
    if any(f"P{int(number):02d}" != pid for number in other):
        return ("I can only see the patient on screen. Open that patient to ask about their contacts.",
                [f"v_predictions returned 0 rows (patient scope = {pid})"], True)
    if m:
        c = m.group(1)
        lines = []
        for name, r in runs.items():
            rk = rank_of(r.scores).get(c)
            if rk:
                ev = r.evidence.get(c, [])
                lines.append(f"{name}: rank {rk}" + (f", evidence windows {', '.join(f'{a:.0f}-{b:.0f} s' for a, b in ev)}" if ev else ""))
        if not lines:
            return (f"{c} is not scored for this patient (marked bad or absent).", ["v_predictions: 0 rows"], True)
        return (f"{c} ({REGIONS[c[:2]]}): " + "; ".join(lines) + ".", ["tools: compare_models, v_evidence"], False)
    if re.search(r"strongest|top|best|highest|which contacts", q, re.IGNORECASE):
        top = report.findings[:3]
        if not top:
            return ("No contact is in the top ranks of every model; see the disagreements section.",
                    ["v_predictions, report.findings"], True)
        return ("Strongest onset evidence: " + "; ".join(f"{f.contact} ({f.region}, {f.note})" for f in top) + ".",
                ["tools: v_predictions, v_evidence"], False)
    if re.search(r"disagree", q, re.IGNORECASE):
        d = report.disagreements
        return (("Models disagree on: " + "; ".join(f"{f.contact} ({f.note})" for f in d) + ".") if d else
                "No top-ranked contact differs by five ranks or more.", ["report.disagreements"], False)
    if re.search(r"last|previous|month|earlier", q, re.IGNORECASE):
        return (f"This is report v{report.version} for {pid}; earlier versions would be listed here with their runs. "
                "In the prototype only one version exists.", ["v_reports"], False)
    return ("I could not find evidence in this patient's predictions or windows that answers that. "
            "Try a contact (e.g. LA3), 'which contacts have the strongest evidence', or 'where do the models disagree'.",
            ["v_predictions, v_evidence: 0 relevant rows"], True)
