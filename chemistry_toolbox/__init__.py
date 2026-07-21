"""Unified source tree for the ResearchChem chemistry toolbox.

When this repository is used directly from a source checkout, expose the
``src`` layout before importing the transport package. Installed wheels and
editable installs already provide the same package path, so this is a no-op
for normal installations.
"""

from __future__ import annotations

import sys
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parent / "src"
if SOURCE_ROOT.is_dir() and str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))
