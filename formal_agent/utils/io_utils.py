"""I/O utilities for reading/writing files and running external commands."""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Tuple


def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """Save JSON data to a file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def write_text(content: str, file_path: str) -> None:
    """Write text content to a file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_text(file_path: str) -> str:
    """Read text content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def run_lean_check(lean_file: str, working_dir: str = None) -> Tuple[bool, str]:
    """
    Run Lean on a file to check if it compiles.
    
    Args:
        lean_file: Path to the Lean file to check
        working_dir: Working directory for the subprocess
        
    Returns:
        Tuple of (success: bool, output: str)
    """
    try:
        result = subprocess.run(
            ['lake', 'env', 'lean', lean_file],
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Timeout: Lean verification took longer than 60 seconds"
    except Exception as e:
        return False, f"Error running Lean: {str(e)}"

