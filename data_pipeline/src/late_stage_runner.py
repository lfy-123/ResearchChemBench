from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from src.config import load_config
from src.contracts import canonical_hash, read_jsonl, safe_component, write_json
from src.model_client import RoleModelClient
from src.stages.stage06_task_builder.stage import run_stage06
from src.stages.stage07_task_judge.stage import run_stage07

STAGE_PATHS = {
    "stage02": "stage_02_computational_content/decisions.jsonl",
    "stage03": "stage_03_toolbox_resource_gate/decisions.jsonl",
    "stage04": "stage_04_mineru_deep_normalization/decisions.jsonl",
    "documents": (
        "stage_04_mineru_deep_normalization/deep_normalization/documents.jsonl"
    ),
    "candidates": "stage_05_benchmark_suitability/candidates.jsonl",
    "candidate_audits": "stage_05_benchmark_suitability/candidate_audits.jsonl",
}


def run_stage06_07_from_history(
    *,
    source_run: str | Path,
    output: str | Path,
    config_path: str | Path,
    paper: str,
    harness: str = "codex",
    allow_stage05_review_hints: bool = False,
    include_stage07: bool = True,
) -> dict[str, Any]:
    source_root = Path(source_run).expanduser().resolve()
    output_root = Path(output).expanduser().resolve()
    if not source_root.is_dir():
        raise FileNotFoundError(f"historical run directory does not exist: {source_root}")
    if source_root == output_root or source_root in output_root.parents:
        raise ValueError("output must not be the historical source run or one of its descendants")

    inputs = load_historical_stage_inputs(
        source_root,
        paper=paper,
        allow_stage05_review_hints=allow_stage05_review_hints,
    )
    config = load_config(config_path)
    config["stage06"]["harness"] = harness
    config["stage06"]["converter_harness"] = harness
    config["stage07"]["harness"] = harness
    output_root.mkdir(parents=True, exist_ok=True)
    run_id = (
        f"stage06-07-history-{safe_component(inputs['paper_id'])}-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    )
    write_json(
        output_root / "historical_input_manifest.json",
        {
            "run_id": run_id,
            "source_run": str(source_root),
            "paper_selector": paper,
            "paper_id": inputs["paper_id"],
            "doi": inputs.get("doi"),
            "candidate_source": inputs["candidate_source"],
            "allow_stage05_review_hints": allow_stage05_review_hints,
            "input_hashes": {
                key: canonical_hash(inputs[key])
                for key in ("stage02", "stage03", "stage04", "documents", "candidates")
            },
        },
    )

    builder_model = RoleModelClient(
        role="builder",
        config=config["models"]["builder"],
        cache_root=output_root / "llm_cache",
    )
    review_role = str(config["stage06"].get("scientific_review_model_role") or "builder")
    review_model = (
        builder_model
        if review_role == "builder"
        else RoleModelClient(
            role=review_role,
            config=config["models"][review_role],
            cache_root=output_root / "llm_cache",
        )
    )
    stage06 = run_stage06(
        candidates=inputs["candidates"],
        stage02_records=inputs["stage02"],
        stage03_records=inputs["stage03"],
        stage04_records=inputs["stage04"],
        documents=inputs["documents"],
        config={
            **config["stage06"],
            "toolbox_capabilities": config["stage03"]["toolbox_capabilities"],
        },
        model=builder_model,
        review_model=review_model,
        workspace=output_root,
        run_id=run_id,
    )

    stage07: dict[str, Any] | None = None
    stage07_handoffs = [
        row
        for row in stage06["records"]
        if row.get("decision")
        in {"provisional_constructed", "provisional_not_constructible"}
        and row.get("handoff_ready", True)
    ]
    if include_stage07 and stage07_handoffs:
        judge_model = RoleModelClient(
            role="judge",
            config=config["models"]["judge"],
            cache_root=output_root / "llm_cache",
        )
        stage07 = run_stage07(
            build_records=stage07_handoffs,
            documents=inputs["documents"],
            config={
                **config["stage07"],
                "toolbox_capabilities": config["stage03"]["toolbox_capabilities"],
            },
            model=judge_model,
            workspace=output_root,
            run_id=run_id,
        )

    summary = {
        "run_id": run_id,
        "paper_id": inputs["paper_id"],
        "doi": inputs.get("doi"),
        "harness": harness,
        "candidate_source": inputs["candidate_source"],
        "stage06": stage06["summary"],
        "stage07": stage07["summary"] if stage07 else {"status": "not_run"},
    }
    write_json(output_root / "late_stage_run_summary.json", summary)
    return summary


def load_historical_stage_inputs(
    source_run: str | Path,
    *,
    paper: str,
    allow_stage05_review_hints: bool = False,
) -> dict[str, Any]:
    root = Path(source_run).expanduser().resolve()
    paths_by_key = {
        key: _recursive_paths(root, relative) for key, relative in STAGE_PATHS.items()
    }
    paper_id = (
        paper
        if re.fullmatch(r"paper_[A-Za-z0-9]+", paper.strip())
        else _resolve_paper_id_from_paths(paths_by_key.values(), paper)
    )
    loaded = {
        key: _read_paths_for_paper(paths, paper_id=paper_id)
        for key, paths in paths_by_key.items()
    }
    filtered = {
        key: _latest_rows(
            [row for row in rows if str(row.get("paper_id") or "") == paper_id],
            key_field="document_id" if key == "documents" else "paper_id",
        )
        for key, rows in loaded.items()
        if key not in {"candidates", "candidate_audits"}
    }
    candidates = _deduplicate_rows(
        [
            row
            for row in loaded["candidates"]
            if str(row.get("paper_id") or "") == paper_id
        ]
    )
    candidate_source = "stage05_approved_candidates"
    if not candidates and allow_stage05_review_hints:
        candidates = _deduplicate_rows(
            _review_hint_candidates(loaded["candidate_audits"], paper_id)
        )
        candidate_source = "stage05_model_review_hint"
    if not candidates:
        raise ValueError(
            f"no Stage05 candidate found for {paper!r}; pass "
            "--allow-stage05-review-hints only when intentionally re-evaluating a historical "
            "needs-builder-review candidate"
        )
    for key in ("stage02", "stage03", "stage04", "documents"):
        if not filtered.get(key):
            raise ValueError(f"historical input {key} is missing for paper {paper_id}")
    doi = next(
        (
            row.get("doi")
            for key in ("stage02", "stage03", "documents")
            for row in filtered[key]
            if row.get("doi")
        ),
        None,
    )
    return {
        "paper_id": paper_id,
        "doi": doi,
        "candidate_source": candidate_source,
        "stage02": filtered["stage02"],
        "stage03": filtered["stage03"],
        "stage04": filtered["stage04"],
        "documents": filtered["documents"],
        "candidates": candidates,
    }


def _read_recursive(root: Path, relative: str) -> list[dict[str, Any]]:
    return [row for path in _recursive_paths(root, relative) for row in read_jsonl(path)]


def _recursive_paths(root: Path, relative: str) -> list[Path]:
    """Return every historical JSONL shard without parsing unrelated records."""

    paths: set[Path] = set(root.glob(f"batches/*/microbatches/*/{relative}"))
    paths.update(root.glob(f"batches/*/{relative}"))
    paths.update(root.glob(f"microbatches/*/{relative}"))
    direct = root / relative
    if direct.is_file():
        paths.add(direct)
    return sorted(paths)


def _read_paths_for_paper(
    paths: Iterable[Path], *, paper_id: str
) -> list[dict[str, Any]]:
    """Stream-filter large JSONL shards before decoding their full payloads."""

    output: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if paper_id not in line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(row, dict) and str(row.get("paper_id") or "") == paper_id:
                    output.append(row)
    return output


def _resolve_paper_id_from_paths(
    path_groups: Iterable[Iterable[Path]], selector: str
) -> str:
    normalized = selector.strip().casefold()
    matches: set[str] = set()
    for paths in path_groups:
        for path in paths:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if normalized not in line.casefold():
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(row, dict):
                        continue
                    paper_id = str(row.get("paper_id") or "")
                    doi = str(row.get("doi") or "").casefold()
                    if paper_id == selector or doi == normalized:
                        matches.add(paper_id)
    matches.discard("")
    if not matches:
        raise ValueError(f"paper selector was not found in historical run: {selector}")
    if len(matches) != 1:
        raise ValueError(f"paper selector is ambiguous: {selector} -> {sorted(matches)}")
    return matches.pop()


def _resolve_paper_id(groups: Iterable[list[dict[str, Any]]], selector: str) -> str:
    normalized = selector.strip().casefold()
    matches: set[str] = set()
    for rows in groups:
        for row in rows:
            paper_id = str(row.get("paper_id") or "")
            doi = str(row.get("doi") or "").casefold()
            if paper_id == selector or doi == normalized:
                matches.add(paper_id)
    matches.discard("")
    if not matches:
        raise ValueError(f"paper selector was not found in historical run: {selector}")
    if len(matches) != 1:
        raise ValueError(f"paper selector is ambiguous: {selector} -> {sorted(matches)}")
    return matches.pop()


def _latest_rows(rows: list[dict[str, Any]], *, key_field: str) -> list[dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        key = str(row.get(key_field) or f"row-{index}")
        previous = output.get(key)
        if previous is None or str(row.get("created_at") or "") >= str(
            previous.get("created_at") or ""
        ):
            output[key] = row
    return list(output.values())


def _deduplicate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop byte-equivalent logical records copied into batch and microbatch outputs."""

    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        fingerprint = canonical_hash(row)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        output.append(row)
    return output


def _review_hint_candidates(
    audit_rows: list[dict[str, Any]], paper_id: str
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for audit in audit_rows:
        if str(audit.get("paper_id") or "") != paper_id:
            continue
        response = audit.get("model_response") or {}
        if response.get("decision") not in {"pass", "needs_builder_review"}:
            continue
        for candidate in response.get("candidates") or []:
            output.append(
                {
                    **candidate,
                    "paper_id": paper_id,
                    "stage05_final_decision": audit.get("decision"),
                    "stage05_model_decision": response.get("decision"),
                    "candidate_source": "historical_model_response",
                }
            )
    return output
