#!/usr/bin/env python3
"""Build metadata-only manifests for an operator-supplied VASP POTCAR library.

The POTCAR files remain under ``.software_cache`` and are never copied into Git.
Each directory name is exposed as an exact selection key so the benchmark Agent,
not this importer, chooses the potential variant for every chemical element.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
DEFAULT_LIBRARY_ROOT = ROOT / ".software_cache" / "vasp" / "potcars" / "potpaw54"
DEFAULT_OUTPUT_DIRECTORY = TOOLBOX_ROOT / "config" / "vasp_potcar_manifests"
ELEMENT_PREFIX = re.compile(r"^([A-Z][a-z]?)")


FAMILIES: tuple[dict[str, Any], ...] = (
    {
        "id": "vasp_uspp_lda_legacy",
        "relative_root": "pot/USPP_LDA",
        "expected_count": 102,
    },
    {
        "id": "vasp_uspp_gga_legacy",
        "relative_root": "pot_GGA/USPP_GGA",
        "expected_count": 8,
    },
    {
        "id": "vasp_paw_lda_54",
        "relative_root": "potpaw/PAW_LDA",
        "expected_count": 316,
    },
    {
        "id": "vasp_paw_pw91_54",
        "relative_root": "potpaw_GGA/PAW_GGA_PW91",
        "expected_count": 5,
    },
    {
        "id": "vasp_paw_pbe_54",
        "relative_root": "potpaw_PBE/PAW_GGA_PBE",
        "expected_count": 304,
    },
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def family_manifest(library_root: Path, family: dict[str, Any]) -> dict[str, Any]:
    family_root = library_root / str(family["relative_root"])
    if not family_root.is_dir():
        raise FileNotFoundError(f"Missing POTCAR family directory: {family_root}")

    records: dict[str, dict[str, Any]] = {}
    ignored_family_files: list[str] = []
    for path in sorted(family_root.rglob("POTCAR")):
        if not path.is_file():
            continue
        relative = path.relative_to(family_root)
        if len(relative.parts) < 2:
            ignored_family_files.append(relative.as_posix())
            continue
        selection = relative.parts[0]
        if selection in records:
            raise ValueError(
                f"POTCAR family {family['id']} has more than one file for selection "
                f"{selection!r}"
            )
        match = ELEMENT_PREFIX.match(selection)
        if match is None:
            raise ValueError(
                f"Cannot infer the chemical element for POTCAR selection {selection!r}"
            )
        records[selection] = {
            "element": match.group(1),
            "relative_path": relative.as_posix(),
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
        }

    expected = int(family["expected_count"])
    if len(records) != expected:
        raise ValueError(
            f"POTCAR family {family['id']} expected {expected} selectable variants, "
            f"found {len(records)}"
        )
    return {
        "schema_version": 1,
        "resource_id": family["id"],
        "selection_policy": "agent_explicit_no_default",
        "family_root": str(family["relative_root"]),
        "variant_count": len(records),
        "ignored_family_files": ignored_family_files,
        "variants": dict(sorted(records.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_LIBRARY_ROOT)
    parser.add_argument(
        "--output-directory", type=Path, default=DEFAULT_OUTPUT_DIRECTORY
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify that existing manifests match the cached POTCAR files.",
    )
    args = parser.parse_args()

    library_root = args.root.expanduser().resolve()
    output_directory = args.output_directory.expanduser().resolve()
    generated: dict[str, dict[str, Any]] = {
        str(family["id"]): family_manifest(library_root, family)
        for family in FAMILIES
    }

    errors: list[str] = []
    if not args.check:
        output_directory.mkdir(parents=True, exist_ok=True)
    for resource_id, payload in generated.items():
        path = output_directory / f"{resource_id}.json"
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                errors.append(str(path))
        else:
            path.write_text(text, encoding="utf-8")

    summary = {
        "family_count": len(generated),
        "variant_count": sum(item["variant_count"] for item in generated.values()),
        "mode": "check" if args.check else "write",
        "mismatched_manifests": errors,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
