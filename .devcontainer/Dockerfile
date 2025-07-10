# Synthetic Plastic Transformer Development Container
# Optimized for Claude Code CLI and ML development

FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    SHELL=/bin/zsh

# Install system dependencies and development tools
RUN apt-get update && apt-get install -y \
    # Build essentials
    gcc g++ git wget curl make cmake \
    # Python scientific computing dependencies
    libblas-dev liblapack-dev gfortran \
    # Chemistry libraries dependencies
    libboost-dev libboost-thread-dev libboost-system-dev \
    # OpenGL for molecular visualization
    libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 \
    libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 \
    # Development tools
    vim nano htop tree jq \
    # Shell and terminal
    zsh tmux \
    # Claude Code CLI dependencies
    nodejs npm \
    # Security tools (from verbatim-ai setup)
    iptables ipset iproute2 \
    # PostgreSQL client
    postgresql-client \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Install oh-my-zsh and plugins
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting \
    && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k

# Configure zsh
RUN echo 'export ZSH="$HOME/.oh-my-zsh"' >> ~/.zshrc \
    && echo 'ZSH_THEME="powerlevel10k/powerlevel10k"' >> ~/.zshrc \
    && echo 'plugins=(git docker python pip zsh-autosuggestions zsh-syntax-highlighting)' >> ~/.zshrc \
    && echo 'source $ZSH/oh-my-zsh.sh' >> ~/.zshrc \
    && echo 'HISTFILE=~/.zsh_history' >> ~/.zshrc \
    && echo 'HISTSIZE=10000' >> ~/.zshrc \
    && echo 'SAVEHIST=10000' >> ~/.zshrc

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Create workspace directory
WORKDIR /workspace

# Install PyTorch with CUDA support (if available)
RUN pip install --upgrade pip setuptools wheel && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install PyTorch Geometric
RUN pip install torch-geometric torch-scatter torch-sparse torch-cluster torch-spline-conv \
    -f https://data.pyg.org/whl/torch-2.0.0+cu118.html

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install development dependencies
RUN pip install \
    jupyter jupyterlab ipython notebook \
    pytest pytest-cov pytest-asyncio pytest-mock hypothesis \
    ruff mypy bandit safety \
    pre-commit detect-secrets \
    sphinx sphinx-rtd-theme mkdocs mkdocs-material \
    ipdb memory-profiler line-profiler \
    mlflow tensorboard \
    httpx pytest-httpx \
    watchdog ariadne-codegen

# Install conda for RDKit (best practice for chemistry libraries)
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh \
    && /opt/conda/bin/conda install -c conda-forge rdkit -y \
    && /opt/conda/bin/conda clean -afy

# Add conda to PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Create directories for the project
RUN mkdir -p /workspace/data/raw /workspace/data/processed \
    /workspace/models /workspace/logs /workspace/configs \
    /workspace/notebooks /workspace/results

# Setup security script (adapted from verbatim-ai)
COPY .devcontainer/init-firewall.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/init-firewall.sh

# Create non-root user with sudo for firewall
RUN useradd -m -s /bin/zsh -G sudo developer \
    && echo "developer ALL=(ALL) NOPASSWD: /usr/local/bin/init-firewall.sh" >> /etc/sudoers

# Switch to non-root user
USER developer
WORKDIR /home/developer/workspace

# Copy zsh config to user
RUN cp -r /root/.oh-my-zsh /home/developer/ \
    && cp /root/.zshrc /home/developer/

# Set up Python path
ENV PYTHONPATH="/home/developer/workspace/src:${PYTHONPATH}"

# Expose ports
EXPOSE 8000 8888 6006 5000 3000

# Set the default shell
SHELL ["/bin/zsh", "-c"]

# Default command
CMD ["/bin/zsh"]