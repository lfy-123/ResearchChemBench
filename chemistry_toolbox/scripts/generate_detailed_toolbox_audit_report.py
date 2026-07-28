#!/usr/bin/env python3
"""Write an English compatibility notice for the retired detailed audit."""

from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = TOOLBOX_ROOT / "docs" / "CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md"
ARCHIVE = (
    TOOLBOX_ROOT.parent
    / "docs/archive/chemistry_toolbox_legacy_cn/scripts/generate_detailed_toolbox_audit_report.py"
)


def main() -> int:
    OUTPUT.write_text(
        "# Archived Legacy Report\n\n"
        "This date-specific report generator was retired when the toolbox adopted an "
        "English-only interface. Its historical source is preserved at "
        f"`{ARCHIVE.relative_to(TOOLBOX_ROOT.parent)}`. Use the live inventory, "
        "discovery APIs, and current test results for audits.\n",
        encoding="utf-8",
    )
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
