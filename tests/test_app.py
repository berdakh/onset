from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_all_pages_and_patient_interactions():
    root = Path(__file__).resolve().parents[1]
    pages = [root / "app/Home.py", *sorted((root / "app/pages").glob("[1-7]*.py"))]
    for page in pages:
        app = AppTest.from_file(str(page), default_timeout=120).run()
        assert not app.exception, (page.name, [e.message for e in app.exception])
        if page.name == "1_Patient.py":
            app.sidebar.selectbox[0].select("P05").run()
            app.sidebar.checkbox[0].check().run()
            assert not app.exception
        if page.name == "3_Assistant.py":
            app.chat_input[0].set_value("Patient 04 LA3").run()
            assert not app.exception
            assert "patient on screen" in app.session_state["chat"][-1][1]


# -- the four things that must stay in step with berdakh/onset-hfo ----------
#
# The twin of these tests lives in onset-hfo/tests/test_app.py. Nothing can
# enforce a convention across two repositories, but each side can enforce its
# own half, and a checklist the code already contradicts is worse than none.


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_the_disclaimer_is_assembled_from_the_canonical_constants():
    """No page may carry a second copy of the sentence that matters most."""
    from app.common import DATA_SENTENCE, DISCLAIMER_LEAD, DISCLAIMER_TAIL

    source = (_root() / "app" / "common.py").read_text()
    whole = f"{DISCLAIMER_LEAD} {DATA_SENTENCE} {DISCLAIMER_TAIL}"
    assert source.count(DISCLAIMER_LEAD) == 1, \
        "the banner restates the disclaimer instead of using DISCLAIMER_LEAD"
    assert "{DISCLAIMER_LEAD}" in source and "{DATA_SENTENCE}" in source
    assert "not a medical device" in whole
    assert "no recommendation anywhere in this product" in whole
    assert "the clinician decides" in whole


def test_this_apps_data_sentence_says_the_cohort_is_synthetic():
    """The one line that must NOT match the twin, and the reason it must not.

    A reader who mistakes this cohort for patients has been misled about the
    only thing that matters here, so the sentence has to say so in its own
    words rather than inherit the other app's.
    """
    from app.common import DATA_SENTENCE

    assert "synthetic" in DATA_SENTENCE
    assert "no patient data here" in DATA_SENTENCE
    assert "real surgical outcomes" not in DATA_SENTENCE, \
        "this app copied Onset-HFO's data sentence; it does not have that data"


def test_the_theme_file_names_its_twin():
    theme = _root() / ".streamlit" / "config.toml"
    assert "TWIN FILE" in theme.read_text()


def test_the_readme_carries_the_four_item_checklist():
    notes = (_root() / "README.md").read_text()
    assert "stay in step with" in notes
    for item in ("DATA_SENTENCE", ".streamlit/config.toml", "Architecture"):
        assert item in notes, f"the checklist does not name {item}"


def test_the_sidebar_opens_with_the_four_shared_destinations_in_order():
    source = (_root() / "app" / "common.py").read_text()
    names = ["Clinical guide", "Implementation walkthrough", "Results & docs",
             "Onset project"]
    positions = [source.index(f"[{name}]") for name in names]
    assert positions == sorted(positions), \
        "the shared link row is out of order; the two apps must match"


def test_the_shared_page_names_still_exist():
    """Checklist item 2. `Patient` and `Models` differ by design; these do not."""
    pages = {p.name.split("_", 1)[1].removesuffix(".py")
             for p in (_root() / "app" / "pages").glob("[1-9]_*.py")}
    assert {"Report", "Assistant", "Data", "Architecture", "Research"} <= pages


def test_each_kept_page_links_the_site_section_it_would_have_been_replaced_by():
    """DUPLICATION.md item 4, as revised after checking its premise.

    The plan said to retire `Data`, `Architecture` and `Research` in favour of
    links. Two of the three turned out not to be restatements -- the site
    *links to* the Data page rather than duplicating it -- so they link the
    matching site section instead of disappearing. This asserts the link is
    there, which is the part of the item that survived.
    """
    for page, anchor in (("5_Data", "#signal"), ("6_Architecture", "#system"),
                         ("7_Research", "#research")):
        source = (_root() / "app" / "pages" / f"{page}.py").read_text()
        assert f"berdakh.github.io/onset/{anchor}" in source, \
            f"{page} does not link the site section it draws on"
