# Frozen TfL Snapshot

[← Back to Data](../README.md)

This folder contains the frozen station-level TfL snapshot used during SKIP model development and evaluation.

## Files

- [`stations-2026-07-06.csv`](stations-2026-07-06.csv) — London Underground station registry used by the project.
- [`station-attributes-2026-07-06.csv`](station-attributes-2026-07-06.csv) — station-level accessibility, crowding, lift, closure and predicted temperature attributes used to construct route features.

## Snapshot Date

The data was frozen on **6 July 2026** so that route features, human labels and model evaluation referred to a consistent network state.

This snapshot supports the reproducibility of the modelling pipeline while avoiding dependence on changing live API responses.

## Related Resources

- [Data Overview](../README.md)
- [Modelling Notebook](../../notebooks/skip-modelling.ipynb)
- [Project Overview](../../README.md)
