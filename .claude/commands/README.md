# Claude Commands

This directory contains organized command references for the Synthetic Plastic Transformer project. These commands are designed to help you quickly perform common tasks during development.

## Command Categories

### 1. [Model Training](./01-model-training.md)
- Training models with various configurations
- Transfer learning from protein folding models
- Multi-task and self-supervised learning
- Model evaluation and prediction
- Hyperparameter optimization
- Distributed training

### 2. [Data Processing](./02-data-processing.md)
- Processing fiber and polymer data
- Generating molecular descriptors
- GOTS compliance validation
- Dataset creation and validation
- Data transformation and analysis
- Database operations

### 3. [API Operations](./03-api-operations.md)
- Starting development and production servers
- Testing API endpoints
- Performance testing and benchmarking
- API monitoring and logging
- Deployment configurations
- Maintenance operations

### 4. [Development Workflow](./04-development-workflow.md)
- Environment setup (venv, poetry, conda)
- Code quality tools (ruff, mypy, bandit)
- Testing and coverage
- Git workflow and conventions
- Documentation generation
- Debugging and profiling
- Dependency management
- CI/CD integration

## Quick Start

### Initial Setup
```bash
# Clone repository
git clone https://github.com/yourusername/synthetic-plastic-transformer.git
cd synthetic-plastic-transformer

# Create environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run pre-commit hooks
pre-commit install
```

### Common Tasks

#### Run Tests
```bash
pytest --cov=src --cov-report=html
```

#### Start API Server
```bash
uvicorn src.api.main:app --reload
```

#### Train Model
```bash
spt-train --config configs/quantum_transfer.yaml --use-gpu
```

#### Process Data
```bash
python -m src.preprocessing.process_fibers --input data/raw/new_fibers.csv
```

## Command Conventions

- All commands assume you're in the project root directory
- Commands using `python -m` ensure proper module resolution
- Use `--help` flag with any command for detailed options
- Environment variables can override config file settings

## Environment Variables

Key environment variables used by commands:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/spt_db

# Redis
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development

# ML
CUDA_VISIBLE_DEVICES=0,1
MLFLOW_TRACKING_URI=http://localhost:5000
```

## Tips

1. **Use Tab Completion**: Many commands support tab completion for file paths and options
2. **Check Logs**: Always check logs in `logs/` directory for detailed error information
3. **Dry Run**: Many commands support `--dry-run` to preview actions without executing
4. **Parallel Processing**: Use `-n` or `--n-workers` flags when available for faster processing
5. **GPU Usage**: Set `CUDA_VISIBLE_DEVICES` to control GPU allocation

## Troubleshooting

If commands fail:

1. Check virtual environment is activated
2. Verify all dependencies are installed: `pip install -e ".[dev]"`
3. Check environment variables are set correctly
4. Look for error details in logs
5. Run with `--debug` flag for verbose output

## Contributing

When adding new commands:

1. Follow the existing format and structure
2. Include examples with expected output
3. Document all options and flags
4. Add to appropriate category file
5. Update this README if adding new categories