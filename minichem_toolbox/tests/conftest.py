from __future__ import annotations

import sys
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
for path in (TOOLBOX_ROOT / "src",):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
