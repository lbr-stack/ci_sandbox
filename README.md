# ci_sandbox

GH Actions Sandbox

## Performance Benchmarking Tool

This repository contains a Python project with CLI tools for performance benchmarking using GitHub Actions.

### CLI Commands

The project provides two CLI entrypoints built with [typer](https://typer.tiangolo.com/):

#### `compute`
Computes performance metrics and outputs them to a JSON file. Includes a 30-second sleep to simulate a long-running job.

```bash
compute
```

Output: `performance_result.json` with structure:
```json
{
  "performance": 0.7234,
  "timestamp": 1234567890.123,
  "status": "completed"
}
```

#### `evaluate`
Evaluates candidate performance against a reference baseline.

```bash
evaluate <reference.json> <candidate.json>
```

Returns exit code 0 if candidate >= reference, exit code 1 otherwise.

### GitHub Actions Workflow

The repository includes a GitHub Actions workflow (`.github/workflows/performance.yml`) that:

1. **On Push to Main**: Runs `compute` and saves the result as an artifact
2. **On Pull Requests**:
   - Runs `compute` on the PR branch (candidate)
   - Runs `compute` on the main branch (baseline)
   - Runs `evaluate` to compare candidate vs baseline

### Installation

```bash
pip install -e .
```

### Development

The package is structured as:
- `perfbench/`: Python package directory
  - `__init__.py`: Package initialization
  - `cli.py`: CLI command implementations
- `pyproject.toml`: Project configuration and dependencies

