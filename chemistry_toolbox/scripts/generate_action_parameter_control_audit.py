#!/usr/bin/env python3
"""Write an English compatibility notice for the retired parameter audit."""

from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = TOOLBOX_ROOT.parent
OUTPUT = REPOSITORY_ROOT / "docs/check/ACTION_PARAMETER_CONTROL_AUDIT.md"
ARCHIVE = (
    REPOSITORY_ROOT
    / "docs/archive/chemistry_toolbox_legacy_cn/scripts/generate_action_parameter_control_audit.py"
)


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "# Archived Legacy Report\n\n"
        "This date-specific report generator was retired when the toolbox adopted an "
        "English-only interface. Its historical source is preserved at "
        f"`{ARCHIVE.relative_to(REPOSITORY_ROOT)}`. Parameter contracts are now "
        "validated directly by the catalog test suite.\n",
        encoding="utf-8",
    )
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
