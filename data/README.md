# Data

[← Back to Project Overview](../README.md)

This folder contains the processed modelling dataset used in the SKIP machine-learning pipeline.

## Dataset

[`processed-route-features.csv`](processed-route-features.csv)

Contains **400 human-labelled candidate routes** represented using route-level features derived from TfL API and static data.

The dataset includes features covering:

- accessibility
- lift availability
- platform gaps
- crowding
- predicted carriage temperature
- interchanges
- closures
- fare-zone span
- passenger PAC goal

It also contains the human-derived suitability target used for supervised model development.

## Reproducibility

The modelling data was derived from a frozen TfL network snapshot dated **6 July 2026** to keep route features and human labels aligned to the same network state.

See the [modelling notebook](../notebooks/skip-modelling.ipynb) for the full preparation and evaluation pipeline.
