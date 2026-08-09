from __future__ import annotations

from pathlib import Path
from typing import Any

from src.stages.stage00_remote_corpus import prepare_remote_corpus
from src.v2.contracts import record_header, write_json


def run_stage00(config: dict[str, Any], workspace: Path, run_id: str) -> dict[str, Any]:
    stage_root = workspace / "stage_00_remote_corpus"
    if not config.get("enabled", False):
        source_root = config.get("source_root")
        if not source_root:
            raise ValueError("stage00.source_root is required when Stage 00 is disabled")
        result = {
            **record_header(run_id=run_id, stage="stage00"),
            "status": "external_corpus",
            "corpus_root": str(Path(source_root).expanduser().resolve()),
        }
        write_json(stage_root / "stage_summary.json", result)
        return result
    raw = prepare_remote_corpus(
        stage_root,
        dataset=str(config.get("dataset", "en-paper-hzzj")),
        count=int(config.get("count", 1000)),
        credentials=config.get("credentials"),
        outside=bool(config.get("outside", False)),
        resume=bool(config.get("resume", True)),
        copy_supplementary=True,
        selection=str(config.get("selection", "remote_order")),
        seed=int(config.get("seed", 0)),
        exclude_selected_manifests=config.get("exclude_selected_manifests") or [],
    )
    summary = {
        **record_header(run_id=run_id, stage="stage00"),
        "status": "completed",
        "corpus_root": raw["corpus_root"],
        "source_summary": raw["summary"],
    }
    write_json(stage_root / "stage_summary.v2.json", summary)
    return summary
