"""Verifier that checks Lean 4 proofs."""

from pathlib import Path
import textwrap
import yaml
from formal_agent.utils import write_text, run_lean_check


class Verifier:
    """Verifier that runs Lean on proof candidates."""
    
    def __init__(self, config_path: str = "config/paths.yaml"):
        """Initialize the verifier with configuration."""
        config_file = Path(__file__).parent.parent / config_path
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        self.tmp_check_file = Path(__file__).parent.parent / config['tmp_check_file']
        self.lean_workspace = Path(__file__).parent.parent / config['lean_workspace']
    
    def verify(self, lean_code: str) -> tuple[bool, str]:
        """
        Verify a Lean 4 proof candidate.
        
        Args:
            lean_code: The Lean 4 code to verify
            
        Returns:
            Tuple of (success: bool, log: str)
        """
        # Process and write the candidate to TmpCheck.lean
        processed_code = textwrap.dedent(lean_code).strip()
        write_text(processed_code, str(self.tmp_check_file))
        
        # Run Lean verification
        success, log = run_lean_check(
            str(self.tmp_check_file),
            working_dir=str(self.lean_workspace)
        )
        
        return success, log

