#!/usr/bin/env python3
"""Create-only scaffold for the jinx context standard.

Usage: python3 jinx_context_scaffold.py --root <repo> [--targets codex,claude,kiro,opencode] [--dry-run]

Creates only missing files from ../templates/. Never overwrites, merges, or deletes. Re-running
produces no diff. It infers no architecture, commands, or requirements: the agent must replace every
placeholder with evidence from the target repository.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from jinxcontext.scaffold import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:], TOOLS_DIR))
