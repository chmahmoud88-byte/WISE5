"""
Analysis of the WISE5 blind pilot (cross-user consistency).
Usage:  python analyze_pilot.py analystA.xlsx analystB.xlsx
Compares the two analysts' inputs and scores with each other and with the authors' reference inputs.
Agreement of inputs is judged at the level of the scoring class (the normalised score of each input),
because two raw values in the same class give the same WISE5 score.
Needs: openpyxl, scipy.   Writes pilot_summary.md and pilot_details.csv.
"""
import sys, csv, itertools
import openpyxl
from scipy.stats import spearmanr, kendalltau

SOLV = {"Water":1.0,"Buffer":0.95,"Ethanol":0.9,"Isopropanol":0.8,"Ethyl acetate":0.8,"Acetone":0.8,"Methanol":0.7,
        "Acetonitrile":0.4,"Tetrahydrofuran (THF)":0.3,"Dichloromethane (DCM)":0.1,"Chloroform":0.1,"Toluene":0.1,"n-Hexane":0.1}
HAZ = {"None":1.0,"Water / Buffer":0.95,"Weak acid/base":0.9,"Acetic acid":0.85,"HCl / H2SO4":0.8,"H3PO4":0.75,"NaOH / KOH":0.7,
       "Ammonia":0.65,"Reducing agents":0.6,"H2O2":0.5,"Organic oxidants":0.45,"Metal catalysts":0.4,"Strong oxidizers":0.35,"Toxic reagents":0.3}
W = dict(op=.15,perf=.10,solv=.20,comp=.15,cons=.10,haz=.15,inst=.05,cx=.10)
# Reference inputs re-derived from the published papers (see reference_check_vs_papers.md); same as wise5_weight_sensitivity.py.
REF = {"[30]":(0.2,5,30,7.14,"Methanol",15,"UPLC",2,"H3PO4"),
       "[31]":(1.0,20,30,2.14,"Acetonitrile",40,"HPLC",7,"H3PO4"),
       "[32]":(1.3,6,25,4.26,"Acetonitrile",7,"HPLC",4,"H3PO4"),
       "[33]":(2.0,3.5,25,3.5,"Ethanol",10,"HPLC",1,"NaOH / KOH"),
       "[34]":(0.2,3,25,8.03,"Ethanol",52.93,"UPLC",2,"Strong oxidizers"),
       "[35]":(1.0,10,25,1.0,"Acetonitrile",50,"HPLC",1,"H3PO4"),
       "[36]":(0.8,20,30,3.15,"Acetonitrile",50,"HPLC",6,"H3PO4")}
METHODS = list(REF)
CLASS_NAMES = ["flow","time","temp","Rs","solvent","organic%","hazard","instrument","analytes"]

def classes(flow,time,temp,rs,solv,org,inst,n,haz):
    c = [1.0 if flow<=.3 else .8 if flow<=.6 else .6 if flow<=1 else .4,
         1.0 if time<=5 else .8 if time<=10 else .6 if time<=20 else .4,
         1.0 if temp<40 else .8 if temp<=60 else .6,
         1.0 if rs>=2 else .7,
         SOLV[solv],
         1.0 if org<=30 else .7 if org<=60 else .4,
         (float(haz.split(':')[1]) if str(haz).startswith('Custom:') else HAZ[haz]),
         1.0 if str(inst).upper()=="UPLC" else .7,
         1.0 if n<=5 else .6]
    return c
def score(inp):
    flow,time = inp[0],inp[1]
    c = classes(*inp)
    op = round((c[0]+c[1]+c[2])/3 + 1e-12, 2)
    cons = 1.0 if flow*time < 200 else .6
    return W["op"]*op+W["perf"]*c[3]+W["solv"]*c[4]+W["comp"]*c[5]+W["cons"]*cons+W["haz"]*c[6]+W["inst"]*c[7]+W["cx"]*c[8]
def label(s): return "Excellent" if s>=.8 else "Good" if s>=.6 else "Moderate" if s>=.4 else "Poor"

def load(path):
    ws = openpyxl.load_workbook(path, data_only=True)["Inputs"]
    out, shown, notes = {}, {}, {}
    for r in range(6,13):
        m = str(ws.cell(r,1).value).strip()
        v = [ws.cell(r,j).value for j in range(2,11)]
        if any(x is None for x in v): raise SystemExit(f"{path}: row {m} is incomplete")
        flow,time,temp,rs,solv,org,inst,n,haz = v
        out[m] = (float(flow),float(time),float(temp),float(rs),str(solv).strip(),float(org),str(inst).strip(),int(n),str(haz).strip())
        shown[m] = ws.cell(r,11).value
        notes[m] = " | ".join(str(ws.cell(r,j).value) for j in range(12,17) if ws.cell(r,j).value)
    return out, shown, notes, (ws["C3"].value if ws["C3"].value is not None else ws["B3"].value)

def main(a_path,b_path):
    raters = {"Ref": REF}
    info = {}
    for name,p in (("A",a_path),("B",b_path)):
        d,shown,notes,mins = load(p); raters[name] = d; info[name]=(shown,notes,mins)
    S = {k:{m:score(v[m]) for m in METHODS} for k,v in raters.items()}
    C = {k:{m:classes(*v[m]) for m in METHODS} for k,v in raters.items()}
    lines = ["# WISE5 blind pilot summary","",f"Analysts: A, B (time spent: A 180 min, B 110 min). Reference = authors' inputs.",""]
    # transcription check
    for k in ("A","B"):
        for m in METHODS:
            sh = info[k][0][m]
            if sh is not None and abs(float(sh)-S[k][m])>(0.0051 if len(str(float(sh)).split('.')[1])<=2 else 0.0006):
                lines.append(f"- CHECK {k} {m}: score recorded {sh} but inputs give {S[k][m]:.4f}")
    lines += ["","## Scores","","| Method | Ref | A | B | max-min |","|---|---|---|---|---|"]
    for m in METHODS:
        v=[S[k][m] for k in ("Ref","A","B")]
        lines.append(f"| {m} | {v[0]:.4f} | {v[1]:.4f} | {v[2]:.4f} | {max(v)-min(v):.4f} |")
    lines += ["","## Pairwise agreement","","| Pair | identical input classes (of 63) | mean abs score diff | max abs score diff | Spearman rho | Kendall tau | same greenness class |","|---|---|---|---|---|---|---|"]
    rows=[]
    for p,q in itertools.combinations(("Ref","A","B"),2):
        same = sum(C[p][m][i]==C[q][m][i] for m in METHODS for i in range(9))
        diffs = [abs(S[p][m]-S[q][m]) for m in METHODS]
        xs=[S[p][m] for m in METHODS]; ys=[S[q][m] for m in METHODS]
        rho = spearmanr(xs,ys)[0]; tau = kendalltau(xs,ys)[0]
        cls = sum(label(S[p][m])==label(S[q][m]) for m in METHODS)
        lines.append(f"| {p} vs {q} | {same} ({100*same/63:.0f}%) | {sum(diffs)/7:.4f} | {max(diffs):.4f} | {rho:.3f} | {tau:.3f} | {cls}/7 |")
        rows.append((p,q,same,sum(diffs)/7,max(diffs),rho,tau,cls))
    lines += ["","## Disagreements in input class (any pair)","","| Method | Input | Ref | A | B |","|---|---|---|---|---|"]
    detail=[]
    for m in METHODS:
        for i,nm in enumerate(CLASS_NAMES):
            v=[C[k][m][i] for k in ("Ref","A","B")]
            if len(set(v))>1:
                raw=[raters[k][m][[0,1,2,3,4,5,8,6,7][i]] for k in ("Ref","A","B")]
                lines.append(f"| {m} | {nm} | {raw[0]} | {raw[1]} | {raw[2]} |")
                detail.append([m,nm]+raw+v)
    lines += ["","## Analysts' notes",""]
    for k in ("A","B"):
        for m in METHODS:
            if info[k][1][m]: lines.append(f"- {k} {m}: {info[k][1][m]}")
    ab = rows[[ (r[0],r[1]) for r in rows].index(("A","B"))]
    lines += ["","## Suggested text (edit after reading the table above)","",
      f"A small blind pilot was run in which two analysts who did not develop the index entered the inputs of the seven methods [30]-[36] independently from the original papers, using only the README and the web tool. "
      f"The two analysts chose the same scoring class for {ab[2]} of 63 inputs ({100*ab[2]/63:.0f}%); the mean and maximum absolute differences in the WISE5 score were {ab[3]:.4f} and {ab[4]:.4f}, "
      f"the rank correlation between their scores was ρ = {ab[5]:.3f}, and they assigned the same greenness class to {ab[7]} of 7 methods. "
      f"The disagreements are listed in Table S11. With two analysts and seven methods this pilot indicates the size of the effect and does not establish general inter-user reliability."]
    open("pilot_summary.md","w",encoding="utf-8").write("\n".join(lines))
    with open("pilot_details.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["method","input","ref","A","B","class_ref","class_A","class_B"]); w.writerows(detail)
    print("\n".join(lines))
if __name__=="__main__":
    main(sys.argv[1],sys.argv[2])
