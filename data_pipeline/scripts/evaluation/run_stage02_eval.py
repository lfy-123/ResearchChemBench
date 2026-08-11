#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

from src.contracts import read_jsonl, write_json
from src.model_client import RoleModelClient
from src.stages.stage02_computational_content.stage import run_stage02


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Stage02 on a frozen evaluation manifest.")
    parser.add_argument("--evaluation-root", type=Path, required=True)
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--worker-state", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=32)
    args = parser.parse_args()

    evaluation_root = args.evaluation_root.expanduser().resolve()
    source_run = args.source_run.expanduser().resolve()
    worker_state = json.loads(args.worker_state.expanduser().resolve().read_text(encoding="utf-8"))
    manifest = read_jsonl(evaluation_root / "manifest.jsonl")
    selected_ids = {str(row["paper_id"]) for row in manifest}
    eval_id_by_paper = {str(row["paper_id"]): str(row["eval_id"]) for row in manifest}
    papers = [
        row
        for row in read_jsonl(source_run / "stage_01_document_preparation/paper_bundles.jsonl")
        if str(row.get("paper_id") or "") in selected_ids
    ]
    for paper in papers:
        paper["eval_id"] = eval_id_by_paper[str(paper["paper_id"])]
    source_documents = {
        str(row["document_id"]): row
        for row in read_jsonl(source_run / "stage_01_document_preparation/documents.jsonl")
    }
    documents = _resolve_frozen_documents(manifest, source_documents)
    if len(papers) != len(selected_ids):
        raise RuntimeError(f"resolved {len(papers)} of {len(selected_ids)} selected papers")

    os.environ["RCB_SCREENING_API_KEY"] = str(worker_state["api_key"])
    model_config: dict[str, Any] = {
        "model": worker_state["model"],
        "base_url": worker_state["base_url"],
        "api_key_env": "RCB_SCREENING_API_KEY",
        "workers": args.workers,
        "cache": True,
        "use_proxy": False,
        "timeout_seconds": 900,
        "retries": 2,
        "max_tokens": 2048,
        "thinking": "disabled",
    }
    stage_config = {
        "workers": args.workers,
        "max_prompt_characters": 36000,
        "excerpt_characters": 1400,
        "max_computational_excerpts": 8,
        "max_experimental_excerpts": 8,
        "max_deterministic_experiment_evidence": 8,
        "classification_max_tokens": 2048,
        "review_max_tokens": 2048,
        "minimum_confidence": 0.85,
        "review_on_conflict": True,
        "review_pass_decisions": True,
    }
    client = RoleModelClient(
        role="screening",
        config=model_config,
        cache_root=evaluation_root / "llm_cache",
    )
    write_json(
        evaluation_root / "stage02_test_config.json",
        {
            "source_run": str(source_run),
            "papers": len(papers),
            "worker_token": worker_state.get("worker_token"),
            "worker_ownership": worker_state.get("worker_ownership"),
            "model": worker_state["model"],
            "base_url": worker_state["base_url"],
            "stage02": stage_config,
        },
    )
    started = time.time()
    result = run_stage02(
        papers=papers,
        documents=documents,
        config=stage_config,
        model=client,
        workspace=evaluation_root / "model_run",
        run_id="stage02-eval-200-20260811-qwen",
    )
    write_json(
        evaluation_root / "model_run_result.json",
        {
            "elapsed_seconds": round(time.time() - started, 3),
            "summary": result["summary"],
        },
    )
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0


def _resolve_frozen_documents(
    manifest: list[dict[str, Any]], source_documents: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for paper in manifest:
        paper_id = str(paper["paper_id"])
        for frozen in paper.get("documents") or []:
            document_id = str(frozen["document_id"])
            source = source_documents.get(document_id)
            if source is None or str(source.get("paper_id") or "") != paper_id:
                raise RuntimeError(f"frozen document {document_id} does not resolve for {paper_id}")
            for path_field, hash_field in (
                ("normalized_markdown_path", "normalized_markdown_sha256"),
                ("content_blocks_path", "content_blocks_sha256"),
            ):
                frozen_path = Path(str(frozen[path_field])).expanduser().resolve()
                source_path = Path(str(source[path_field])).expanduser().resolve()
                if frozen_path != source_path:
                    raise RuntimeError(f"frozen path changed for {document_id}: {path_field}")
                if _sha256(frozen_path) != str(frozen[hash_field]):
                    raise RuntimeError(f"frozen content changed for {document_id}: {path_field}")
            resolved.append(source)
    return resolved


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
