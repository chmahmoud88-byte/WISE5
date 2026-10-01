# WISE5 – Weighted Integrated Sustainability Evaluation

## 🔬 Overview
WISE5 is a web-based sustainability assessment tool developed for chromatographic analytical methods.

The platform integrates environmental impact, analytical performance, operational efficiency, resource consumption, and method complexity into a unified weighted sustainability score.

WISE5 provides both numerical evaluation and circular visualization to support the development and optimization of greener chromatographic methods.

---

## 🚀 Features

- ✅ Weighted sustainability scoring model
- ✅ Circular sustainability visualization
- ✅ Real-time sustainability calculation
- ✅ Green analytical chemistry evaluation
- ✅ Comparative assessment capability
- ✅ Interactive web interface
- ✅ Chromatographic method sustainability ranking
- ✅ GHS/NFPA-informed solvent greenness scoring
- ✅ Reagent/additive-based hazard profile scoring
- ✅ Parameter-level evaluation breakdown table
- ✅ Export results as high-resolution PNG
- ✅ Export results as a one-page PDF report
- ✅ No installation required (runs directly in browser)

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

These nine measured inputs are normalized and combined into eight weighted sustainability categories (Operational Efficiency, Analytical Performance, Solvent Type, Composition, Consumption, Hazard Profile, Instrument Efficiency, Method Complexity) to compute the final WISE5 score.

---

## 🧴 Solvent Greenness Scoring

Solvent-specific scores (*P*₍solv₎) are informed by GHS hazard classification ([UN GHS, 11th revised edition](https://unece.org/transport/standards/transport/dangerous-goods/ghs-rev11-2025)) and NFPA 704 ratings ([NFPA 704, 2027 Edition](https://www.nfpa.org/codes-and-standards/nfpa-704-standard-development/704)), together with solvent-specific environmental and toxicological considerations (biodegradability, VOC status, persistence). Scores are not derived from a single fixed formula; they reflect an expert-informed relative ranking grounded in these sources.

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

---

## ☣️ Hazard Profile Scoring

Hazard Profile is scored per the dominant reagent/additive used in the method (mobile-phase modifiers, buffers, titrants, etc.), rather than from the primary solvent alone:

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

- Weighted sustainability score (0–1 scale)
- Circular sustainability chart
- Sustainability classification:
  - 🟢 Excellent
  - 🟡 Good
  - 🟠 Moderate
  - 🔴 Poor
- Individual parameter contribution analysis
- Visual method performance assessment
- Downloadable PNG chart and PDF summary report

---

## 📈 Scoring Model

WISE5 uses a weighted evaluation framework:

```text
WISE5 = Σ (Wi × Pi)
```

Where:

- Wi = sustainability category weight
- Pi = normalized category score (0–1)

### Category Weights

| Sustainability Category | Weight (Wi) |
|---|---|
| Operational Efficiency | 0.15 |
| Analytical Performance | 0.10 |
| Solvent Type | 0.20 |
| Composition | 0.15 |
| Consumption | 0.10 |
| Hazard Profile | 0.15 |
| Instrument Efficiency | 0.05 |
| Method Complexity | 0.10 |

Weighting factors were assigned by author judgment, informed by the relative emphasis placed on solvent- and hazard-related impact in established green analytical chemistry metrics (Eco-Scale, GAPI, AGREE), rather than derived through formal expert elicitation or a structured multicriteria decision method. Formal weight derivation is a direction for future development.

### Score Interpretation

| Score | Rating |
|---------|---------|
| ≥ 0.80 | Excellent |
| 0.60 – 0.79 | Good |
| 0.40 – 0.59 | Moderate |
| < 0.40 | Poor |

---

## 🌐 Live Tool

👉 https://chmahmoud88-byte.github.io/WISE5/

---

## 📦 DOI (Citable Version)

WISE5 is archived and assigned a DOI via Zenodo:

👉 https://doi.org/10.5281/zenodo.20803095

---

## 📖 Citation

If you use WISE5 in academic research, please cite:

```text
Mohamed MA, et al.

WISE5: A Multidimensional Analytical Parameter Integrated Tool
for Sustainability Evaluation of Chromatographic Techniques.
```

(Final publication details will be added after acceptance.)

---

## 📚 Scientific Background

WISE5 was developed to support:

- Green Analytical Chemistry (GAC)
- Sustainable chromatographic method development
- Environmental impact assessment
- Quantitative greenness evaluation
- Method optimization and comparison

---

## 👨‍🔬 Author

Mahmoud A. Mohamed

📧 ch.mahmoud88@gmail.com

📧 mmabdelfatah@hikma.com

---

## ✅ Project Status

- Online Tool Available
- Sustainability Framework Implemented
- Circular Visualization Active
- PNG & PDF Export Available
- Journal Manuscript Under Submission
