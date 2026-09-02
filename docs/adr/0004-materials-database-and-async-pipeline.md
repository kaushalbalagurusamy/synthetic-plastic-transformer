# ADR 0004: Materials Database Schema & Asynchronous Calculation Pipeline

* **Status**: Accepted (Schema) / Planned (Async Queue)
* **Date**: 2026-09-02
* **Deciders**: Engineering & Infrastructure Team

---

## Context & Problem Statement

As experimental composite formulations, polymer substitution queries, and GOTS audit logs scale, storing data solely in static CSVs/JSONs creates concurrency bottlenecks and lacks relational integrity. Additionally, computing quantum-informed 3D descriptors and running genetic algorithm searches across millions of candidate permutations requires background execution off the main application thread.

---

## Decision Drivers

1. **Relational & JSON Hybrid Storage**: Standard fiber profiles require structured columns with typed numerical ranges (e.g. `tensile_strength_min`, `tensile_strength_max`), while complex experimental formulations require semi-structured JSONB storage.
2. **Asynchronous Execution**: High-dimensional Pareto searches must execute asynchronously via worker tasks with progress polling.
3. **Auditing & Traceability**: Every GOTS compliance assessment and formulation recommendation must maintain an immutable audit trail.

---

## Decision Outcome

1. **PostgreSQL Relational Schema (`scripts/init_db.sql`)**:
   * `spt.natural_fibers`: Quantitative catalog of natural fibers, category classifications, and processing boundaries.
   * `spt.polymers`: Reference table of petroleum-based polymers (SMILES, glass transition, mechanical properties).
   * `spt.experiments`: JSONB-backed record of multi-component formulations, predicted properties, and actual lab test metrics.
   * `spt.gots_certifications`: Immutable compliance verification records.
2. **Task Queue Architecture (Future Milestone)**:
   * Redis as an in-memory message broker with Celery / async worker tasks for batch molecular featurization and parameter sweeps.
   * Minimal local SQLite / in-memory fallback for standalone library operation without Docker dependencies.

### Positive Consequences
* Clear separation between lightweight library usage (zero external services) and enterprise batch calculation workflows.
* Preserves complete database schema blueprints for production deployments.
