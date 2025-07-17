# Maestro

Maestro is a tool for managing and running AI agents and workflows.

## Installation

```bash
pip install git+https://github.com/AI4quantum/maestro.git@v0.3.0
```

Note: If using scoring or crewai agents, install:
```bash
pip install "maestro[crewai] @ git+https://github.com/AI4quantum/maestro.git@v0.3.0"
```

## Usage

1. Run a workflow:
```bash
maestro run <workflow_path>
```

2. Create an agent:
```bash
maestro create <agent_path>
```

3. Validate a workflow or agent:
```bash
maestro validate <path>
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/AI4quantum/maestro.git
cd maestro
```

2. Install development dependencies:
```bash
uv sync --all-extras
```

3. Run tests:
```bash
uv run pytest
```

4. Run the formatter:
```bash
uv run ruff format
```

5. Run the linter:
```bash
uv run ruff check --fix
```

## Builder Development

The Maestro Builder (web interface) has been moved to a separate repository: [maestro-builder](https://github.com/AI4quantum/maestro-builder)

For detailed instructions and development setup, please visit the [maestro-builder repository](https://github.com/AI4quantum/maestro-builder).

Quick start for the builder:
```bash
git clone https://github.com/AI4quantum/maestro-builder.git
cd maestro-builder
./start.sh    # Start both API and frontend
./stop.sh     # Stop all services
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.
