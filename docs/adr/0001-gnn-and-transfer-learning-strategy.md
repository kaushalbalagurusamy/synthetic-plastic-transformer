# ADR 0001: Graph Neural Network & Transfer Learning Strategy for Bio-Polymer Modeling

* **Status**: Proposed / Planned
* **Date**: 2026-09-02
* **Deciders**: Engineering & Materials Science Team

---

## Context & Problem Statement

Predicting the macro-mechanical properties (tensile strength, elastic modulus, thermal conductivity) of natural organic fiber composites and their ability to replace petroleum-based synthetic polymers (e.g., Polypropylene, PET, Nylon 6) requires encoding molecular structure and interfacial interaction. 

Traditional quantitative structure-property relationship (QSPR) models rely on hand-crafted 2D molecular fingerprints (Morgan/ECFP) which fail to capture 3D spatial conformation, hydrogen bonding networks in cellulose/lignin matrices, and interfacial adhesion between fiber reinforcements and bio-polymer resins.

---

## Decision Drivers

1. **Spatial & Bond Angle Representation**: Continuous-filter graph architectures must process 3D atomic coordinates and bond angle distributions.
2. **Limited Labeled Bio-Composite Data**: Experimental composite testing datasets are small (< 2,000 samples), necessitating pretraining on large computational chemistry corpora (QM9, Materials Project, PI1M).
3. **Multi-Property Inference**: The model must simultaneously predict mechanical, thermal, and degradation properties from a single forward pass.

---

## Considered Options

1. **Option 1 (Chosen)**: Dual-Stage Transfer Learning with 3D Graph Neural Networks (SchNet / ALIGNN).
2. **Option 2**: Classical Tree-Based Ensemble (XGBoost / Random Forest) using static RDKit 2D tabular descriptors.
3. **Option 3**: Sequence-based Transformers (SMILES string embeddings via ChemBERTa).

---

## Decision Outcome: Chosen Option 1

Adopt a two-stage 3D GNN transfer learning architecture:

1. **Stage 1 (Self-Supervised Pretraining)**:
   * Pretrain a continuous-filter convolutional GNN (SchNet/ALIGNN backbone) on large-scale molecular datasets (QM9 for quantum mechanical features, PI1M for polymer repeat units) using masked atom prediction and contrastive graph representation learning.
2. **Stage 2 (Bio-Composite Fine-Tuning & Multi-Task Heads)**:
   * Fine-tune the encoder against the natural fiber dataset (`src/data/natural_fiber_properties.py`) with specialized multi-task prediction heads for tensile strength ($R^2 \ge 0.85$), elastic modulus, and thermal stability.

### Positive Consequences
* Captures non-linear hydrogen bonding and 3D steric effects in cellulose microfibrils.
* Generalizes effectively to novel agricultural waste fibers with minimal laboratory test samples.

### Negative Consequences
* Requires 3D conformational generation (e.g. via RDKit ETKDG / quantum chemical relaxation) prior to inference.
* Higher computational footprint during initial pretraining phase.
