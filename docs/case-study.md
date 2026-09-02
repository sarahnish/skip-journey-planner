# SKIP — Case Study

[← Back to Project Overview](../README.md)

## Executive Summary

SKIP is a London Underground journey-recommendation prototype built around three passenger priorities: **Punctuality, Accessibility and Comfort**.

It combines graph-based routing, human-labelled route suitability, machine learning and an interpretable PAC scoring framework.

The final design is hybrid:

> **Goal-specific ML models rank routes, while the PAC framework provides explanation and recall-oriented protection.**

---

## The Problem

Traditional journey planners largely optimise around efficiency and travel time.

For passengers with mobility requirements, however, the fastest route may still contain barriers such as:

- inaccessible stations
- lift disruption
- difficult interchanges
- crowding
- service disruption
- uncomfortable journey conditions

SKIP therefore asks:

> **Can journey recommendations reflect passenger-specific priorities while remaining transparent about why a route was selected?**

---

## System Design

```text
TfL Data
   ↓
London Underground Graph
   ↓
Candidate Routes
   ↓
Route-Level Features
   ↓
Goal-Specific ML Ranking
   ↓
PAC Explanation + Safety Layer
   ↓
Top 3 Recommendations
```

The Underground is represented as a graph containing **272 stations and 313 edges**.

For each origin-destination pair, SKIP generates up to **5 candidate routes** using k-shortest simple paths before ranking them according to the selected passenger goal.

---

## Data & Features

SKIP integrates **7 TfL API and static data streams** covering:

- network structure
- service disruption
- accessibility
- lift availability
- platform gaps
- crowding
- carriage temperature

The final supervised-learning dataset uses **10 route-level ML features**.

Examples include:

`num_interchanges` · `any_closure` · `min_step_free` · `mean_accessibility` · `any_lift_issue` · `max_gap_mm` · `mean_crowding_peak` · `route_temp`

A frozen TfL snapshot from **6 July 2026** was used during modelling so that route features and human labels described the same network state.

---

## Human-in-the-Loop Learning

The development dataset contained **400 human-labelled routes** rated by **4 annotators**.

Routes were scored on a 1–5 suitability scale and converted into binary:

**Suitable / Not Suitable**

labels for supervised learning.

The deterministic PAC formula achieved approximately **66% agreement with human judgement**.

This was important: the rules captured meaningful structure, but did not completely reproduce how people judged route suitability.

That gap motivated the predictive ML layer.

---

## Models & Evaluation

The project evaluated:

- **PAC Formula** — deterministic baseline
- **Logistic Regression**
- **Random Forest**
- **Gradient Boosting**
- **PyTorch Neural Network**
- **Per-goal Specialist Mixture**

The 400 development routes were split into:

```text
240 training
80 validation
80 held-out test
```

Model selection and tuning were performed using validation data.

A further **100 newly labelled routes** were used for external evaluation, giving a final pooled test set of:

**80 held-out + 100 external = 180 routes**

---

# Key Findings

## 1. Different Passenger Goals Needed Different Models

<p align="center">
  <img src="../results/goal-specialist-f1.png" alt="Goal-oriented validation F1 by model" width="800"/>
</p>

| Passenger Goal | Selected Specialist |
|---|---|
| **Punctuality** | Random Forest |
| **Accessibility** | Logistic Regression |
| **Comfort** | Gradient Boosting |

Different PAC goals produced different modelling behaviour.

**Takeaway:** one universal classifier did not perform best across every passenger priority, supporting a **per-goal specialist architecture**.

---

## 2. Machine Learning Did Not Replace the Interpretable Baseline

<p align="center">
  <img src="../results/final-model-tradeoff.png" alt="Final model trade-off" width="800"/>
</p>

On the pooled **180-route final evaluation**:

| Approach | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| **PAC Formula** | 0.69 | 0.52 | **0.92** | **0.66** |
| **Per-goal Mixture** | **0.73** | **0.58** | 0.73 | 0.65 |
| **Random Forest** | 0.69 | 0.52 | 0.78 | 0.63 |

The learned specialist mixture achieved the strongest **accuracy and precision**, while the PAC formula retained the strongest **recall**.

**Takeaway:** the evidence supported combining ML and deterministic reasoning rather than treating them as competing approaches.

---

## 3. Validation Improvements Did Not Fully Generalise

<p align="center">
  <img src="../results/tuning-vs-final.png" alt="Accuracy across tuning and final evaluation" width="800"/>
</p>

The per-goal mixture achieved:

**0.775 validation accuracy**

but:

**0.733 final pooled accuracy**

The drop on untouched data reinforced the importance of separating model selection from final evaluation.

**Takeaway:** validation performance alone was not sufficient evidence for choosing the final system.

---

## Final Hybrid Architecture

The results led to the following serving design:

```text
Candidate Routes
      ↓
Goal-Specific ML Specialist
      ↓
Probability-Based Ranking
      ↓
PAC Formula
      ↓
Explanation + Recall Protection
      ↓
Confidence / Honesty Flags
      ↓
Top 3 Recommendations
```

> **ML ranks. PAC explains. The safety layer protects.**

The specialist model determines route ordering, while the PAC framework provides interpretable scores, feature-level explanations and a recall-oriented safeguard.

---

## External Benchmark

SKIP was compared with the TfL Journey Planner across **20 representative journeys**.

| Measure | SKIP | TfL | p-value |
|---|---:|---:|---:|
| Mean interchanges | **1.60** | **1.20** | 0.119 |
| Mean stops | **13.85** | **14.80** | 0.103 |

Neither difference was statistically significant.

The benchmark therefore did not show that SKIP consistently produced shorter journeys.

Instead, it suggested that SKIP could generate structurally comparable routes while optimising for a different objective:

> **passenger-specific suitability rather than travel time alone.**

---

## Safety & Explainability

SKIP does not treat model predictions as guarantees.

The final recommendation layer combines:

- specialist-model confidence
- interpretable PAC scores
- feature-level explanations
- low-confidence warnings
- compromise flags
- a recall safeguard

The serving logic uses:

```python
NET_FLOOR = 0.2
```

This provides an additional safeguard for potentially viable routes while still communicating uncertainty to the passenger.

---

## Prototype

<p align="center">
  <img src="../screenshots/route-results.png" alt="SKIP ranked route recommendations" width="800"/>
</p>

The Streamlit prototype demonstrates:

- origin and destination selection
- PAC goal selection
- ranked route recommendations
- model confidence
- PAC scores
- accessibility indicators
- route trade-offs
- low-confidence compromise handling

[Run the prototype →](../app/README.md)

---

## Limitations

SKIP is an academic prototype and has several important limitations:

- relatively small labelled dataset
- smaller samples within individual PAC goals
- incomplete accessibility information for some stations
- weaker predictive signals for Comfort
- rate-limited external APIs
- reliance on a frozen network snapshot for modelling
- limited direct testing with passengers with mobility impairments
- London Underground-only coverage
- Streamlit interface not deployed as a fully integrated production backend

These limitations also help explain why the final system retained both predictive and deterministic components rather than relying entirely on one model.

---

## My Contribution

SKIP was developed as a **collaborative MSc Artificial Intelligence project at Queen Mary University of London**.

As **Team Lead**, I:

- originated the project concept
- coordinated the team and overall project direction
- built the passenger-facing **Streamlit frontend**
- supported model evaluation and interpretation of results
- contributed to final-stage coding, debugging and integration
- contributed to project framing and related work
- helped communicate the accessibility, explainability and responsible-AI motivation

The project gave me experience across both the **technical and decision-making sides of an AI project**, including problem framing, application development, evaluation and communicating model limitations.

---

## Project Links

- [← Project Overview](../README.md)
- [Modelling Notebook](../notebooks/skip-modelling.ipynb)
- [Evaluation Figures](../notebooks/evaluation-figures.ipynb)
- [Evaluation Results](../results/README.md)
- [Run Prototype](../app/README.md)
- [Project Portfolio](https://github.com/sarahnish/portfolio)

---

## Disclaimer

SKIP is an academic research prototype and is **not affiliated with or endorsed by Transport for London**.

Recommendations should not be relied upon as a guarantee of real-time transport or accessibility conditions.
