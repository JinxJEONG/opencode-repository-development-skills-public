#!/usr/bin/env python3
"""Read-only deterministic checker for the jinx context standard.

Usage: python3 jinx_context_check.py --mode project --root <repo>
       python3 jinx_context_check.py --mode package --root <repo> --package skills/<name>

Writes nothing. Standard library only. See ../contract.md for check ids and exit codes.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from jinxcontext.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:], TOOLS_DIR))
