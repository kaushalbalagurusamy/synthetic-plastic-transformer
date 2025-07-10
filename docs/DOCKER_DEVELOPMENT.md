# Docker Development Environment

This guide covers how to use the containerized development environment for the Synthetic Plastic Transformer project, optimized for Claude Code CLI and ML development workflows.

## Overview

The development container provides:
- Pre-installed Claude Code CLI for AI-assisted development
- Complete Python ML environment with PyTorch, scikit-learn, and chemistry libraries
- GPU support for model training
- Isolated, reproducible development environment
- Security-hardened networking with firewall rules
- All development tools pre-configured

## Quick Start

### 1. Prerequisites

- Docker Desktop (with GPU support enabled if using NVIDIA GPUs)
- VS Code with Remote-Containers extension (optional but recommended)
- Claude API key (set as `ANTHROPIC_API_KEY` environment variable)

### 2. Starting the Development Environment

#### Option A: VS Code DevContainer (Recommended)

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. Wait for the container to build (first time takes ~10-15 minutes)

#### Option B: Docker Compose

```bash
# Start all development services
docker-compose -f docker-compose.dev.yml up -d

# Enter the development container
docker-compose -f docker-compose.dev.yml exec devcontainer zsh

# You're now in the container with Claude Code CLI available!
claude-code
```

### 3. Using Claude Code CLI in the Container

Once inside the container:

```bash
# Start Claude Code for AI-assisted development
claude-code

# The entire project is mounted at /home/developer/workspace
cd /home/developer/workspace

# All Python tools are available
python --version  # Python 3.10
pip list         # See all installed packages
conda list       # RDKit and other conda packages
```

## Container Features

### Pre-installed Tools

#### Development Tools
- **Claude Code CLI**: AI pair programming assistant
- **Python 3.10**: With all project dependencies
- **Conda**: For RDKit and chemistry libraries
- **Git**: Version control with your host credentials
- **Zsh**: With oh-my-zsh and plugins
- **tmux**: Terminal multiplexer

#### ML/Data Science Tools
- **PyTorch**: With CUDA support (GPU enabled)
- **scikit-learn**: Traditional ML algorithms
- **RDKit**: Chemistry informatics
- **Jupyter Lab**: Interactive notebooks
- **TensorBoard**: Model training visualization
- **MLflow**: Experiment tracking

#### Code Quality Tools
- **Ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks
- **bandit**: Security linter

### Directory Structure

Inside the container:
```
/home/developer/
├── workspace/           # Your project (mounted from host)
│   ├── src/            # Source code
│   ├── tests/          # Tests
│   ├── data/           # Datasets
│   ├── models/         # Trained models
│   └── ...
├── .cache/             # PyTorch and HuggingFace model cache
├── .claude/            # Claude configuration (from host)
└── .ssh/               # SSH keys (read-only from host)
```

### Environment Variables

Key environment variables set in the container:
- `PYTHONPATH=/home/developer/workspace/src`
- `DATABASE_URL=postgresql://postgres:postgres@db:5432/spt_db`
- `REDIS_URL=redis://redis:6379/0`
- `CUDA_VISIBLE_DEVICES=0` (configurable)
- `ANTHROPIC_API_KEY` (passed from host)

## Common Workflows

### 1. Training Models with GPU

```bash
# Inside the container
cd /home/developer/workspace

# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Train a model
spt-train --config configs/quantum_transfer.yaml --use-gpu

# Monitor with TensorBoard (in another terminal)
tensorboard --logdir runs/ --host 0.0.0.0
# Access at http://localhost:6006
```

### 2. Running Jupyter Lab

```bash
# Start Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Access at http://localhost:8888
# Token will be shown in the terminal
```

### 3. API Development

```bash
# Start the FastAPI server with hot reload
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Access at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 4. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_quantum_descriptors.py -v
```

### 5. Database Operations

```bash
# Access PostgreSQL
psql -h db -U postgres -d spt_db

# Run migrations
alembic upgrade head

# Initialize database
python -m src.database.init_db
```

## Advanced Usage

### Using Multiple Services

```bash
# Start all services including MLflow and TensorBoard
docker-compose -f docker-compose.dev.yml --profile ml up -d

# This starts:
# - Main dev container
# - PostgreSQL database
# - Redis
# - MLflow tracking server (http://localhost:5000)
# - TensorBoard (http://localhost:6006)
```

### GPU Configuration

```bash
# Use specific GPU
CUDA_VISIBLE_DEVICES=1 docker-compose -f docker-compose.dev.yml up -d

# Use multiple GPUs
CUDA_VISIBLE_DEVICES=0,1 docker-compose -f docker-compose.dev.yml up -d

# Disable GPU
CUDA_VISIBLE_DEVICES=-1 docker-compose -f docker-compose.dev.yml up -d
```

### Customizing the Environment

Edit `.devcontainer/devcontainer.json` to:
- Add VS Code extensions
- Change environment variables
- Modify port forwarding
- Add additional mounts

## Security Features

The container includes a firewall that:
- Blocks all outbound traffic by default
- Allows only essential domains (GitHub, PyPI, etc.)
- Logs blocked connections for debugging
- Can be customized in `.devcontainer/init-firewall.sh`

To check firewall status:
```bash
# Inside container
sudo iptables -L -n -v
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.dev.yml logs devcontainer

# Rebuild container
docker-compose -f docker-compose.dev.yml build --no-cache devcontainer
```

### GPU Not Available

```bash
# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# Ensure NVIDIA Container Toolkit is installed
```

### Permission Issues

```bash
# Fix ownership (run from host)
docker-compose -f docker-compose.dev.yml exec devcontainer chown -R developer:developer /home/developer/workspace
```

### Network Issues

```bash
# Check allowed domains in firewall
cat /usr/local/bin/init-firewall.sh

# Temporarily disable firewall (for debugging only!)
sudo iptables -P OUTPUT ACCEPT
```

## Best Practices

1. **Use Claude Code CLI for complex tasks**: The AI assistant is pre-installed and configured
2. **Commit from inside the container**: Git is configured with your host credentials
3. **Keep data in mounted volumes**: Ensures persistence across container rebuilds
4. **Use the ML profile for training**: Includes TensorBoard and MLflow
5. **Regular cleanup**: Remove unused images with `docker system prune`

## Updating the Environment

To update dependencies:

1. Modify `requirements.txt` or `.devcontainer/Dockerfile`
2. Rebuild the container:
   ```bash
   docker-compose -f docker-compose.dev.yml build devcontainer
   ```
3. Restart services:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

## Additional Resources

- [Docker Compose Reference](https://docs.docker.com/compose/)
- [VS Code DevContainers](https://code.visualstudio.com/docs/remote/containers)
- [Claude Code CLI Documentation](https://docs.anthropic.com/claude-code)
- [Project Commands Reference](../.claude/commands/README.md)