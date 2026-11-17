"""ApplyPilot AI command-line entry point."""
import sys
from pathlib import Path

# Support running directly from a source checkout.
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from applypilot.cli import main

if __name__ == "__main__":
    main()
