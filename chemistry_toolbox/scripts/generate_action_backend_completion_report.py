#!/usr/bin/env python3
"""Generate a compact English audit of the live Action/Backend catalog."""

import sys
from datetime import datetime, timezone
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = TOOLBOX_ROOT / "docs" / "ACTION_BACKEND_COMPLETE_AUDIT_20260721.md"
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, TOOLBOX_ROOT.parent):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.catalog import CATEGORY_LABELS, action_specs, backend_specs


def main() -> int:
    actions = action_specs()
    backends = backend_specs()
    pair_count = sum(len(item.backend_ids) for item in actions.values())
    lines = [
        "# Live Action/Backend Catalog Audit",
        "",
        f"Generated at `{datetime.now(timezone.utc).isoformat()}` from the live catalog.",
        "",
        f"- Actions: {len(actions)}",
        f"- Backends: {len(backends)}",
        f"- Action/Backend pairs: {pair_count}",
        "",
        "## Actions",
        "",
        "| Action | Category | Backends |",
        "|---|---|---|",
    ]
    for action in sorted(actions.values(), key=lambda item: item.id):
        providers = ", ".join(f"`{item}`" for item in action.backend_ids)
        lines.append(
            f"| `{action.id}` | {CATEGORY_LABELS.get(action.category, action.category)} | {providers} |"
        )
    lines.extend(["", "## Backends", "", "| Backend | Action count |", "|---|---:|"])
    for backend in sorted(backends.values(), key=lambda item: item.id):
        lines.append(f"| `{backend.id}` | {len(backend.capabilities)} |")
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "This report is generated from the same immutable catalog used by MCP discovery. "
            "The test suite verifies that every Action id and provider Backend id appears here.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
