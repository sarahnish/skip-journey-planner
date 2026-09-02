<p align="center">
  <img src="app/logo.png" alt="SKIP logo" width="180"/>
</p>

# SKIP — Intelligent Journey Recommendation System

An interpretable London Underground journey-planning system that combines graph-based route generation, rule-based scoring, and machine-learning ranking to recommend routes based on **punctuality, accessibility, or comfort**.

> **Project role:** Project Lead — Initiated project concept and led full-lifecycle development for a collaborative MSc AI project.

## Overview

Traditional journey planners tend to optimise primarily for travel time. SKIP was designed to explore a more passenger-centred approach by allowing users to prioritise different journey needs.

Given an origin, destination, and passenger goal, SKIP:

1. Finds routes: Generates candidate paths across the London Underground network.
2. Scores & ranks: Evaluates accessibility, speed, and comfort using ML models tailored to your goal.
3. Recommends: Delivers ranked journey options complete with confidence scores and trade-offs.

The system supports three journey PAC goals:

- **Punctuality**
- **Accessibility**
- **Comfort**

## Key Features

- 🚇 Graph-based routing across **272 London Underground stations**
- 🎯 Goal-specific recommendations for punctuality, accessibility, and comfort
- 🤖 Machine-learning ranking using models including Logistic Regression, Random Forest, and Gradient Boosting
- 🔎 Interpretable route scoring and feature-level drivers
- 🛡️ Recall-based safety mechanism for route recommendations
- 🚩 Honesty flags when no route confidently satisfies the selected goal
- 🧊 Frozen-data snapshot for reproducible modelling and evaluation
- 🖥️ Passenger-facing Streamlit interface
- 🔤 Station-name validation and suggestions for misspelled inputs

## System Workflow

```text
Transport & Station Data
        ↓
Data Processing & Feature Engineering
        ↓
Frozen Data Snapshot
        ↓
London Underground Network Graph
        ↓
Candidate Route Generation
        ↓
PAC Interpretable Scoring
        ↓
Goal-Specific ML Models
        ↓
Safety & Confidence Checks
        ↓
Ranked Journey Recommendations
        ↓
Streamlit User Interface

