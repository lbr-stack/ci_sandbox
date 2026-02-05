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
3. **On Merge Queue**: Runs the same evaluation as pull requests

#### Skipping Performance Evaluation

You can skip the performance evaluation for a specific PR by adding the `skip-performance-check` label to the PR. This is useful when:
- You know the performance regression is expected and acceptable
- You're making changes that don't affect performance (e.g., documentation)
- The performance test is flaky or not relevant for the change

**How it works:**
- **For Pull Requests**: Add the `skip-performance-check` label to the PR. The evaluation step will be skipped and will not block merging.
- **For Merge Queue**: The label must be present on the PR before it enters the merge queue. The workflow will check the PR's labels even when running in the merge group context.

When the label is present, the evaluation job still runs but skips the actual performance comparison, allowing the PR to merge even if performance has regressed.

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

