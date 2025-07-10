# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Synthetic Plastic Transformer is a quantum-informed materials discovery platform that uses machine learning to identify natural fiber combinations that can replace synthetic polymers. It leverages transfer learning from protein folding models and ensures GOTS (Global Organic Textile Standard) compliance.

## Technology Stack

- **Python Version**: 3.8-3.11 (3.10+ recommended)
- **ML Frameworks**: PyTorch, scikit-learn, TensorFlow
- **Chemistry Libraries**: RDKit, PyMatgen, Mordred
- **API Framework**: FastAPI with Pydantic v2
- **Database**: PostgreSQL with SQLAlchemy
- **Task Queue**: Celery with Redis
- **Testing**: pytest with coverage
- **Code Quality**: Ruff (replacing black, isort, flake8)
- **Type Checking**: mypy with strict mode
- **Documentation**: Google-style docstrings

## Development Commands

### Running the Application

#### Using DevContainer (Recommended for Claude Code)
```bash
# Open in VS Code and reopen in container
# OR use Docker Compose directly:
docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml exec devcontainer zsh

# Inside container, Claude Code CLI is available:
claude-code
```

#### Standard Docker Compose
```bash
# Start full development environment with Docker
docker-compose up -d

# Start production services
docker-compose --profile production up -d

# Start with monitoring stack
docker-compose --profile monitoring up -d
```

For detailed Docker development setup, see [Docker Development Guide](docs/DOCKER_DEVELOPMENT.md).

### Testing

```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=src tests/

# Run tests in Docker
docker-compose exec app pytest tests/
```

### Code Quality

```bash
# Format and lint with Ruff (replaces black, isort, flake8)
ruff check src/ tests/ --fix
ruff format src/ tests/

# Type checking with strict mode
mypy src/ --strict

# Security scanning
bandit -r src/

# Run all pre-commit hooks
pre-commit run --all-files

# Check for dependency vulnerabilities
safety check
```

### Building and Installation

```bash
# Install in development mode
pip install -e .

# Install with all extras
pip install -e ".[dev,docs]"

# Build Docker image
docker build -t synthetic-plastic-transformer .

# Deploy to staging/production
./scripts/deploy.sh staging
./scripts/deploy.sh production
```

## Architecture Overview

### Core ML Components

1. **Protein Transfer Model** (`src/models/protein_transfer_model.py`): Transformer architecture leveraging protein folding insights
2. **Graph Neural Networks** (`src/models/graph_neural_network.py`): SchNet and ALIGNN implementations for molecular structure learning
3. **Quantum Descriptors** (`src/models/quantum_descriptors.py`): HOMO-LUMO gap and electronic property calculations
4. **Self-Supervised Learning** (`src/models/self_supervised_learning.py`): Pretraining strategies for limited data scenarios

### Data Processing Pipeline

1. **Natural Fiber Database** (`src/data/natural_fiber_properties.py`): Contains 14+ fiber types with 30+ properties each
2. **Dataset Classes** (`src/data/fiber_polymer_dataset.py`): PyTorch datasets for polymer and fiber data
3. **GOTS Compliance** (`src/utils/gots_compliance.py`): Validates organic certification requirements

### Service Architecture

- **FastAPI Application**: Main API service running on port 8000
- **PostgreSQL Database**: Primary data storage
- **Redis**: Caching and Celery task queue
- **Celery Workers**: Background task processing
- **Monitoring Stack**: Prometheus + Grafana for observability

## Key Development Patterns

### Multi-Task Learning
The system predicts multiple properties simultaneously:
- Mechanical: tensile strength, elastic modulus, elongation
- Thermal: conductivity, glass transition temperature
- Functional: water absorption, UV resistance, antimicrobial
- Environmental: biodegradability, carbon footprint

### Transfer Learning Workflow
1. Pretrain on QM9/Materials Project quantum data
2. Fine-tune on polymer-specific datasets
3. Apply to natural fiber prediction tasks

### Fiber Blend Optimization
Uses genetic algorithms to optimize fiber mix ratios for target properties while maintaining GOTS compliance.

## Testing Strategy

- **Unit Tests**: Test individual components (models, utils, data processing)
- **Integration Tests**: Test API endpoints and full prediction pipeline
- **Property Tests**: Use Hypothesis for property-based testing
- **Performance Tests**: Ensure model inference meets latency requirements

## Deployment Notes

- Production uses multi-stage Docker builds for optimized images
- Nginx handles SSL termination and load balancing
- GitHub Actions CI/CD pipeline runs on every push
- Automated deployment to staging on main branch updates
- Manual approval required for production deployment

## Common Tasks

### Adding New Fibers
1. Update `src/data/natural_fiber_properties.py` with fiber properties
2. Ensure all required properties are included
3. Validate GOTS compliance parameters
4. Update tests in `tests/unit/test_gots_compliance.py`

### Training New Models
1. Configure training parameters in `configs/`
2. Use appropriate pretraining strategy from `src/models/self_supervised_learning.py`
3. Monitor training with TensorBoard
4. Evaluate on holdout test set

### API Development
1. Add new endpoints to FastAPI application with proper type annotations
2. Implement request/response models with Pydantic v2
3. Add async handlers for I/O operations
4. Implement proper dependency injection
5. Add integration tests for new endpoints
6. Update API documentation with examples

## Python Development Standards

### Type Annotations
All functions, methods, and class members MUST have type annotations:

```python
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel

async def predict_replacement(
    target_properties: Dict[str, float],
    constraints: Optional[Dict[str, Any]] = None
) -> List[FiberRecommendation]:
    """Predict natural fiber replacements for target properties.
    
    Args:
        target_properties: Dictionary of desired material properties.
        constraints: Optional constraints for the prediction.
        
    Returns:
        List of fiber recommendations sorted by match score.
        
    Raises:
        ValueError: If target_properties are invalid.
    """
    pass
```

### Docstrings
Use Google-style docstrings for all functions, classes, and modules:

```python
def calculate_quantum_descriptors(molecule: Chem.Mol) -> Dict[str, float]:
    """Calculate quantum mechanical descriptors for a molecule.
    
    Computes HOMO-LUMO gap, partial charges, and topological indices
    using RDKit and custom quantum calculations.
    
    Args:
        molecule: RDKit molecule object.
        
    Returns:
        Dictionary containing:
            - homo_lumo_gap: Energy gap in eV
            - partial_charges: List of atomic partial charges
            - chi_indices: Chi connectivity indices
            
    Example:
        >>> mol = Chem.MolFromSmiles("CCO")
        >>> descriptors = calculate_quantum_descriptors(mol)
        >>> print(descriptors["homo_lumo_gap"])
        8.5
    """
    pass
```

### Testing Conventions
All tests use pytest with proper fixtures and type annotations:

```python
from typing import TYPE_CHECKING
import pytest
from unittest.mock import Mock

if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from pytest_mock.plugin import MockerFixture

@pytest.fixture
def fiber_dataset() -> FiberPolymerDataset:
    """Fixture providing a test fiber dataset."""
    return FiberPolymerDataset(test_mode=True)

@pytest.mark.parametrize("fiber_type,expected_strength", [
    ("hemp", 550.0),
    ("flax", 345.0),
    ("silk", 400.0),
])
async def test_fiber_properties(
    fiber_type: str,
    expected_strength: float,
    fiber_dataset: FiberPolymerDataset,
    mocker: MockerFixture
) -> None:
    """Test that fiber properties are correctly loaded.
    
    Args:
        fiber_type: Type of natural fiber to test.
        expected_strength: Expected tensile strength in MPa.
        fiber_dataset: Test dataset fixture.
        mocker: Pytest mocker fixture.
    """
    # Test implementation
    pass
```

### Error Handling
Use specific exceptions with informative messages:

```python
class FiberNotFoundError(Exception):
    """Raised when a requested fiber is not in the database."""
    pass

class GOTSComplianceError(Exception):
    """Raised when a fiber blend violates GOTS standards."""
    
    def __init__(self, violation: str, blend: Dict[str, float]) -> None:
        self.violation = violation
        self.blend = blend
        super().__init__(f"GOTS violation: {violation} for blend {blend}")
```

### Async Best Practices
Use async/await for I/O operations:

```python
async def fetch_polymer_data(
    polymer_id: str,
    db: AsyncSession
) -> Optional[PolymerProperties]:
    """Fetch polymer data from database asynchronously.
    
    Args:
        polymer_id: Unique identifier for the polymer.
        db: Async database session.
        
    Returns:
        Polymer properties if found, None otherwise.
    """
    async with db.begin():
        result = await db.execute(
            select(PolymerProperties).where(
                PolymerProperties.id == polymer_id
            )
        )
        return result.scalar_one_or_none()
```

### ML/Chemistry Specific Guidelines

1. **Data Validation**: Always validate chemical structures and properties
2. **Reproducibility**: Set random seeds and log all parameters
3. **Memory Management**: Use generators for large datasets
4. **GPU Utilization**: Check CUDA availability before model initialization
5. **Model Serialization**: Use proper versioning for saved models

### Commit Message Convention
Follow Conventional Commits specification:

```bash
# Feature
feat(models): add ALIGNN architecture for bond angle learning

# Bug fix
fix(api): correct async handler for polymer prediction endpoint

# Breaking change
feat(data)!: change fiber property schema to support new attributes

# Documentation
docs(readme): update installation instructions for GPU support

# Performance
perf(training): optimize batch processing for large molecules

# Testing
test(gots): add edge cases for compliance validation
```

## Commands and Development Guidelines

### Quick Reference
For detailed command references, see the `.claude/commands/` directory:
- [Model Training Commands](.claude/commands/01-model-training.md)
- [Data Processing Commands](.claude/commands/02-data-processing.md)
- [API Operations Commands](.claude/commands/03-api-operations.md)
- [Development Workflow Commands](.claude/commands/04-development-workflow.md)

### Cursor Rules
Development patterns and best practices are documented in `.cursor/rules/`:
- [General Development Rules](.cursor/rules/00-general.md)
- [Python Patterns](.cursor/rules/01-python-patterns.md)
- [ML/Chemistry Guidelines](.cursor/rules/02-ml-chemistry.md)
- [FastAPI Guidelines](.cursor/rules/03-fastapi.md)
- [Testing Guidelines](.cursor/rules/04-testing.md)

## Common Development Patterns

### Creating New Models
When adding new neural network architectures:

1. Inherit from `BaseModel` in `src/models/base.py`
2. Implement required methods with type annotations
3. Add configuration class in `src/configs/model_configs.py`
4. Create unit tests in `tests/models/`
5. Document architecture in docstring with paper references

### Adding New Fibers
1. Update `src/data/natural_fiber_properties.py`:
   ```python
   FIBER_PROPERTIES["new_fiber"] = FiberProperties(
       tensile_strength=(min_val, max_val),
       elastic_modulus=value,
       # ... all required properties
   )
   ```
2. Validate against GOTS requirements
3. Add tests for new fiber
4. Update documentation

### Implementing New Endpoints
1. Define Pydantic models in `src/api/schemas/`:
   ```python
   class PredictionRequest(BaseModel):
       target_properties: Dict[str, float]
       constraints: Optional[Dict[str, Any]] = None
       
   class PredictionResponse(BaseModel):
       recommendations: List[FiberRecommendation]
       processing_time: float
   ```
2. Implement endpoint in `src/api/routes/`
3. Add dependency injection for services
4. Write integration tests
5. Update OpenAPI documentation

## Troubleshooting

### Common Issues
1. **CUDA out of memory**: Reduce batch size or use gradient accumulation
2. **RDKit import errors**: Ensure conda environment is activated
3. **Type checking failures**: Run `mypy --install-types` to install stubs
4. **Test failures**: Check fixture scope and async test markers

### Performance Optimization
1. Use `torch.jit.script` for production model inference
2. Implement caching with Redis for repeated predictions
3. Use batch processing for multiple molecules
4. Profile with `cProfile` or `line_profiler`