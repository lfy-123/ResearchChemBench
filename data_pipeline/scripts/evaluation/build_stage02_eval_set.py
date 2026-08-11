#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_RUN = Path("runs/stage00-03-random500-seed20260810")
DEFAULT_CENTRALITY_RUN = Path("runs/stage02-centrality-random500-seed20260810-qwen")
DEFAULT_OUTPUT = Path("runs/stage02-eval-200-20260811")
QUOTAS = {
    "both_no_computation": 40,
    "mixed_confirmed": 45,
    "pure_confirmed": 13,
    "pure_but_contract_uncertain": 20,
    "experimental_primary": 29,
    "mixed_but_contract_uncertain": 30,
    "historical_direction_disagreement": 8,
    "non_original": 3,
    "historical_processing_failed": 12,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a leakage-separated 200-paper Stage02 evaluation manifest."
    )
    parser.add_argument("--source-run", type=Path, default=DEFAULT_SOURCE_RUN)
    parser.add_argument("--centrality-run", type=Path, default=DEFAULT_CENTRALITY_RUN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20260811)
    args = parser.parse_args()

    source = args.source_run.expanduser().resolve()
    centrality = args.centrality_run.expanduser().resolve()
    output = args.output.expanduser().resolve()
    papers = _by_id(_read_jsonl(source / "stage_01_document_preparation/paper_bundles.jsonl"))
    documents = _read_jsonl(source / "stage_01_document_preparation/documents.jsonl")
    old = _by_id(_read_jsonl(source / "stage_02_computational_content/decisions.jsonl"))
    reviewed = _by_id(_read_jsonl(centrality / "stage_02_computational_content/decisions.jsonl"))
    documents_by_paper: dict[str, list[dict[str, Any]]] = {}
    for row in documents:
        if row.get("decision") == "pass":
            documents_by_paper.setdefault(str(row["paper_id"]), []).append(row)

    pools: dict[str, list[str]] = {name: [] for name in QUOTAS}
    for paper_id, paper in papers.items():
        if not _complete_stage01_paper(paper):
            continue
        previous = old.get(paper_id) or {}
        central = reviewed.get(paper_id) or {}
        stratum = _stratum(previous, central)
        if stratum:
            pools[stratum].append(paper_id)

    rng = random.Random(args.seed)
    selected: list[tuple[str, str]] = []
    for stratum, quota in QUOTAS.items():
        candidates = sorted(pools[stratum])
        rng.shuffle(candidates)
        if len(candidates) < quota:
            raise RuntimeError(
                f"stratum {stratum} has {len(candidates)} candidates, requires {quota}"
            )
        selected.extend((paper_id, stratum) for paper_id in candidates[:quota])
    rng.shuffle(selected)

    public_rows: list[dict[str, Any]] = []
    private_rows: list[dict[str, Any]] = []
    for index, (paper_id, stratum) in enumerate(selected, start=1):
        paper = papers[paper_id]
        paper_documents = sorted(
            documents_by_paper.get(paper_id, []),
            key=lambda row: (
                0 if row.get("document_role") == "main_paper" else 1,
                str(row.get("document_id") or ""),
            ),
        )
        if not paper_documents or not all(
            Path(row["normalized_markdown_path"]).is_file()
            and Path(row["content_blocks_path"]).is_file()
            for row in paper_documents
        ):
            raise RuntimeError(f"missing normalized Stage01 assets for {paper_id}")
        public_rows.append(
            {
                "eval_id": f"stage02-eval-{index:04d}",
                "paper_id": paper_id,
                "title": paper.get("title"),
                "doi": paper.get("doi"),
                "journal_name": paper.get("journal_name"),
                "article_url": paper.get("article_url"),
                "documents": [
                    {
                        "document_id": row.get("document_id"),
                        "document_role": row.get("document_role"),
                        "selected_parser": row.get("selected_parser"),
                        "normalized_markdown_path": row.get("normalized_markdown_path"),
                        "normalized_markdown_sha256": _sha256(
                            Path(row["normalized_markdown_path"])
                        ),
                        "content_blocks_path": row.get("content_blocks_path"),
                        "content_blocks_sha256": _sha256(Path(row["content_blocks_path"])),
                        "source_remote_uri": row.get("source_remote_uri"),
                    }
                    for row in paper_documents
                ],
            }
        )
        central_review = (reviewed.get(paper_id) or {}).get("centrality_review") or {}
        private_rows.append(
            {
                "eval_id": f"stage02-eval-{index:04d}",
                "paper_id": paper_id,
                "sampling_stratum": stratum,
                "historical_stage02_decision": (old.get(paper_id) or {}).get("decision"),
                "historical_centrality_decision": (reviewed.get(paper_id) or {}).get("decision"),
                "historical_centrality_verdict": central_review.get("verdict"),
            }
        )

    output.mkdir(parents=True, exist_ok=True)
    _write_jsonl(output / "manifest.jsonl", public_rows)
    _write_jsonl(output / "sampling_audit.private.jsonl", private_rows)
    (output / "annotation_instructions.md").write_text(_annotation_instructions(), encoding="utf-8")
    summary = {
        "schema_version": 2,
        "seed": args.seed,
        "papers": len(public_rows),
        "source_run": str(source),
        "centrality_run": str(centrality),
        "quotas": QUOTAS,
        "available_by_stratum": {name: len(pools[name]) for name in QUOTAS},
        "selected_by_stratum": dict(Counter(row[1] for row in selected)),
        "journals": dict(Counter(row.get("journal_name") or "unknown" for row in public_rows)),
        "annotation_manifest": str(output / "manifest.jsonl"),
        "private_sampling_audit": str(output / "sampling_audit.private.jsonl"),
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _stratum(previous: dict[str, Any], central: dict[str, Any]) -> str | None:
    old_decision = str(previous.get("decision") or "")
    decision = str(central.get("decision") or "")
    verdict = str((central.get("centrality_review") or {}).get("verdict") or "")
    if decision == "non_original_article":
        return "non_original"
    if decision == "processing_failed":
        return "historical_processing_failed"
    if verdict == "computation_led_mixed" and old_decision in {
        "computational_content_not_found",
        "uncertain",
    }:
        return "historical_direction_disagreement"
    if decision == "computational_content_confirmed":
        return "pure_confirmed"
    if decision == "uncertain" and verdict == "pure_computational":
        return "pure_but_contract_uncertain"
    if verdict == "experiment_led_with_computational_support":
        return "experimental_primary"
    if decision == "computational_primary_mixed_confirmed":
        return "mixed_confirmed"
    if decision == "uncertain" and verdict == "computation_led_mixed":
        return "mixed_but_contract_uncertain"
    if (
        decision == "computational_content_not_found"
        and old_decision == "computational_content_not_found"
    ):
        return "both_no_computation"
    return None


def _complete_stage01_paper(row: dict[str, Any]) -> bool:
    if row.get("decision") != "pass" or row.get("main_parse_ok") is not True:
        return False
    if row.get("partial_si_parse"):
        return False
    if row.get("package_status") == "complete_with_si":
        return row.get("supplementary_parse_ok") is True
    return row.get("supplementary_parse_ok") is not False


def _annotation_instructions() -> str:
    return """# Stage02 benchmarkable-computation annotation instructions

Read the main paper and every listed supplementary document. Do not open
`sampling_audit.private.jsonl`, historical Stage02 outputs, or new model outputs.

Stage02 asks whether the paper contains an author-performed, substantive computational-chemistry workflow that
could supply a scientifically meaningful benchmark subtask. Computation need not dominate the paper.

Assign exactly one label:

- `computational_content_confirmed`: original pure computational chemistry; no author physical experiment;
  a complete computation generates a central claim that fails without computation.
- `computational_primary_mixed_confirmed`: authors perform computation and physical experiments, but computation
  generates the primary scientific contribution and experiments validate, constrain, or support it.
- `computational_experimental_co_primary_confirmed`: computation and experiments are comparably indispensable.
- `experimental_primary_benchmarkable_computation`: experiments are primary, but a complete non-trivial
  computational workflow generates a meaningful chemical result.
- `computational_workflow_not_benchmarkable`: computation exists but lacks a meaningful input-calculation-output
  workflow or is incidental/routine processing.
- `computational_content_not_found`: no author-performed computational-chemistry workflow.
- `uncertain`: author attribution or workflow completeness cannot be established.

Do not use paragraph counts or require computation to be central. Record a concise rationale, confidence, the
computation workflow and generated result, author experiments, benchmarkability, and decisive source evidence.
"""


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row["paper_id"]): row for row in rows if row.get("paper_id")}


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8"
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
