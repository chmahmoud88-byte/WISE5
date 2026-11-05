"""
WISE5 weight-sensitivity and rank-stability analysis (supports Tables S7-S9).
Reproduces the WISE5 scores of the seven published methods [30]-[36] from the
category scores (Tables 2-4, S3, S5) and then perturbs / removes weights.
Run:  python wise5_weight_sensitivity.py      (needs numpy, scipy)
Seed is fixed so results are reproducible.
"""
import json
import numpy as np
from scipy.stats import spearmanr, rankdata

CATS = ["Op", "Perf", "Solv", "Comp", "Cons", "Haz", "Inst", "Cx"]
W0 = np.array([0.15, 0.10, 0.20, 0.15, 0.10, 0.15, 0.05, 0.10])

# --- normalisation rules (Table 2) -------------------------------------------------
def p_flow(f):  return 1.0 if f <= 0.3 else 0.8 if f <= 0.6 else 0.6 if f <= 1.0 else 0.4
def p_time(t):  return 1.0 if t <= 5 else 0.8 if t <= 10 else 0.6 if t <= 20 else 0.4
def p_temp(T):  return 1.0 if T < 40 else 0.8 if T <= 60 else 0.6
def p_comp(o):  return 1.0 if o <= 30 else 0.7 if o <= 60 else 0.4
def p_cons(v):  return 1.0 if v < 200 else 0.6
def p_inst(i):  return 1.0 if i == "UPLC" else 0.7
def p_cx(n):    return 1.0 if n <= 5 else 0.6
def p_perf(rs): return 1.0 if rs >= 2.0 else 0.7
SOLV = {"MeOH": 0.70, "ACN": 0.40, "EtOH": 0.90}

def build(flow, time, temp, rs, solv, org, inst, n, haz):
    op = round((p_flow(flow) + p_time(time) + p_temp(temp)) / 3, 2)   # Op reported to 2 dp (Table S3: 0.93)
    return [op, p_perf(rs), SOLV[solv], p_comp(org), p_cons(flow * time), haz, p_inst(inst), p_cx(n)]

# Hazard scores of [31], [32], [34] are NOT stated in the manuscript: they were
# back-calculated from the reported totals (0.95, 0.45, 0.65). Replace with the
# authors' actual Table S5 values and rerun.
METHODS = {
    "[30]": build(0.2, 6, 30, 7.14, "MeOH", 15, "UPLC", 2, 0.50),
    "[31]": build(0.8, 20, 50, 10.79, "ACN", 50, "HPLC", 6, 0.95),
    "[32]": build(1.3, 8, 25, 15.5, "ACN", 7, "HPLC", 4, 0.45),
    "[33]": build(2.0, 5, 25, 3.5, "EtOH", 10, "HPLC", 1, 0.45),
    "[34]": build(0.2, 3, 25, 8.03, "EtOH", 47.07, "UPLC", 2, 0.65),
    # case studies: only the category values stated in the text are used
    "[35]": [0.80, 0.70, 0.40, 0.70, 1.0, 0.50, 0.70, 1.0],
    "[36]": [0.73, 1.00, 0.40, 0.70, 1.0, 0.35, 0.70, 0.6],
}
NAMES = list(METHODS)
P = np.array([METHODS[k] for k in NAMES])          # 7 x 8
AGREE = {"[30]": .84, "[31]": .71, "[32]": .75, "[33]": .81, "[34]": .89}
MOGAPI = {"[30]": .83, "[31]": .70, "[32]": .74, "[33]": .83, "[34]": .87}
IDX5 = [NAMES.index(k) for k in AGREE]

def score(w): return np.round(P @ w, 9)   # round so exact ties are treated as ties
def rank(s):  return rankdata(-s, method="min").astype(int)
BASE = score(W0); BR = rank(BASE)

def rho(a, b): return spearmanr(a, b)[0]
def summarise(ws):
    """ws: array of weight vectors (N x 8) -> stability statistics"""
    S = np.round(ws @ P.T, 9)                       # N x 7
    R = np.apply_along_axis(rank, 1, S)
    rho_b = np.array([rho(BASE, s) for s in S])
    Sr = np.round(S, 2)   # concordance with AGREE/MoGAPI uses 2-dp WISE5 scores, as in the manuscript
    rho_a = np.array([rho(Sr[i][IDX5], list(AGREE.values())) for i in range(len(S))])
    rho_m = np.array([rho(Sr[i][IDX5], list(MOGAPI.values())) for i in range(len(S))])
    pc = lambda a: (np.median(a), np.percentile(a, 5))
    return {
        "rho_base_median_p5": pc(rho_b), "rho_agree_median_p5": pc(rho_a), "rho_mogapi_median_p5": pc(rho_m),
        "top_is_34_pct": float(np.mean(S.argmax(1) == NAMES.index("[34]")) * 100),
        "keep_baseline_rank_pct": {k: float(np.mean(R[:, i] == BR[i]) * 100) for i, k in enumerate(NAMES)},
        "pair_30_33_swap_pct": float(np.mean(S[:, 0] < S[:, 3]) * 100),
    }

def renorm(w): return w / w.sum(axis=-1, keepdims=True)

if __name__ == "__main__":
    rng = np.random.default_rng(20261104)
    out = {"baseline": dict(zip(NAMES, np.round(BASE, 4))), "baseline_rank": dict(zip(NAMES, BR.tolist()))}

    # (1) deterministic scenarios (Table S7)
    def sc(name, w):
        w = np.array(w, float); w = w / w.sum(); s = score(w)
        return {"scenario": name, "rho_base": round(float(rho(BASE, s)), 3), "ranks": rank(s).tolist(),
                "top": "/".join(NAMES[i] for i in np.flatnonzero(np.isclose(s, s.max()))), "rho_agree": round(float(rho(np.round(s,2)[IDX5], list(AGREE.values()))), 3),
                "rho_mogapi": round(float(rho(np.round(s,2)[IDX5], list(MOGAPI.values()))), 3)}
    def drop(*cats):
        w = W0.copy()
        for c in cats: w[CATS.index(c)] = 0
        return w
    def half(*cats):
        w = W0.copy()
        for c in cats: w[CATS.index(c)] *= 0.5
        return w
    def dbl(c):
        w = W0.copy(); w[CATS.index(c)] *= 2; return w
    sc_list = [("Baseline", W0), ("Drop Consumption", drop("Cons")), ("Drop Operational Efficiency", drop("Op")),
        ("Drop Operational Efficiency + Consumption", drop("Op", "Cons")),
        ("Halve Operational Efficiency and Consumption", half("Op", "Cons")),
        ("Drop Composition", drop("Comp")), ("Drop Composition + Consumption", drop("Comp", "Cons")),
        ("Halve solvent block (Solvent Type, Composition, Consumption, Hazard)", half("Solv", "Comp", "Cons", "Haz")),
        ("Drop Solvent Type", drop("Solv")), ("Drop Hazard Profile", drop("Haz")),
        ("Drop Instrument Efficiency", drop("Inst")), ("Drop Analytical Performance", drop("Perf")),
        ("Drop Method Complexity", drop("Cx")), ("Double Method Complexity", dbl("Cx")),
        ("Equal weights (0.125 each)", np.ones(8))]
    out["S7"] = [sc(n, w) for n, w in sc_list]

    # (2) one-at-a-time +/-50 % (16 cases)
    oat = []
    for i in range(8):
        for f in (0.5, 1.5):
            w = W0.copy(); w[i] *= f; w /= w.sum(); oat.append((float(rho(BASE, score(w))), NAMES[int(score(w).argmax())]))
    out["OAT50"] = {"min_rho": min(o[0] for o in oat), "all_top_34": all(o[1] == "[34]" for o in oat)}

    # (3) random schemes (Table S8)
    N = 20000
    out["S8"] = {
        "+-20%": summarise(renorm(W0 * rng.uniform(0.8, 1.2, (N, 8)))),
        "+-50%": summarise(renorm(W0 * rng.uniform(0.5, 1.5, (N, 8)))),
        "uniform simplex": summarise(rng.dirichlet(np.ones(8), N)),
    }

    # (4) acetonitrile score check requested in R3.1: Psolv(ACN) 0.40 -> 0.55 and -> 0.70 (= methanol)
    ACN_IDX = [NAMES.index(k) for k in ("[31]", "[32]", "[35]", "[36]")]
    out["ACN_check"] = {}
    for val in (0.55, 0.70):
        P2 = P.copy(); P2[ACN_IDX, CATS.index("Solv")] = val
        s2 = np.round(P2 @ W0, 9)
        out["ACN_check"][str(val)] = {"scores": dict(zip(NAMES, np.round(s2, 4).tolist())),
            "ranks": rank(s2).tolist(), "rho_base": round(float(rho(BASE, s2)), 3)}
    json.dump(out, open("wise5_sensitivity_results.json", "w"), indent=1, default=lambda o: float(o))
    print(json.dumps(out, indent=1, default=lambda o: float(o)))
