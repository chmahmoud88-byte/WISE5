# WISE5 Greenness Index Tool

## 🔬 Overview
WISE5 is a web-based greenness index tool developed for liquid chromatographic analytical methods.

The tool combines operational conditions, analytical performance, solvent and reagent hazard, resource consumption, and method complexity into a single weighted WISE5 score (0–1).

WISE5 is an operational and chemical greenness index. It is **not** a life-cycle sustainability assessment: direct energy use, sample preparation, total waste, solvent production/disposal and life-cycle impacts are not included.

WISE5 provides both a numerical evaluation and a circular visualization to support the development and comparison of greener chromatographic methods.

---

## 🚀 Features

- ✅ Weighted scoring model (WISE5 score, 0–1)
- ✅ Circular visualization of the eight scoring categories
- ✅ Real-time calculation
- ✅ Green analytical chemistry evaluation
- ✅ Comparative assessment of chromatographic methods
- ✅ Interactive web interface
- ✅ GHS/NFPA-informed solvent greenness scoring
- ✅ Reagent/additive-based hazard profile scoring
- ✅ Parameter-level evaluation breakdown table
- ✅ Export results as high-resolution PNG
- ✅ Export results as a one-page PDF report
- ✅ No installation required (runs directly in the browser)

---

## 🧪 Parameters Included

### Operational Parameters
- Flow rate
- Analysis time
- Temperature

### Analytical Performance
- Resolution (Rs)

### Solvent & Environmental Parameters
- Solvent type (scored per solvent — see **Solvent Greenness Scoring** below)
- Organic solvent percentage
- Solvent consumption (derived from flow rate × analysis time)
- Hazard profile (scored per reagent/additive — see **Hazard Profile Scoring** below)

### Method Characteristics
- Instrument type (HPLC / UPLC)
- Number of analytes

These ten parameters (nine inputs plus the derived solvent consumption) are normalized and combined into eight weighted scoring categories (Operational Efficiency, Analytical Performance, Solvent Type, Composition, Consumption, Hazard Profile, Instrument Efficiency, Method Complexity) to compute the final WISE5 score.

---

## 🧴 Solvent Greenness Scoring

Solvent-specific scores (*P*₍solv₎) are informed by GHS hazard classification ([UN GHS, 11th revised edition](https://unece.org/transport/standards/transport/dangerous-goods/ghs-rev11-2025)) and NFPA 704 ratings ([NFPA 704, 2027 Edition](https://www.nfpa.org/codes-and-standards/nfpa-704-standard-development/704)), together with solvent-specific environmental and toxicological considerations (biodegradability, VOC status, persistence). Scores are expert-assigned tier scores; they are not derived from a single fixed formula. The rules that define each tier are given in Table 4a of the manuscript.

| Solvent | Score |
|---|---|
| Water | 1.00 |
| Buffer | 0.95 |
| Ethanol | 0.90 |
| Isopropanol | 0.80 |
| Ethyl acetate | 0.80 |
| Acetone | 0.80 |
| Methanol | 0.70 |
| Acetonitrile | 0.40 |
| Tetrahydrofuran (THF) | 0.30 |
| Dichloromethane (DCM) | 0.10 |
| Chloroform | 0.10 |
| Toluene | 0.10 |
| n-Hexane | 0.10 |
| Custom | user-defined (0.00–1.00) |

The score of acetonitrile (0.40) below methanol (0.70) is a judgment about factors that the GHS category does not capture (VOC emissions, energy-intensive production, toxic combustion products). Users who weigh these factors differently can enter a custom value.

---

## ☣️ Hazard Profile Scoring

The hazard profile is scored once per method, using the single highest-hazard reagent or additive present (the one with the lowest score in the table below), for example buffers, acids, bases, oxidizers or titrants. Mobile-phase organic solvents are not scored here because they are scored under Solvent Type. Scores refer to the pure reagent; the concentration at which it is used is not considered. A reagent that is not listed can be entered as a custom value.

| Reagent / Additive | Score |
|---|---|
| None | 1.00 |
| Water / Buffer | 0.95 |
| Weak acid/base | 0.90 |
| Acetic acid | 0.85 |
| HCl / H₂SO₄ | 0.80 |
| H₃PO₄ | 0.75 |
| NaOH / KOH | 0.70 |
| Ammonia | 0.65 |
| Reducing agents | 0.60 |
| H₂O₂ | 0.50 |
| Organic oxidants | 0.45 |
| Metal catalysts | 0.40 |
| Strong oxidizers | 0.35 |
| Toxic reagents | 0.30 |
| Custom | user-defined (0.00–1.00) |

---
Figure caption
<img width="1090" height="765" alt="image" src="https://github.com/user-attachments/assets/06dcd164-b997-4cb3-921e-7fe4c0105b20" />

## 📊 Output

- WISE5 score (0–1 scale)
- Circular chart of the eight scoring categories
- Greenness class:
  - 🟢 Excellent
  - 🟡 Good
  - 🟠 Moderate
  - 🔴 Poor
- Individual parameter contribution analysis
- Downloadable PNG chart and PDF summary report

---

## 📈 Scoring Model

WISE5 uses a weighted evaluation framework:

```text
WISE5 = Σ (Wi × Pi)
```

Where:

- Wi = scoring category weight
- Pi = normalized category score (0–1)

### Category Weights

| Scoring Category | Weight (Wi) |
|---|---|
| Operational Efficiency | 0.15 |
| Analytical Performance | 0.10 |
| Solvent Type | 0.20 |
| Composition | 0.15 |
| Consumption | 0.10 |
| Hazard Profile | 0.15 |
| Instrument Efficiency | 0.05 |
| Method Complexity | 0.10 |

Weighting factors were assigned by author judgment, informed by the relative emphasis placed on solvent- and hazard-related impact in established green analytical chemistry metrics (Eco-Scale, GAPI, AGREE), rather than derived through formal expert elicitation or a structured multicriteria decision method. They have not been empirically calibrated. A weight-sensitivity and rank-stability analysis on seven published methods is reported in the manuscript (Section 3.10) and can be reproduced with `wise5_weight_sensitivity.py`.

### Score Interpretation

| Score | Greenness class |
|---------|---------|
| ≥ 0.80 | Excellent |
| 0.60 – 0.79 | Good |
| 0.40 – 0.59 | Moderate |
| < 0.40 | Poor |

The classes are proposed interpretive ranges for comparing methods. Agreement of WISE5 with other greenness tools (AGREE, MoGAPI, AMGS) shows consistency with those tools, not environmental accuracy.

---

## 🌐 Live Tool

👉 https://chmahmoud88-byte.github.io/WISE5/

---

## 💻 Code and Analysis Script

- `index.html` — the WISE5 web tool (all calculations run in the browser).
- `wise5_weight_sensitivity.py` — Python script for the weight-sensitivity and rank-stability analysis (requires numpy and scipy; fixed random seed).
- `wise5_sensitivity_results.json` — output of the script.

---

## 📦 DOI (Citable Version)

WISE5 is archived and assigned a DOI via Zenodo:

👉 https://doi.org/10.5281/zenodo.23974615

---

## 📖 Citation

If you use WISE5 in academic research, please cite:

```text
Mohamed MA, Alminderej FM, Binsaleh AY, Saleh SM, Nassar HF.

WISE5: A Multi-Parameter Operational and Chemical Greenness Index
for Liquid Chromatographic Methods.
```

(Final publication details will be added after acceptance.)

---

## 📚 Scientific Background

WISE5 was developed to support:

- Green Analytical Chemistry (GAC)
- Greener chromatographic method development
- Comparison of the operational and chemical greenness of methods
- Method optimization

---

## 👨‍🔬 Author

Mahmoud A. Mohamed

📧 ch.mahmoud88@gmail.com

📧 mmabdelfatah@hikma.com

---

## ✅ Project Status

- Online tool available
- Scoring framework implemented
- Circular visualization active
- PNG & PDF export available
- Journal manuscript under revision
