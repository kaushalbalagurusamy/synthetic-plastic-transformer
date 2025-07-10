# Development Workflow Commands

## Environment Setup

### Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### Poetry Environment
```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install with extras
poetry install --extras "dev docs"

# Add new dependency
poetry add fastapi@latest

# Add dev dependency
poetry add --dev pytest-asyncio
```

### Conda Environment
```bash
# Create conda environment
conda create -n spt python=3.10

# Activate environment
conda activate spt

# Install PyTorch with CUDA
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# Install RDKit
conda install -c conda-forge rdkit
```

## Code Quality

### Formatting with Ruff
```bash
# Format code
ruff format src/ tests/

# Check without fixing
ruff check src/ tests/

# Fix issues
ruff check src/ tests/ --fix

# Check specific rules
ruff check src/ --select E,W,F
```

### Type Checking
```bash
# Run mypy
mypy src/ --strict

# Install missing type stubs
mypy --install-types

# Check specific module
mypy src/models/protein_transfer_model.py --strict

# Generate type stubs
stubgen -p src.models -o stubs/
```

### Security Scanning
```bash
# Run bandit
bandit -r src/

# Run with specific severity
bandit -r src/ -ll  # Only high severity

# Check dependencies
safety check

# Scan for secrets
detect-secrets scan > .secrets.baseline
```

## Testing Workflow

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_quantum_descriptors.py

# Run tests matching pattern
pytest -k "test_fiber"

# Run with specific markers
pytest -m "not slow"
```

### Test Coverage
```bash
# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html

# Check coverage threshold
pytest --cov=src --cov-fail-under=90
```

### Test Debugging
```bash
# Run with debugging
pytest --pdb

# Run with detailed output
pytest -vvs

# Run with log capture
pytest --log-cli-level=DEBUG

# Profile test performance
pytest --profile
```

## Git Workflow

### Branch Management
```bash
# Create feature branch
git checkout -b feat/quantum-descriptors

# Create from specific commit
git checkout -b fix/api-timeout abc123

# Push new branch
git push -u origin feat/quantum-descriptors
```

### Commit Conventions
```bash
# Feature commit
git commit -m "feat(models): add ALIGNN architecture for bond angles"

# Fix commit
git commit -m "fix(api): resolve timeout in prediction endpoint"

# Breaking change
git commit -m "feat(data)!: restructure fiber properties schema

BREAKING CHANGE: FiberProperties now requires density field"

# Multiple changes
git commit -m "refactor(tests): improve test structure

- Separate unit and integration tests
- Add more fixtures
- Improve test coverage"
```

### Pre-commit Hooks
```bash
# Install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files

# Skip hooks (emergency only)
git commit -m "fix: urgent patch" --no-verify

# Update hooks
pre-commit autoupdate
```

## Documentation

### Generate Documentation
```bash
# Build Sphinx docs
cd docs && make html

# Serve docs locally
python -m http.server --directory docs/_build/html 8080

# Build MkDocs
mkdocs build

# Serve MkDocs with hot reload
mkdocs serve
```

### API Documentation
```bash
# Generate API docs from docstrings
sphinx-apidoc -o docs/api src/

# Update autodoc
cd docs && make clean && make html
```

## Debugging

### Python Debugging
```bash
# Run with pdb
python -m pdb src/train.py

# Run with ipdb (enhanced debugger)
python -m ipdb src/train.py

# Remote debugging with debugpy
python -m debugpy --listen 5678 --wait-for-client src/train.py
```

### Memory Profiling
```bash
# Profile memory usage
python -m memory_profiler src/train.py

# Line-by-line memory usage
python -m memory_profiler -l src/models/quantum_descriptors.py

# Generate memory report
mprof run python src/train.py
mprof plot
```

### Performance Profiling
```bash
# CPU profiling
python -m cProfile -o profile.stats src/train.py

# Visualize profile
snakeviz profile.stats

# Line profiling
kernprof -l -v src/models/protein_transfer_model.py
```

## Dependency Management

### Update Dependencies
```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Freeze current versions
pip freeze > requirements-lock.txt
```

### Vulnerability Scanning
```bash
# Check for vulnerabilities
pip-audit

# Fix automatically
pip-audit --fix

# Generate report
pip-audit --format json > vulnerabilities.json
```

## CI/CD Integration

### GitHub Actions
```bash
# Test workflow locally
act -j test

# Run specific workflow
act -W .github/workflows/ci.yml

# List available workflows
act -l
```

### Pre-release Checks
```bash
# Run all quality checks
make check-all

# Or manually:
ruff check src/ tests/
mypy src/ --strict
pytest --cov=src --cov-fail-under=90
bandit -r src/
safety check
```

## Release Process

### Version Bumping
```bash
# Bump version (poetry)
poetry version patch  # 0.1.0 -> 0.1.1
poetry version minor  # 0.1.1 -> 0.2.0
poetry version major  # 0.2.0 -> 1.0.0

# Tag release
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

### Building Packages
```bash
# Build distribution
python -m build

# Build with poetry
poetry build

# Check distribution
twine check dist/*
```