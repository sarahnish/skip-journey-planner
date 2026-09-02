<p align="center">
  <img src="app/logo.png" alt="SKIP logo" width="180"/>
</p>

# SKIP — Intelligent Journey Recommendation System

An interpretable London Underground journey-planning system combining graph-based routing, human-labelled data, machine learning, and explainable scoring to recommend journeys based on Punctuality, Accessibility, and Comfort.

## My contributions 

- Originating the project concept
- Coordinating the team and project direction
- Building the passenger-facing **Streamlit application (`app.py`)**
- Supporting the **evaluation and interpretation of model results**
- Contributing to **final-stage coding and integration**
- Shaping the project framing, introduction, and related work
- Helping communicate the accessibility, explainability, and responsible-AI motivation

The project strengthened my interest in building AI systems where **predictive performance, explainability, uncertainty, and user impact** are considered together.

## Quick Links

<p align="center">
  <a href="https://github.com/sarahnish/portfolio">Project Portfolio</a> •
  <a href="notebooks/skip-modelling.ipynb">Modelling Notebook</a> •
  <a href="notebooks/evaluation-figures.ipynb">Evaluation Figures</a>
</p>

## At a Glance

| Network | Human-labelled routes | ML features | Final evaluation | Data sources |
|---|---:|---:|---:|---:|
| **272 stations · 313 edges** | **400** | **10** | **180 routes** | **7 streams** |

**Final architecture:** goal-specific machine-learning specialists rank candidate routes, while an interpretable PAC formula provides scores, explanations, and a recall-oriented safety layer.

---



## Overview

Traditional journey planners tend to optimise primarily for travel time. SKIP was designed to explore a more passenger-centred approach by allowing users to prioritise different journey needs.

Given an origin, destination, and passenger goal, SKIP:

1. Finds routes: Generates candidate paths across the London Underground network.
2. Scores & ranks: Evaluates accessibility, speed, and comfort using ML models tailored to your goal.
3. Recommends: Delivers ranked journey options complete with confidence scores and trade-offs.

PAC Goals - The system supports three journey goals:

- **Punctuality**
- **Accessibility**
- **Comfort**

## Key Features

- **Graph-based routing** across **272 London Underground stations** and **313 network edges**
- **12 interpretable route features** derived from accessibility, congestion, transfer, and operational signals
- **Goal-specific ML ranking** for Punctuality, Accessibility, and Comfort
- **7 TfL data sources** — 4 APIs and 3 official static datasets — with caching and persistent rate limiting
- **Safety-aware recommendation logic** — PAC formula recall safety net (`NET_FLOOR = 0.2`) and honesty flags for low-confidence recommendations
- **Reproducible modelling** — frozen TfL snapshot dated **2026-07-06**
- **Passenger-facing Streamlit prototype** with a colour-blind-friendly interface
- **Leakage-controlled evaluation** — 240/80/80 train-validation-test split, 5-fold cross-validation, model decisions made before final testing, and a separate 100-route external evaluation set

## Key Metrics

| Metric | Result |
|---|---:|
| London Underground stations | **272** |
| Network graph edges | **313** |
| Integrated data streams | **7** |
| Route-level ML features | **10** |
| Human-labelled development routes | **400** |
| Team annotators | **4** |
| Routes double-labelled for agreement checking | **40** |
| Additional final-test routes | **100** |
| Final pooled evaluation set | **180 routes** |
| TfL Journey Planner benchmark | **20 journeys** |
| Candidate routes generated per query | **Top 5** |
| Recommendations shown to users | **Top 3** |
| PAC formula agreement with human judgement | **66%** |
| PAC baseline final recall | **92%** |
| Per-goal mixture final accuracy | **73%** |

### External Benchmark

SKIP was benchmarked against the TfL Journey Planner across 20 representative journeys.

| Measure | SKIP | TfL Journey Planner | p-value |
|---|---:|---:|---:|
| Mean interchanges | **1.60** | **1.20** | **0.119** |
| Mean stops | **13.85** | **14.80** | **0.103** |

Neither difference was statistically significant, suggesting that SKIP produced structurally comparable routes while optimising for different passenger priorities.

## Models Evaluated

| Model | Role | Key Finding |
|---|---|---|
| **PAC Formula** | Deterministic baseline | **91.7% final classification recall**; fully interpretable scoring baseline |
| **Logistic Regression** | Linear benchmark | Selected specialist for the **Accessibility** goal |
| **Random Forest** | Non-linear model | Selected specialist for the **Punctuality** goal |
| **Gradient Boosting** | Boosted-tree model | Selected specialist for the **Comfort** goal during validation |
| **Neural Network (M1)** | Deep-learning experiment | PyTorch baseline investigated and ultimately dropped from the final configuration due to instability |
| **Per-goal Specialist Mixture** | **Final ranking approach** | Uses a specialist model for each PAC goal, with the PAC formula providing explanation and a recall safety layer |

## Tech Stack

| Layer | Technologies |
|---|---|
| **Language** | Python 3.12 |
| **Machine Learning** | scikit-learn |
| **Deep Learning** | PyTorch |
| **Data Processing** | pandas, NumPy |
| **Time Series** | statsmodels (SARIMA) |
| **Graph Processing** | NetworkX |
| **Frontend** | Streamlit |
| **Visualisation** | Matplotlib |
| **Data Integration** | TfL Open Data APIs |
| **Development** | Jupyter, Google Colab, Git, GitHub |

## System Workflow

```text
                                                TfL APIs + Static Data
                                                          ↓
                                                Data Cleaning & Integration
                                                          ↓
                                                Frozen Network Snapshot
                                                          ↓
                                                London Underground Graph
                                                          ↓
                                                Candidate Route Generation
                                                          ↓
                                                Route-Level Feature Engineering
                                                          ↓
                                                ┌─────────────────────┐
                                                │                     │
                                                ↓                     ↓
                                         PAC Formula           Goal-Specific ML
                                         Explanation              Ranking
                                                │                     │
                                                └─────────┬───────────┘
                                                          ↓
                                                Safety & Confidence Checks
                                                          ↓
                                               Ranked Top-3 Recommendations
                                                          ↓
                                                  Streamlit Interface
```
| APIs | TfL Open Data REST APIs |
| Development | Jupyter, Google Colab |
