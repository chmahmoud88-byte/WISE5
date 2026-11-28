"""Normalises the returned analyst sheets (units, fractions, case) without changing any choice. Logs every change."""
import re, sys, openpyxl, warnings, csv
warnings.filterwarnings("ignore")
HAZ_NAMES=["None","Water / Buffer","Weak acid/base","Acetic acid","HCl / H2SO4","H3PO4","NaOH / KOH","Ammonia","Reducing agents","H2O2","Organic oxidants","Metal catalysts","Strong oxidizers","Toxic reagents"]
SOLV_NAMES=["Water","Buffer","Ethanol","Isopropanol","Ethyl acetate","Acetone","Methanol","Acetonitrile","Tetrahydrofuran (THF)","Dichloromethane (DCM)","Chloroform","Toluene","n-Hexane"]
CUSTOM_HAZ={("A","[30]"):"Custom:0.20"}   # analyst A chose ethyl acetate and entered a custom score of 0.2 (see her/his note)
log=[]
def num(x):
    if isinstance(x,(int,float)): return float(x)
    m=re.search(r"-?\d+(?:\.\d+)?",str(x).replace("\xa0"," ").replace("−","-"))
    return float(m.group()) if m else None
def clean(src,code,dst):
    wb=openpyxl.load_workbook(src); ws=wb["Inputs"]
    for r in range(6,13):
        m=ws.cell(r,1).value
        for j in (2,3,4,5,7,9,11):
            old=ws.cell(r,j).value
            if isinstance(old,str) and old.strip().upper().startswith("N/A"): new=0.0
            else: new=num(old)
            if j==7 and new is not None and new<=1: new=round(new*100,4)
            if new is not None and old!=new:
                log.append([code,m,ws.cell(5,j).value,old,new]); ws.cell(r,j).value=new
        for j,names in ((6,SOLV_NAMES),(10,HAZ_NAMES)):
            old=ws.cell(r,j).value; new=old
            for n in names:
                if str(old).lower().startswith(n.lower()): new=n
            if j==10 and (code,m) in CUSTOM_HAZ: new=CUSTOM_HAZ[(code,m)]
            if new!=old: log.append([code,m,ws.cell(5,j).value,old,new]); ws.cell(r,j).value=new
    old=ws["C3"].value
    if old is not None: ws["C3"].value=num(old)
    wb.save(dst)
clean(sys.argv[1],"A","A_clean.xlsx"); clean(sys.argv[2],"B","B_clean.xlsx")
with open("cleaning_log.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["analyst","method","field","original","cleaned"]); w.writerows(log)
print(len(log),"normalisations logged")
