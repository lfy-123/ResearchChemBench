"""Make a pip-freeze inventory relocatable with the managed cache layout."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PROJECT_EDITABLE_NAMES = {"researchchem_mcp_tools", "researchchembench"}
CACHE_PATH = re.compile(r"\$\{PROJECT_ROOT\}/(\.software_cache/[^#\s]+)")


def _translate_project_cache_path(value: str) -> str:
    from chemistry_toolbox.software_management.legacy_layout import (
        translate_project_cache_path,
    )

    return translate_project_cache_path(value)


def normalize_pip_freeze(text: str, *, project_root: str) -> str:
    """Replace host-specific project and legacy cache paths."""

    output: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.replace(project_root, "${PROJECT_ROOT}")
        editable = re.search(r"#egg=([A-Za-z0-9_.-]+)$", line)
        if line.startswith("-e ") and editable:
            name = editable.group(1).replace("-", "_").lower()
            if name in PROJECT_EDITABLE_NAMES:
                line = "-e ${PROJECT_ROOT}"
        elif line == "-e ${PROJECT_ROOT}/chemistry_toolbox":
            line = "-e ${PROJECT_ROOT}"

        def portable_cache_path(match: re.Match[str]) -> str:
            return "${PROJECT_ROOT}/" + _translate_project_cache_path(match.group(1))

        output.append(CACHE_PATH.sub(portable_cache_path, line))
    return "\n".join(output) + ("\n" if text else "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    sys.stdout.write(
        normalize_pip_freeze(sys.stdin.read(), project_root=args.project_root)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
