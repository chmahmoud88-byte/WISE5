# Regenerates Table S1 / Figure 4 with the exact scoring rules of the WISE5 web tool (index.html)
import openpyxl
from openpyxl.styles import Font, Alignment
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

def wise5(flow=0.5, time=5.0, temp=30, rs=2.0, solv=0.90, org=30, inst=1.0, n=2, haz=1.0):
    fs = 1.0 if flow <= 0.3 else 0.8 if flow <= 0.6 else 0.6 if flow <= 1.0 else 0.4
    ts = 1.0 if time <= 5 else 0.8 if time <= 10 else 0.6 if time <= 20 else 0.4
    tp = 1.0 if temp < 40 else 0.8 if temp <= 60 else 0.6
    op = round((fs + ts + tp) / 3 + 1e-12, 2)
    perf = 1.0 if rs >= 2 else 0.7
    cons = 1.0 if flow * time < 200 else 0.6
    comp = 1.0 if org <= 30 else 0.7 if org <= 60 else 0.4
    cx = 1.0 if n <= 5 else 0.6
    return 0.15*op + 0.10*perf + 0.20*solv + 0.15*comp + 0.10*cons + 0.15*haz + 0.05*inst + 0.10*cx

BASE = wise5()
series = {
 "a": ("Organic solvent content (% v/v)", "org",  [10, 20, 30, 31, 40, 50, 60, 61, 70]),
 "b": ("Flow rate (mL/min)",              "flow", [0.2, 0.3, 0.31, 0.6, 0.61, 1.0, 1.01, 2.0]),
 "c": ("Run time (min)",                  "time", [3, 5, 5.1, 10, 10.1, 20, 20.1, 30]),
}
rows = {k: [(v, wise5(**{key: v})) for v in vals] for k, (lab, key, vals) in series.items()}

wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Table_S1"
ws["A1"] = "Table S1. Responsiveness of the WISE5 score to single inputs (web tool rules; one input varied, all others at the base case)."
ws["A1"].font = Font(bold=True)
ws["A2"] = ("Base case: ethanol-water mobile phase (Psolv = 0.90), 0.5 mL/min, 5 min, 30 °C, Rs = 2.0, 30%% organic, UPLC, 2 analytes, "
            "no hazardous reagent; WISE5 = %.4f. Scores change in steps at the thresholds of Table 2; no regression was fitted." % BASE)
r = 4
for k, (lab, key, vals) in series.items():
    ws.cell(r, 1, "(%s) %s" % (k, lab)).font = Font(bold=True)
    ws.cell(r, 2, "WISE5 score").font = Font(bold=True)
    ws.cell(r, 3, "Change from base case").font = Font(bold=True)
    r += 1
    for v, s in rows[k]:
        ws.cell(r, 1, v); ws.cell(r, 2, round(s, 4)); ws.cell(r, 3, round(s - BASE, 4)); r += 1
    r += 1
ws.column_dimensions["A"].width = 40; ws.column_dimensions["B"].width = 16; ws.column_dimensions["C"].width = 24
wb.save("Table_S1_Figure4_data.xlsx")

x, y = zip(*rows["a"])
fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
ax.step(x, y, where="post", color="#1b7f4b", lw=2)
ax.plot(x, y, "o", color="#1b7f4b")
for xi, yi in zip(x, y):
    ax.annotate("%.4f" % yi, (xi, yi), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7)
ax.set_xlabel("Organic solvent content (% v/v)"); ax.set_ylabel("WISE5 score")
ax.set_ylim(0.85, 1.0); ax.set_xlim(5, 75); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("Figure4_WISE5_vs_organic.png")
for k in rows:
    print(k, [(v, round(s, 4)) for v, s in rows[k]])
print("base", round(BASE, 4))
