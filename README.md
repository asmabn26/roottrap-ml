# RootTrap ML — Network Threat Detection & MITRE ATT&CK Mapping

An academic machine-learning research module for network intrusion detection and threat interpretation. The repository explores traffic classification with **Random Forest** and **LSTM**, mapping predicted classes to **MITRE ATT&CK** concepts, assigning threat scores, and visualizing attack-chain relationships.

> **Scope clarification:** This repository contains the **ML research module** named RootTrap. It is **not the complete RootRAP Linux rootkit-response platform** described in the accompanying academic report. Several notebooks are exploratory, and some pipeline inputs are not included.

## Features

- Exploratory analysis and preprocessing of network traffic data
- Random Forest and LSTM model experimentation
- Model evaluation and confusion-matrix analysis
- ATT&CK mapping and explainable threat scoring utilities
- Kill-chain graph/reconstruction experiments
- Saved experimental model artifacts

## Reported results

The included `docs/final_evaluation_report.md` reports the following **Random Forest** metrics on a cleaned CICIDS2017 test split of 504,151 rows, 52 features and seven classes. These figures are reproduced from the project documentation, **not independently revalidated here**.

| Metric | Reported value |
| --- | ---: |
| Accuracy | 0.9930 |
| Precision | 0.9978 |
| Recall | 0.9930 |
| F1-score | 0.9951 |

Classes: Bots, Brute Force, DDoS, DoS, Normal Traffic, Port Scanning, Web Attacks.

## Repository structure

```text
roottrap-ml/
├── notebooks/             # Exploration, training and evaluation notebooks
├── src/                   # ATT&CK mapping, scoring and kill-chain helpers
├── models/                # Experimental serialized models and scaler
├── docs/                  # Evaluation notes
├── requirements.txt
└── README.md
```

## Getting started

Use Python 3.10+ in a **virtual environment**. Compatibility may vary across library versions.

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate    # Windows PowerShell
pip install -r requirements.txt
jupyter lab
```

Open the notebooks in numerical order, beginning with `notebooks/00_test_env.ipynb`. The original CICIDS2017 dataset is **not bundled**; obtain it from its authorized source and update notebook data paths as necessary. Some helper modules expect `data/attck_extended_mapping.json`, which is not included in the supplied archive; generate/provide it before invoking those modules. Empty source placeholders are not represented as implemented features.

**Model safety:** `models/*.pkl` are pickle-based files and must only be loaded in a trusted environment. Loading untrusted pickle files can execute arbitrary code. The provided models are experimental artifacts, not production-ready detection services.

## Demo

A video demonstration of the project is available. **Add the actual URL here before publishing:** `[Watch the demo](PASTE_YOUR_DEMO_URL_HERE)`.

If you prefer to host the video in this repository, place an appropriately sized recording under `demo/` and replace the link with its relative path. No demo recording was included in the supplied source ZIP.

## Responsible use and limitations

For academic research and defensive cybersecurity only. Classification quality depends on dataset preparation, train/test split, class imbalance, and deployment conditions. The reported metrics do not establish performance on live networks or novel attacks. MITRE mappings are interpretive aids, not definitive attribution.

## Academic context

Developed as a cybersecurity academic project. The associated RootRAP report discusses a broader Linux defensive incident-response platform; this repository documents only the supplied network-traffic ML component.
