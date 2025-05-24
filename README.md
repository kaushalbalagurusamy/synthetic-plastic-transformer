# Synthetic Plastic Transformer 🌿🔄

## A Materials Discovery Engine for Replacing Synthetic Polymers with Organic Natural Fibers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GOTS Compliant](https://img.shields.io/badge/GOTS-Compliant-green.svg)](https://global-standard.org/)

## Overview

The Synthetic Plastic Transformer is an advanced machine learning platform that uses transfer learning from protein folding models to identify natural fiber combinations that can replace synthetic polymers while maintaining or exceeding performance requirements. The system ensures all recommendations meet GOTS (Global Organic Textile Standard) certification requirements.

### Key Features

- **Quantum-Informed Molecular Descriptors**: Integrates HOMO-LUMO gap, partial charges, and electronic properties for enhanced predictions
- **Graph Neural Networks (GNN)**: Implements SchNet and ALIGNN architectures for learning from 3D molecular structures and bond angles
- **Self-Supervised Pretraining**: Uses masked atom prediction and contrastive learning for robust representations with limited data
- **Transfer Learning from Protein Folding**: Leverages insights from AlphaFold and pretrained models on QM9/Materials Project
- **Multi-Property Optimization**: Simultaneously predicts mechanical, thermal, and functional properties
- **Comprehensive Natural Fiber Database**: Includes 14+ fibers with detailed properties (hemp, flax, silk, bamboo, pineapple, etc.)
- **GOTS Compliance**: Built-in validation for organic certification standards
- **Mixture Prediction**: Optimizes fiber blend ratios for target properties using genetic algorithms
- **Explainable AI**: Uses Shapley values and attention mechanisms for transparent decision-making

## Architecture

```
synthetic-plastic-transformer/
├── src/
│   ├── models/              # Neural network architectures
│   │   ├── protein_transfer_model.py    # Core transformer architecture
│   │   ├── graph_neural_network.py      # SchNet/ALIGNN implementations
│   │   ├── quantum_descriptors.py       # Quantum mechanical features
│   │   └── self_supervised_learning.py  # Pretraining strategies
│   ├── data/                # Data loading and dataset classes
│   │   ├── fiber_polymer_dataset.py     # Dataset implementations
│   │   └── natural_fiber_properties.py  # Comprehensive fiber database
│   ├── preprocessing/       # Data preprocessing utilities
│   ├── transfer_learning/   # Transfer learning implementations
│   └── utils/              # Helper functions and utilities
│       └── gots_compliance.py           # GOTS certification checker
├── tests/                  # Unit and integration tests
├── data/                   # Raw and processed datasets
├── notebooks/              # Jupyter notebooks for exploration
└── docs/                   # Documentation
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/synthetic-plastic-transformer.git
cd synthetic-plastic-transformer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install PyTorch Geometric (adjust CUDA version as needed)
pip install torch-scatter torch-sparse torch-geometric -f https://data.pyg.org/whl/torch-2.0.0+cu118.html

# Install in development mode
pip install -e .
```

## Quick Start

```python
from synthetic_plastic_transformer import MaterialsDiscoveryEngine
from src.data.natural_fiber_properties import get_fiber_properties

# Initialize the engine with quantum descriptors
engine = MaterialsDiscoveryEngine(use_quantum_descriptors=True)

# Define target polymer properties
target_properties = {
    'tensile_strength': 50.0,  # MPa
    'elastic_modulus': 2.5,    # GPa
    'thermal_conductivity': 0.3,  # W/mK
    'water_absorption': 5.0,    # %
    'biodegradability': True,
    'uv_resistance': 0.7  # 0-1 scale
}

# Find natural fiber replacements
recommendations = engine.predict_replacement(
    target_properties=target_properties,
    max_processing_temp=150,  # °C (GOTS limit)
    include_agricultural_waste=True  # Consider banana/pineapple fibers
)

# Display results
for rec in recommendations[:3]:
    print(f"Fiber Mix: {rec['fiber_composition']}")
    print(f"Processing: {rec['processing_method']}")
    print(f"Match Score: {rec['property_match_score']:.2f}")
    print(f"GOTS Compliant: {rec['gots_compliant']}")
    print(f"Predicted Properties: {rec['predicted_properties']}")
    print("---")
```

## Core Components

### 1. Quantum-Informed Property Prediction

The system calculates quantum mechanical descriptors to enhance property predictions:

- **Electronic Properties**: HOMO-LUMO gap estimation, partial charge distribution
- **Topological Indices**: Chi indices, Kappa shape indices, Balaban J
- **3D Structure Features**: When available, uses SchNet for distance-based convolutions

### 2. Graph Neural Network Architecture

Implements state-of-the-art GNN architectures:

- **SchNet Layers**: Continuous-filter convolutions with Gaussian distance expansion
- **ALIGNN Integration**: Bond angle information for improved mechanical property prediction
- **Multi-Task Heads**: Specialized prediction heads for each property

### 3. Self-Supervised Pretraining

Enables learning from limited labeled data:

- **Masked Atom Prediction**: Similar to BERT, predicts masked atom types
- **Graph Contrastive Learning**: Learns invariant representations through augmentation
- **Multi-Task Pretraining**: Combines self-supervised and auxiliary supervised tasks

### 4. Enhanced Natural Fiber Database

Comprehensive database with 14+ natural fibers including:

- **Bast Fibers**: Hemp (550-1110 MPa), Flax (345-1500 MPa), Ramie (400-938 MPa)
- **Leaf Fibers**: Sisal, Pineapple leaf (PALF)
- **Seed Fibers**: Cotton, Kapok (ultralight, hydrophobic), Coir
- **Protein Fibers**: Silk, Wool (with elasticity data)
- **Agricultural Waste**: Banana fiber, mechanically-processed bamboo

Each fiber includes 30+ properties: mechanical, thermal, moisture, environmental, and processing characteristics.

### 5. Advanced GOTS Compliance Checker

Ensures all recommendations meet organic certification standards:

- Validates fiber sources and organic content percentages
- Checks processing temperatures against fiber-specific limits
- Verifies chemical treatments (enzymatic, citric acid, hydrogen peroxide)
- Monitors water/energy consumption limits

### 6. Multi-Property Optimizer

Balances multiple material properties simultaneously:

- Mechanical: tensile strength, elastic modulus, elongation at break
- Thermal: glass transition temperature, thermal conductivity, heat capacity
- Functional: water absorption, UV resistance, dielectric properties, antimicrobial
- Environmental: biodegradability rate, carbon footprint, water usage

## Datasets

### Required Data Format

The system now supports multiple input formats:

```python
# SMILES-based input for polymers
{
  "polymer_id": "HDPE_001",
  "smiles": "CC(C)CC(C)CC(C)C",  # Repeat unit
  "properties": {...}
}

# Graph-based input (PyG format)
{
  "x": node_features,  # [num_atoms, features]
  "edge_index": connectivity,  # [2, num_edges]
  "pos": coordinates,  # [num_atoms, 3] optional
  "y": target_properties
}
```

### Data Sources

- **Polymer Properties**: PolyInfo, PI1M (1M+ virtual polymers), Khazana databases
- **Quantum Data**: QM9 (134k molecules), Materials Project
- **Natural Fiber Data**: Literature compilation + GOTS certified fiber databases
- **Processing Methods**: Industry standard procedures with environmental impact data

## Training

### Self-Supervised Pretraining

```bash
# Pretrain on unlabeled polymer structures
python pretrain.py --config configs/self_supervised_config.yaml \
                   --dataset PI1M \
                   --tasks masked_atom contrastive
```

### Transfer Learning with Quantum Models

```bash
# Fine-tune from QM9 pretrained model
python train.py --config configs/transfer_config.yaml \
                --pretrained_model models/schnet_qm9.pth \
                --freeze_encoder_epochs 5
```

### Multi-Task Training

```bash
# Train on all properties simultaneously
python train.py --config configs/multitask_config.yaml \
                --loss_weights tensile:1.0 modulus:1.0 biodegradability:1.5
```

## Evaluation

The system includes comprehensive evaluation metrics:

```bash
python evaluate.py --model_path models/best_model.pth \
                   --test_data data/test_set.json \
                   --compute_shap  # For explainability
```

Metrics include:
- Property prediction accuracy (MAE, RMSE, R²)
- GOTS compliance rate
- Biodegradability assessment
- Cost-effectiveness analysis
- Uncertainty quantification

## Examples

### Example 1: Replacing HDPE for Packaging

```python
# Using quantum descriptors for better accuracy
result = engine.replace_polymer(
    polymer="HDPE",
    application="packaging",
    constraints={
        "min_uv_resistance": 0.7,
        "max_water_absorption": 5.0,
        "require_antimicrobial": True
    }
)
# Recommendation: 45% Hemp, 30% Pineapple leaf, 25% Chitosan coating
# Processing: Enzymatic degumming at 60°C, natural antimicrobial treatment
```

### Example 2: High-Performance Athletic Wear

```python
# Moisture-wicking with stretch
result = engine.optimize_blend(
    target_properties={
        "moisture_wicking": "high",
        "elongation": 15.0,  # %
        "quick_dry": True,
        "tensile_strength": 400  # MPa
    },
    allowed_fibers=["hemp", "wool", "silk", "kapok"]
)
# Recommendation: 40% Hemp, 25% Merino wool, 20% Silk, 15% Kapok
# Fabric construction: Dual-layer knit with kapok inner layer
```

## API Reference

See [API Documentation](docs/api.md) for detailed API reference.

## Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/unit/test_quantum_descriptors.py
pytest tests/unit/test_graph_neural_network.py

# Run with coverage
pytest --cov=synthetic_plastic_transformer tests/
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this project in your research, please cite:

```bibtex
@software{synthetic_plastic_transformer,
  title={Synthetic Plastic Transformer: A Quantum-Informed Materials Discovery Engine for Natural Fiber Composites},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/synthetic-plastic-transformer}
}
```

## Acknowledgments

- Inspired by DeepMind's AlphaFold for protein structure prediction
- SchNet and ALIGNN architectures for molecular property prediction
- GOTS (Global Organic Textile Standard) for certification guidelines
- Open-source polymer databases: PolyInfo, PI1M, Khazana, QM9

## Contact

For questions or collaborations, please open an issue or contact [your-email@example.com] 