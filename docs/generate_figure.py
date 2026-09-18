"""Run from the repository root: python docs/generate_figure.py."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from onset.synth import make_patient

p = make_patient("P01", seed=100)
x = p.raw.get_data(units="uV")
sf = p.raw.info["sfreq"]
soz = sorted(p.soz)[0]
normal = next(c for c in p.ch_names if c not in p.soz and c not in p.bad and c[:2] != soz[:2])
bad = sorted(p.bad)[0]
peak = int(np.argmax(np.abs(x[p.ch_names.index(soz), :int(380*sf)])))
start = min(max(peak-int(sf), 0), int(378*sf))
stop = start+int(2*sf)
t = np.arange(start, stop)/sf
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":12,"svg.fonttype":"none"})
fig, axes = plt.subplots(3,1,figsize=(10,7),sharex=True,layout="constrained")
fig.patch.set_facecolor("#ffffff")
for ax, ch, title, color in zip(axes,[normal,soz,bad],["Background contact", "Synthetic onset-zone contact", "Marked bad: added noise"],["#176678","#534ab7","#a35317"]):
 ax.plot(t,x[p.ch_names.index(ch),start:stop],color=color,lw=.8)
 ax.set_title(f"{ch} · {title}",loc="left",fontsize=13,fontweight="bold")
 ax.set_ylabel("µV")
 ax.grid(alpha=.15)
 ax.spines[['top','right']].set_visible(False)
axes[-1].set_xlabel("Recording time (seconds)")
fig.suptitle("Three traces from the actual synthetic generator",fontsize=17,fontweight="bold")
fig.savefig(Path(__file__).with_name("ieeg-example.svg"),metadata={"Date":None})
plt.close(fig)
print({"soz":sorted(p.soz),"bad":sorted(p.bad),"window":[start/sf,stop/sf]})
