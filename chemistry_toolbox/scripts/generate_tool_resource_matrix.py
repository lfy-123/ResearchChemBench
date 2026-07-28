#!/usr/bin/env python3
"""Write an English compatibility notice for the retired resource matrix."""

from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = TOOLBOX_ROOT / "docs" / "CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md"
ARCHIVE = (
    TOOLBOX_ROOT.parent
    / "docs/archive/chemistry_toolbox_legacy_cn/scripts/generate_tool_resource_matrix.py"
)


def main() -> int:
    OUTPUT.write_text(
        "# Archived Legacy Report\n\n"
        "This date-specific report generator was retired when the toolbox adopted an "
        "English-only interface. Its historical source is preserved at "
        f"`{ARCHIVE.relative_to(TOOLBOX_ROOT.parent)}`. Use the live catalog and "
        "resource validation commands for current information.\n",
        encoding="utf-8",
    )
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
