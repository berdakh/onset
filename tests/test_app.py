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
