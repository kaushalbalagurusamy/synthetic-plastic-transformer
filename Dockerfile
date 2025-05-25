# Multi-stage build for synthetic-plastic-transformer
# Stage 1: Base image with Python and system dependencies
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    wget \
    curl \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxi6 \
    libxtst6 \
    libglib2.0-0 \
    libgtk-3-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies installation
FROM base as dependencies

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install torch-geometric torch-scatter torch-sparse torch-cluster torch-spline-conv \
        -f https://data.pyg.org/whl/torch-2.0.0+cpu.html && \
    pip install -r requirements.txt

# Stage 3: Application
FROM dependencies as app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Copy application code
COPY --chown=app:app . .

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data/raw data/processed models configs logs

# Set the default command
CMD ["python", "-m", "synthetic_plastic_transformer.cli", "--help"]

# Stage 4: Development image with additional tools
FROM app as development

USER root

# Install development dependencies
RUN pip install \
    jupyter \
    jupyterlab \
    ipython \
    notebook \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    pre-commit \
    sphinx \
    sphinx-rtd-theme

USER app

# Expose ports for Jupyter and API
EXPOSE 8888 8000

# Default to Jupyter Lab for development
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

# Stage 5: Production image (default)
FROM app as production

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import synthetic_plastic_transformer; print('OK')" || exit 1

# Set production environment
ENV ENVIRONMENT=production

# Default command for production
CMD ["python", "-m", "synthetic_plastic_transformer.api.server"] 