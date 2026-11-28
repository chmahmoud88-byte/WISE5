"""
+/-5 % input perturbation test (supports Table S10).
Run: python wise5_input_perturbation.py   (needs numpy; imports wise5_weight_sensitivity.py for the scoring rules)
For each of the seven methods the five numeric inputs (flow rate, run time, temperature, Rs, organic %) are changed by
-5 % and +5 %, singly and in all 32 combinations, and in 20,000 random combinations (each input multiplied by U(0.95, 1.05)).
"""
import itertools, json, os
import numpy as np
import wise5_weight_sensitivity as w

# flow, time, temp, Rs, solvent, organic %, instrument, analytes, hazard (same inputs as wise5_weight_sensitivity.py)
INP = {"[30]":(0.2,5,30,7.14,"MeOH",15,"UPLC",2,0.75), "[31]":(1.0,20,30,2.14,"ACN",40,"HPLC",7,0.75),
       "[32]":(1.3,6,25,4.26,"ACN",7,"HPLC",4,0.75),   "[33]":(2.0,3.5,25,3.5,"EtOH",10,"HPLC",1,0.70),
       "[34]":(0.2,3,25,8.03,"EtOH",52.93,"UPLC",2,0.35), "[35]":(1.0,10,25,1.0,"ACN",50,"HPLC",1,0.75),
       "[36]":(0.8,20,30,3.15,"ACN",50,"HPLC",6,0.65)}
NAMES = list(INP); INPUTS = ["flow rate","run time","temperature","Rs","organic %"]
def sc(m, f):
    a = INP[m]
    return float(np.dot(w.W0, w.build(a[0]*f[0], a[1]*f[1], a[2]*f[2], a[3]*f[3], a[4], a[5]*f[4], a[6], a[7], a[8])))
base = {m: sc(m, [1]*5) for m in NAMES}
base_rank = w.rank(np.round(np.array([base[m] for m in NAMES]), 9))
out = {"baseline": base, "methods": {}}
for m in NAMES:
    single, cross = [], set()
    for i in range(5):
        for f in (0.95, 1.05):
            ff = [1]*5; ff[i] = f; d = sc(m, ff) - base[m]; single.append(d)
            if abs(d) > 1e-9: cross.add(f"{INPUTS[i]} {'+' if f>1 else '-'}5 %")
    allc, changed = [], False
    for combo in itertools.product((0.95, 1.05), repeat=5):
        s_m = sc(m, combo); allc.append(s_m - base[m])
        scores = np.array([s_m if k == m else base[k] for k in NAMES])
        if not np.array_equal(w.rank(np.round(scores, 9)), base_rank): changed = True
    out["methods"][m] = {"largest_single_delta": max(single, key=abs), "delta_min": min(allc), "delta_max": max(allc),
                         "inputs_crossing_threshold": sorted(cross), "rank_order_changed": changed}
rng = np.random.default_rng(1)
n_draw = 20000; strict_reversal = 0; top_changed = 0; tie = [0, 0, 0]
pairs = [(i, j) for i in range(7) for j in range(7) if base[NAMES[i]] - base[NAMES[j]] > 1e-6]
for _ in range(n_draw):
    s = np.round(np.array([sc(m, rng.uniform(0.95, 1.05, 5)) for m in NAMES]), 9)
    strict_reversal += any(s[i] < s[j] - 1e-9 for i, j in pairs)
    top_changed += int(s.argmax() != 0)
    d = round(s[1] - s[6], 9); tie[0 if d == 0 else 1 if d > 0 else 2] += 1
out["random_5pct"] = {"draws": n_draw, "draws_with_reversal_of_methods_with_different_baseline_scores": strict_reversal,
                      "draws_where_top_method_changed": top_changed,
                      "tie_31_36_remains": tie[0], "31_above_36": tie[1], "36_above_31": tie[2]}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wise5_input_perturbation_results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
