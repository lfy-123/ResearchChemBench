from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def public_input_probe(candidate_dir: str | Path) -> dict[str, Any]:
    root = Path(candidate_dir).expanduser().resolve()
    errors: list[str] = []
    files: list[dict[str, Any]] = []
    for required in ("candidate_task.json", "task.md", "public_inputs/manifest.json"):
        if not (root / required).is_file():
            errors.append(f"missing {required}")
    manifest_path = root / "public_inputs" / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for item in manifest:
                path = root / str(item.get("path"))
                files.append(
                    {
                        "path": str(item.get("path")),
                        "exists": path.is_file(),
                        "size_bytes": path.stat().st_size if path.is_file() else None,
                    }
                )
                if not path.is_file():
                    errors.append(f"missing public input: {item.get('path')}")
        except Exception as exc:
            errors.append(f"invalid public input manifest: {exc}")
    return {"passed": not errors, "errors": errors, "files": files}
