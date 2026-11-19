# RootTrap ML — Network Intrusion Detection & Threat Intelligence

**Machine learning research for network traffic classification, MITRE ATT&CK interpretation, threat scoring and attack-chain visualization.**

> **Repository scope:** This repository contains the **RootTrap ML research module**, not the full **RootRAP** Linux incident-response platform described in the academic project report. The RootRAP architecture below is provided as **project context**; its Linux agent, quarantine service, VM sandbox, API and web dashboard are **not supplied in this repository**. Do not interpret the conceptual diagrams as a fully integrated, executable pipeline.

## 1. Project Concept and Motivation

Security analysts need more than an isolated alert: they need to understand what happened, assess its severity, connect related events, and decide how to respond. The wider **RootRAP** academic project explores a defensive Linux workflow for identifying *rootkit-like* behavior, preserving evidence and supporting investigation without running real malicious rootkits.

**RootTrap ML** explores a complementary research problem: how machine learning can classify **network traffic** and help analysts interpret suspicious activity through threat labels, MITRE ATT&CK mappings, risk scores and event graphs. **Network intrusion classification is not the same as Linux rootkit detection**, and the ML module does not by itself detect kernel-level rootkits.

## 2. Objectives

- Explore the CICIDS2017 network intrusion dataset and prepare traffic features for classification.
- Experiment with **Random Forest** and **LSTM** models.
- Evaluate classification performance and class-level predictions.
- Associate predicted attack categories with **MITRE ATT&CK** metadata using a mapping file.
- Calculate interpretable threat scores from rule-based indicators.
- Experiment with directed graphs representing sequences of security events.
- Document limitations and provide reproducible research notebooks where their required inputs are available.

## 3. Broader RootRAP Architecture — Project Context

The accompanying RootRAP academic report describes a **defensive Linux incident-response platform** with the following conceptual architecture:

```text
Linux monitored environment
    |  suspicious system signals
    v
Detection agent -> structured alert
    |
    v
Quarantine + evidence manifest + SHA-256
    |
    v
Central backend / API
    |
    v
Isolated virtual-machine sandbox
    |  hash verification + controlled behavioral analysis
    v
Static / behavioral analysis + indicators
    |
    v
Risk assessment -> analyst-assisted remediation
    |
    v
Web dashboard + incident report
```

### Why virtual machines?

The broader RootRAP design uses isolated virtual machines for **controlled behavioral analysis**. A clean VM snapshot can be restored before a test, an approved benign artifact can be analyzed away from the monitored host, and results can be collected before returning the VM to a known state. This separation is intended to reduce risk and improve repeatability. The report's tests use **benign simulated rootkit-like artifacts**, not real rootkits.

### Roles of the components

| Component in the broader RootRAP design | Purpose |
|---|---|
| Monitored Linux host | Observe local system events and generate suspicious-activity alerts |
| Detection agent | Normalize observations into structured alerts |
| Quarantine and manifest | Preserve artifacts, metadata and SHA-256 integrity evidence |
| Central API/backend | Coordinate case data and analysis results |
| Isolated VM sandbox | Perform controlled behavioral analysis on approved artifacts |
| Dashboard | Present alerts, evidence, risk, remediation guidance and reports |

**Availability:** These RootRAP components are described in the academic report; their implementation is **not included** in this RootTrap ML ZIP.

## 4. RootTrap ML — Research Workflow

The actual code and notebooks in this repository investigate the following stages:

```text
CICIDS2017 network-flow data (external; not bundled)
                  |
                  v
       Exploration and label review
                  |
                  v
       Feature preparation / scaling
                  |
          +-------+-------+
          |               |
          v               v
     Random Forest       LSTM
          |               |
          +-------+-------+
                  |
                  v
     Evaluation and attack labels
                  |
          +-------+------------------+
          |                          |
          v                          v
  ATT&CK mapping + scoring     Event graph experiments
          |                          |
          +-------------+------------+
                        v
              Research outputs
```

**Important:** This is a research workflow spread across notebooks and helper scripts, **not** a single automated production pipeline. Some notebooks require local dataset files, and some helper scripts require mapping data absent from the archive.

### Stage A — Dataset exploration

The notebooks examine the **CICIDS2017** network traffic dataset and its labels. The original dataset is **not distributed** with this repository. The reported evaluation covers seven grouped classes: **Bots, Brute Force, DDoS, DoS, Normal Traffic, Port Scanning, and Web Attacks**.

### Stage B — Data preparation

Exploratory notebooks cover feature and label preparation. A saved scaler is included in `models/scaler.pkl`. Reproducing results requires consistent feature order, preprocessing and dataset splits. The repository does not include a finished standalone `src/preprocessing.py` pipeline.

### Stage C — Model experiments

- **Random Forest:** an ensemble tree classifier used for tabular traffic features. A serialized experimental model is available at `models/random_forest_model.pkl`.
- **LSTM:** a neural-network model explored in the notebooks. A saved experimental model is available at `models/lstm_model.h5`.

The notebooks contain training/evaluation research. The repository does **not** provide a production inference API or a real-time network sensor.

### Stage D — MITRE ATT&CK interpretation

`src/attck_mapper.py` defines `map_prediction_to_attck(...)`, which looks up an attack label and returns ATT&CK technique/tactic metadata, a confidence value and an alert level. It also contains simple feature-based sub-technique selection rules.

**Dependency:** The script reads `data/attck_extended_mapping.json` at import time. That file is **not included** in the supplied archive, so the helper will not run as-is until a compatible mapping file is provided. ATT&CK mapping is an **interpretation**, not proof of attacker technique or attribution.

### Stage E — Explainable threat scoring

`src/threat_scorer.py` combines a mapping-provided base criticality with simple feature modifiers (for example, high failed-login counts or traffic volume) and returns a score capped at 10, reasons and an alert level. This is a **rule-based scoring helper**, not an independently validated risk prediction model. It also requires the missing ATT&CK mapping JSON.

### Stage F — Attack-chain graph experiments

`src/kill_chain_reconstructor.py` builds a `networkx.DiGraph` from a supplied ordered list of events and exports nodes/edges to JSON. Each event is linked to the next event in the input list. **This does not establish causality or automatically reconstruct a real attack kill chain**. The script's example duration is illustrative rather than derived from timestamp differences.

## 5. Repository Contents

```text
roottrap-ml/
├── notebooks/
│   ├── 00_test_env.ipynb
│   ├── 01_explore_mitre.ipynb
│   ├── 02_data_exploration.ipynb
│   ├── 03_label_schema.ipynb
│   ├── 04_algo_research.ipynb
│   ├── 05_preprocessing.ipynb
│   ├── 06_random_forest.ipynb
│   ├── 07_lstm.ipynb
│   ├── 08_evaluation.ipynb
│   ├── 09_attck_mapper_extended.ipynb
│   ├── 10_threat_scoring.ipynb
│   ├── 11_kill_chain_dag.ipynb
│   └── 12_final_evaluation.ipynb
├── src/
│   ├── attck_mapper.py
│   ├── threat_scorer.py
│   └── kill_chain_reconstructor.py
├── models/
│   ├── random_forest_model.pkl
│   ├── lstm_model.h5
│   └── scaler.pkl
├── docs/
│   ├── evaluation_report.md
│   └── final_evaluation_report.md
├── requirements.txt
└── README.md
```

The original source archive also contained empty placeholder files for training, preprocessing and evaluation; these should not be mistaken for implemented standalone modules.

## 6. Technologies

| Area | Tools / concepts |
|---|---|
| Language and experimentation | Python, Jupyter notebooks |
| ML models | scikit-learn Random Forest, Keras/TensorFlow LSTM |
| Data work | Pandas, NumPy, feature scaling |
| Visualization / graphs | Matplotlib and NetworkX (as used in experiments) |
| Threat interpretation | MITRE ATT&CK mapping, heuristic risk scoring |
| Dataset | CICIDS2017 (external download) |
| Broader RootRAP context only | Linux, virtual machines, sandboxing, SHA-256 evidence, incident response |

## 7. Installation and Exploration

Use a **trusted local or isolated research environment**. Python 3.10+ is a reasonable starting point, but exact compatibility depends on the library versions used to create the saved models.

```bash
git clone https://github.com/YOUR_USERNAME/roottrap-ml.git
cd roottrap-ml
python -m venv .venv
```

Activate the environment:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and open Jupyter:

```bash
pip install -r requirements.txt
jupyter lab
```

Explore the notebooks in numeric order. Download CICIDS2017 separately from an authorized source and adjust local data paths where needed. The repository is **not guaranteed to run end-to-end without additional dataset and mapping files**.

**Model-file safety:** Python pickle (`.pkl`) files can execute code when loaded. Only load model artifacts you trust, preferably in an isolated environment. Do not treat these saved experimental models as production-ready.

## 8. Evaluation and Reported Results

The included `docs/final_evaluation_report.md` reports the following **Random Forest** metrics on a cleaned CICIDS2017 test set of **504,151 rows**, **52 features** and **seven classes**:

| Metric | Reported value |
|---|---:|
| Accuracy | 99.30% |
| Precision | 99.78% |
| Recall | 99.30% |
| F1-score | 99.51% |

These values are **reported in the project's documentation**, not independently reproduced or verified in this publication. Performance on an offline test split does not demonstrate effectiveness against live, novel or adversarial traffic. The README does not claim corresponding LSTM performance without a supported evaluation result.

## 9. Video Demo

A video demonstration is available to illustrate the academic project and its experimental workflow.



https://github.com/user-attachments/assets/1198955d-d536-4867-aaae-082d280dafe8



Replace `YOUR_VIDEO_LINK` with the actual video URL before publishing. The source ZIP did not contain a recording. If the video instead demonstrates the **broader RootRAP Linux platform**, rename the link accordingly and state explicitly that the demonstrated components are outside this ML-only repository.

## 10. Testing, Limitations and Next Steps

### Current limitations

- Dataset and ATT&CK mapping JSON are not bundled.
- Some notebooks use environment-specific data paths and require adaptation.
- No unified executable training or inference pipeline is included.
- No integrated Linux agent, VM sandbox, backend or dashboard is included in this repository.
- Threat scoring uses heuristic rules; attack-chain graphs connect events by input order.
- Results are research metrics, not deployment or production security guarantees.

### Potential improvements

- Add reproducible dataset preparation scripts and documented split strategy.
- Package and test the mapping JSON with a clear schema.
- Add unit tests for the ATT&CK mapper, scorer and graph utilities.
- Validate both models against realistic holdout and cross-dataset scenarios.
- Build a documented inference service if the research is integrated into a larger platform.
- Evaluate false positives, class imbalance, drift and adversarial robustness.

## 11. Responsible Use and Academic Context

This repository is for **defensive cybersecurity education and research**. It does not provide a real rootkit, an offensive toolkit, or a validated production intrusion-detection system. Experiments should use authorized data and controlled environments.

**RootRAP** was developed as a team academic project at **ENSA Marrakech, Université Cadi Ayyad**, during the **2025–2026** academic year. The accompanying report describes a broader Linux defensive platform; **RootTrap ML** is documented here only to the extent supported by the supplied source code.
