#!/bin/bash

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .

# Copy environment files
cp example.env .env
cp .env ./../common/src
