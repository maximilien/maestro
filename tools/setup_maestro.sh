#!/usr/bin/env bash
#
# Usage:
#   source ./tools/setup_maestro.sh (from root level)
#
# This will:
#   1) Install all uv deps
#   2) Drop you into the uv venv shell

uv sync

VENV_PATH=$(uv venv --python 3.12 --with crewai litellm==1.67.0.post1)
source "$VENV_PATH/bin/activate"