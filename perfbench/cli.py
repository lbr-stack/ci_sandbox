"""CLI commands for performance benchmarking."""

import json
import random
import time
from pathlib import Path

import typer

try:
    from git import Repo
except ImportError:
    Repo = None


def compute():
    """
    Compute performance metrics and output to JSON.
    Includes a 30-second sleep to simulate a long-running job.
    """
    typer.echo("Computing performance metrics...")
    
    # Simulate long-running computation
    time.sleep(180)
    
    # Generate dummy performance value
    performance_value = 1.
    
    # Get git hash if available
    git_hash = None
    if Repo is not None:
        try:
            repo = Repo(search_parent_directories=True)
            git_hash = repo.head.commit.hexsha
        except Exception:
            pass

    performance_value = 3
    
    result = {
        "performance": performance_value,
        "timestamp": time.time(),
        "status": "completed",
        "git_hash": git_hash
    }
    
    # Output JSON
    output_path = Path("performance_result.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    typer.echo(f"Performance metrics saved to {output_path}")
    typer.echo(f"Performance value: {performance_value:.4f}")
    if git_hash:
        typer.echo(f"Git hash: {git_hash}")


def compute_main():
    """Entry point for compute CLI."""
    typer.run(compute)


def evaluate(ref: str, candidate: str):
    """
    Evaluate candidate performance against reference baseline.
    
    Args:
        ref: Path to reference/baseline JSON file
        candidate: Path to candidate JSON file
    """
    typer.echo(f"Evaluating candidate against reference...")
    typer.echo(f"Reference: {ref}")
    typer.echo(f"Candidate: {candidate}")
    
    # Load reference data
    ref_path = Path(ref)
    if not ref_path.exists():
        typer.echo(f"Error: Reference file not found: {ref}", err=True)
        raise typer.Exit(code=1)
    
    with open(ref_path, "r") as f:
        ref_data = json.load(f)
    
    # Load candidate data
    candidate_path = Path(candidate)
    if not candidate_path.exists():
        typer.echo(f"Error: Candidate file not found: {candidate}", err=True)
        raise typer.Exit(code=1)
    
    with open(candidate_path, "r") as f:
        candidate_data = json.load(f)
    
    # Compare performance values
    ref_perf = ref_data.get("performance", 0)
    candidate_perf = candidate_data.get("performance", 0)
    
    difference = candidate_perf - ref_perf
    percent_change = (difference / ref_perf * 100) if ref_perf != 0 else 0
    
    typer.echo("\n" + "="*50)
    typer.echo("EVALUATION RESULTS")
    typer.echo("="*50)
    typer.echo(f"Reference performance:  {ref_perf:.4f}")
    typer.echo(f"Candidate performance:  {candidate_perf:.4f}")
    typer.echo(f"Difference:             {difference:+.4f}")
    typer.echo(f"Percent change:         {percent_change:+.2f}%")
    typer.echo("="*50)
    
    if candidate_perf >= ref_perf:
        typer.echo("✓ Candidate performance is better or equal to reference!")
    else:
        typer.echo("✗ Candidate performance is worse than reference.")
        raise typer.Exit(code=1)


def evaluate_main():
    """Entry point for evaluate CLI."""
    typer.run(evaluate)
