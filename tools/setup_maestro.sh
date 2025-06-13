#!/usr/bin/env bash
#
# Usage:
#   source ./tools/setup_maestro.sh (from root level)
#
# This will:
#   1) Install all uv deps
#   2) Drop you into the uv venv shell

uv sync

# Create virtual environment
uv venv --python 3.12 .venv

# Activate virtual environment
source .venv/bin/activate

# Install additional dependencies
uv pip install crewai litellm==1.67.0.post1