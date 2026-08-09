from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PIPELINE_CONTRACT = "researchchembench-data-pipeline/v2"
SCHEMA_VERSION = "2.0"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(payload).hexdigest()


def record_header(
    *,
    run_id: str,
    stage: str,
    paper_id: str | None = None,
    document_id: str | None = None,
) -> dict[str, Any]:
    return {
        "pipeline_contract": PIPELINE_CONTRACT,
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "stage": stage,
        "paper_id": paper_id,
        "document_id": document_id,
        "created_at": now_utc(),
    }


def evidence_id(document_id: str, block_index: int, text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"ev_{document_id}_{block_index:06d}_{digest}"


def safe_component(value: str) -> str:
    cleaned = "".join(
        character if character.isalnum() or character in "-_" else "_" for character in value
    )
    return cleaned[:180] or "record"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)


def write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as output:
        for row in rows:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    temporary.replace(target)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    if not source.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with source.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError(f"JSONL row must be an object: {source}")
                rows.append(value)
    return rows


def decision_counts(rows: list[dict[str, Any]], key: str = "decision") -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        decision = str(row.get(key) or "missing")
        counts[decision] = counts.get(decision, 0) + 1
    return dict(sorted(counts.items()))
