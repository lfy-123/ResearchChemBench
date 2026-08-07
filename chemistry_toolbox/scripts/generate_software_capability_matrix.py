#!/usr/bin/env python3
"""Render the software capability audit from the managed cache index."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chemistry_toolbox.src.environment_layout import resolve_configured_path


INDEX = resolve_configured_path(".software_cache/documentation/index.json")
OUTPUT = TOOLBOX_ROOT / "docs" / "CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md"


def _cell(values: list[str] | None, *, limit: int = 12) -> str:
    items = list(values or [])
    if not items:
        return "—"
    shown = items[:limit]
    text = "<br>".join(f"`{value}`" for value in shown)
    if len(items) > limit:
        text += f"<br>...and {len(items) - limit} more"
    return text


def _plain(value: object) -> str:
    text = str(value or "—").replace("|", "\\|")
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    value = json.loads(INDEX.read_text(encoding="utf-8"))
    records = list(value.get("software") or [])
    public = [item for item in records if item.get("current_validated_actions")]
    candidate = [item for item in records if item.get("candidate_actions")]
    documented = [item for item in records if item.get("official_sources")]
    lines = [
        "# ResearchChemBench Software Capability Expansion Matrix",
        "",
        f"> Generated at `{value.get('generated_at')}` from the local documentation cache by `chemistry_toolbox/scripts/generate_software_capability_matrix.py`.",
        "",
        "## 1. Audit Summary",
        "",
        "| Item | Count |",
        "|---|---:|",
        f"| Software, algorithm, and data-source records | {len(records)} |",
        f"| Records with public Action mappings | {len(public)} |",
        f"| Records with candidate Action extensions | {len(candidate)} |",
        f"| Records with official documentation sources | {len(documented)} |",
        "",
        "Capability status advances through `documented -> installed -> adapted -> validated`. Candidate Actions are not current MCP capabilities.",
        "",
        "## 2. Audited Candidate Extensions",
        "",
        "| Software | Detected versions | Current validated Actions | Candidate Actions | Official sources |",
        "|---|---|---|---|---|",
    ]
    for item in sorted(candidate, key=lambda row: row["software_id"]):
        sources = "<br>".join(
            f"[{source.get('title', 'official')}]({source.get('url')})"
            for source in item.get("official_sources") or []
        ) or "—"
        lines.append(
            "| {name}<br>`{sid}` | {versions} | {current} | {candidates} | {sources} |".format(
                name=_plain(item.get("display_name")),
                sid=item["software_id"],
                versions=_plain(", ".join(item.get("detected_versions") or []) or "unknown"),
                current=_cell(item.get("current_validated_actions")),
                candidates=_cell(item.get("candidate_actions"), limit=20),
                sources=sources,
            )
        )

    lines.extend(
        [
            "",
            "## 3. Complete Software, Algorithm, and Data-Source Inventory",
            "",
            "| ID / Name | Detected versions | Inventory status / Adapter | Current public Actions | Candidate Actions | Local documentation | Notes |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in sorted(records, key=lambda row: row["software_id"]):
        versions = ", ".join(item.get("detected_versions") or []) or "unknown"
        status = f"{item.get('inventory_status') or 'not listed'}<br>{item.get('public_adapter') or 'catalog/backend only'}"
        downloads = len(item.get("downloads") or [])
        errors = len(item.get("download_errors") or [])
        local_documents = item.get("local_documents") or []
        local_available = sum(bool(document.get("available")) for document in local_documents)
        local = (
            f"sources={len(item.get('official_sources') or [])}<br>"
            f"downloads={downloads}<br>local_docs={local_available}/{len(local_documents)}<br>"
            f"errors={errors}"
        )
        lines.append(
            "| `{sid}`<br>{name} | {versions} | {status} | {current} | {candidates} | {local} | {notes} |".format(
                sid=item["software_id"],
                name=_plain(item.get("display_name")),
                versions=_plain(versions),
                status=status,
                current=_cell(item.get("current_validated_actions")),
                candidates=_cell(item.get("candidate_actions")),
                local=local,
                notes=_plain(item.get("notes")),
            )
        )

    lines.extend(
        [
            "",
            "## 4. Interpretation Rules",
            "",
            "- `current_validated_actions` comes from the active `BACKEND_SPECS` and means the capability is present in the public catalog; scientific correctness still requires test evidence.",
            "- `candidate_actions` comes from official capability review and only records planned adaptation targets.",
            "- `runtime_only` means software is installed or cached without a complete ActionSpec, BackendSpec, handler, Artifact contract, and end-to-end test chain.",
            "- Data-source clients, parsing libraries, and workflow frameworks do not automatically become Agent-selectable compute Backends.",
            "- Cached documentation lives under `.software_cache/documentation<software>/<version>/` with SHA-256 and source URL records.",
            "- Package-provided manuals remain in their versioned `.software_cache/installations/<software>/<version>/` locations; the matrix records paths, sizes, and hashes without duplicating large licensed files.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "records": len(records)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
