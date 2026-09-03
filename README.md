# Synthetic Plastic Transformer

[![CI](https://github.com/kaushalbalagurusamy/synthetic-plastic-transformer/actions/workflows/ci.yml/badge.svg)](https://github.com/kaushalbalagurusamy/synthetic-plastic-transformer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Materials informatics toolkit and dataset pipeline for evaluating and modeling bio-based organic natural fiber alternatives to synthetic polymers, complete with Global Organic Textile Standard (GOTS v7.0) compliance validation.

---

## Architecture & Data Pipeline

```
                    +----------------------------------------------+
                    |  Synthetic Polymer Target Specifications     |
                    |  (PET, PP, PE, Nylon 6, PS, PVC Profiles)   |
                    +----------------------+-----------------------+
                                           |
                                           v
+------------------------------------------+------------------------------------------+
|                 Materials Informatics & Property Modeling Pipeline                  |
|                                                                                      |
|  +------------------------------+                  +------------------------------+  |
|  | Natural Fiber Database       |                  | PyTorch Dataset Engine       |  |
|  | (14+ bast, leaf, seed fibers)|                  | (RDKit Descriptors & Scaling)|  |
|  | - Mechanical (Tensile, Mod)  |                  | - FiberPolymerDataset        |  |
|  | - Thermal & Moisture Regain  |                  | - FiberBlendDataset          |  |
|  | - Carbon Footprint & Water   |                  | - MaterialsDataLoader        |  |
|  +--------------+---------------+                  +--------------+---------------+  |
+-----------------|-------------------------------------------------|------------------+
                  |                                                 |
                  +------------------------+------------------------+
                                           |
                                           v
                    +----------------------------------------------+
                    |        GOTS v7.0 Compliance Validator        |
                    | - Organic content thresholds (>=70% / >=95%) |
                    | - Restricted Substance List (RSL) audit      |
                    | - Chemical hazard & processing tier checks   |
                    +----------------------+-----------------------+
                                           |
                                           v
                    +----------------------------------------------+
                    | Validated Sustainable Material Formulations  |
                    +----------------------------------------------+
```

---

## Core Capabilities

* **Natural Fiber Database**: Comprehensive profile database covering 14+ natural fiber species (hemp, flax, jute, ramie, sisal, abaca, coir, kapok, bamboo, modal, lyocell, organic cotton, silk, and wool) across 20+ physical, chemical, thermal, and environmental properties.
* **PyTorch Dataset Engine**: Specialized `Dataset` and `DataLoader` abstractions for training property prediction models, featuring RDKit molecular descriptor extraction and automated feature normalization.
* **Fiber Blend Formulation**: Multi-component blend generation calculating linear and non-linear composite properties for custom natural fiber mixtures.
* **GOTS v7.0 Verification**: Built-in certification engine checking material composition against Global Organic Textile Standard requirements, processing tiers, and restricted substance thresholds.

---

## Repository Structure

```
synthetic-plastic-transformer/
├── src/
│   ├── data/
│   │   ├── natural_fiber_properties.py # Natural fiber database & physical property metrics
│   │   └── fiber_polymer_dataset.py    # PyTorch dataset loaders & RDKit feature pipelines
│   └── utils/
│       └── gots_compliance.py          # GOTS v7.0 validation & chemical restriction auditor
├── configs/                            # Dataset and modeling configuration YAMLs
├── tests/
│   ├── unit/                           # Unit test suite (properties, datasets, GOTS)
│   └── integration/                    # Pipeline integration tests
├── scripts/                            # Data processing and evaluation scripts
├── pyproject.toml                      # Project metadata and tool configuration
└── requirements.txt                    # Core Python dependencies
```

---

## Prerequisites

* **Python**: 3.9 or higher
* **Core Libraries**: PyTorch, RDKit, NumPy, Pandas, Scikit-learn

---

## Installation

```bash
git clone https://github.com/kaushalbalagurusamy/synthetic-plastic-transformer.git
cd synthetic-plastic-transformer

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage Examples

### 1. Querying Natural Fiber Properties

```python
from src.data.natural_fiber_properties import NaturalFiberDatabase

db = NaturalFiberDatabase()

# Retrieve complete mechanical and environmental profile for Hemp
hemp = db.get_fiber("hemp")
print(f"Tensile Strength: {hemp.tensile_strength} MPa")
print(f"Elastic Modulus: {hemp.elastic_modulus} GPa")
print(f"Carbon Footprint: {hemp.carbon_footprint} kg CO2/kg")

# Find candidate natural fibers matching mechanical requirements of Polypropylene (PP)
candidates = db.find_replacements_for_polymer("polypropylene", min_tensile_strength=300)
for fiber_name, score in candidates:
    print(f"Candidate: {fiber_name} (Similarity Score: {score:.2f})")
```

### 2. Loading PyTorch Materials Datasets

```python
from src.data.fiber_polymer_dataset import FiberPolymerDataset, MaterialsDataLoader

dataset = FiberPolymerDataset(
    data_path="data/processed",
    target_properties=["tensile_strength", "elastic_modulus", "thermal_conductivity"],
    mode="train"
)

loader = MaterialsDataLoader(dataset, batch_size=32, shuffle=True)
for batch in loader:
    features, targets = batch["features"], batch["targets"]
    # Pass to downstream PyTorch model
```

### 3. Validating GOTS v7.0 Compliance

```python
from src.utils.gots_compliance import GOTSValidator, MaterialBlend

validator = GOTSValidator()

# Evaluate a proposed textile formulation
blend = MaterialBlend(
    components={"organic_flax": 0.85, "recycled_polyester": 0.15},
    processing_tier="spinning",
    chemical_inputs=["reactive_dye_04"]
)

compliance_result = validator.evaluate_blend(blend)
print(f"GOTS Certified: {compliance_result.is_compliant}")
print(f"Certification Label: {compliance_result.label_grade}") # 'Made with Organic' or 'Organic'
```

---

## Testing

Run the test suite with pytest:

```bash
# Run all unit tests
pytest tests/unit/

# Run with coverage report
pytest --cov=src tests/
```

---

## Technical Documentation & ADRs

All foundational architectural decisions and roadmaps are recorded in [`docs/adr/`](docs/adr/):

* [`docs/adr/0001-gnn-and-transfer-learning-strategy.md`](docs/adr/0001-gnn-and-transfer-learning-strategy.md) — Graph Neural Network & Transfer Learning Strategy for Bio-Polymer Modeling
* [`docs/adr/0002-multi-objective-fiber-blend-optimization.md`](docs/adr/0002-multi-objective-fiber-blend-optimization.md) — Multi-Objective Genetic Algorithm for Composite Formulation
* [`docs/adr/0003-gots-compliance-and-chemical-restriction-engine.md`](docs/adr/0003-gots-compliance-and-chemical-restriction-engine.md) — GOTS v7.0 Rule-Based Compliance & Chemical Restriction Architecture
* [`docs/adr/0004-materials-database-and-async-pipeline.md`](docs/adr/0004-materials-database-and-async-pipeline.md) — Materials Database Schema & Asynchronous Calculation Pipeline

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.