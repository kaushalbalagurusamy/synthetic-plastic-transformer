# ADR 0002: Multi-Objective Genetic Algorithm for Composite Formulation

* **Status**: Proposed / Planned
* **Date**: 2026-09-02
* **Deciders**: Engineering & Materials Science Team

---

## Context & Problem Statement

Replacing standard synthetic polymers (e.g., Polypropylene in automotive paneling or PET in technical apparel) cannot typically be achieved with a single mono-fiber due to conflicting engineering tradeoffs:
* High-strength bast fibers (e.g. Flax, Hemp) offer high tensile strength ($> 800\text{ MPa}$) but exhibit high stiffness and moisture absorption.
* Seed/fruit fibers (e.g. Kapok, Coir) provide lightweight density and hydrophobic characteristics but lower structural modulus.

To synthesize realistic sustainable alternatives, the system must determine optimal multi-fiber blend ratios (e.g., $40\%\text{ Hemp} + 35\%\text{ Flax} + 25\%\text{ Bio-Resin}$) that satisfy multiple competing performance constraints simultaneously.

---

## Decision Drivers

1. **Non-Linear Composite Behavior**: Composite properties follow Halpin-Tsai and modified rule-of-mixtures dynamics with fiber aspect ratio thresholds.
2. **Multi-Constraint Optimization**: Formulations must optimize structural strength while minimizing carbon footprint, raw material cost, and water usage.
3. **Pareto Frontier Output**: Engineers need a spectrum of candidate solutions (e.g. Lowest Cost vs. Highest Tensile Strength) rather than a single fixed answer.

---

## Decision Outcome

Implement a multi-objective evolutionary algorithm (NSGA-II) integrated with the PyTorch property prediction pipeline:

1. **Genome Representation**:
   * Vector of continuous blend weights $\mathbf{w} = [w_1, w_2, \dots, w_K]$ where $\sum w_i = 1.0$ across candidate fiber species and matrix resins.
2. **Objective Functions**:
   * Maximize Tensile Strength / Modulus ($f_1$).
   * Minimize Carbon Footprint ($\text{kg CO}_2\text{e / kg}$) ($f_2$).
   * Minimize Cost per Metric Ton ($f_3$).
   * Minimize Water Absorption percentage ($f_4$).
3. **Hard Constraint Filtering**:
   * Enforce minimum thermal degradation temperature ($T_{\text{service}} \ge 150^\circ\text{C}$).
   * Enforce GOTS compliance criteria ($\ge 70\%$ certified organic component).

### Positive Consequences
* Automatically explores high-dimensional mixture spaces without manual trial-and-error laboratory compounding.
* Delivers explainable Pareto-optimal tradeoffs to material engineers.
