# AGENTS.md — AI Development & Architecture Guidelines

Single source of truth for AI coding assistants and developers contributing to `synthetic-plastic-transformer`.

---

## 1. Project Philosophy & Architecture

The Synthetic Plastic Transformer is a materials informatics toolkit for finding and modeling organic, bio-based natural fiber alternatives to synthetic polymers, validated against GOTS v7.0 compliance standards.

### Core Modules
* `src/data/natural_fiber_properties.py`: Quantitative database of 14+ organic fibers with physical, mechanical, thermal, and chemical metrics.
* `src/data/fiber_polymer_dataset.py`: PyTorch `Dataset` and `DataLoader` classes with RDKit molecular descriptor integration.
* `src/utils/gots_compliance.py`: Global Organic Textile Standard (GOTS v7.0) certification and chemical restriction validation engine.
* `docs/adr/`: Architectural Decision Records documenting system decisions and long-term design roadmaps.

---

## 2. Engineering Standards & Code Hygiene

* **Python Standard**: Python 3.9+, strict type annotations (`typing`, `dataclasses`).
* **Clean Documentation**: Zero emoji stuffing in docstrings, commit messages, and technical markdown.
* **Deterministic Rules**: GOTS compliance and validation logic must remain deterministic and auditable in `src/utils/gots_compliance.py`.
* **Testing Protocol**: All new features or dataset loaders must include unit tests under `tests/unit/`. Run `pytest tests/unit/` before committing.

---

## 3. Key Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run unit tests
pytest tests/unit/

# Run tests with coverage
pytest --cov=src tests/
```
