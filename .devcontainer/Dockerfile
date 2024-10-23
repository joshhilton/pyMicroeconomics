FROM mcr.microsoft.com/devcontainers/python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLIT_ROOT_INSTALL=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN python -m pip install --upgrade pip \
    && python -m pip install \
    flit>=3.8.0 \
    pre-commit \
    ipykernel \
    jupyter

# Set correct working directory and Python path
WORKDIR /workspaces/pyMicroeconomics
ENV PYTHONPATH=/workspaces/pyMicroeconomics/src:$PYTHONPATH