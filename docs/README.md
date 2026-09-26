# Project website

GitHub Pages serves this directory. `index.html` introduces the prototype;
`mockup.html` illustrates a proposed interface; `clinical-guide.html` explains the
presurgical workup for readers coming from outside the clinic; `tutorial.html` is the
self-contained implementation walkthrough. The actual Python app runs separately on
Streamlit, and the real-data sibling project is at
<https://berdakh.github.io/onset-hfo/>.

`ieeg-example.svg` is generated from synthetic data with `generate_figure.py`.
Run it from an environment with the project dependencies installed.

The optional `examples/qwen_agent.py` teaching lab defaults to an offline scripted
model. Live Qwen inference needs a separately configured local server; it is not
part of the deployed app and has not been benchmarked here.
