#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

from src.contracts import read_jsonl, write_json, write_jsonl
from src.model_client import RoleModelClient
from src.stages.stage05_benchmark_suitability.stage import run_stage05


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the Stage05 two-pass API gate.")
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--manual-reference", type=Path)
    parser.add_argument("--env-file", type=Path, default=Path("data_pipeline/config.local.env"))
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--router-model", default="deepseek-v4-flash")
    parser.add_argument("--auditor-model", default="deepseek-v4-pro")
    parser.add_argument("--paper-id", action="append", default=[])
    parser.add_argument("--run-id")
    args = parser.parse_args()

    load_dotenv(args.env_file.expanduser().resolve(), override=False)
    source_run = args.source_run.expanduser().resolve()
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    run_id = args.run_id or output.name

    router_key = os.environ.get("RCB_STAGE05_ROUTER_API_KEY") or os.environ.get(
        "RCB_SUITABILITY_API_KEY"
    )
    if not router_key:
        raise RuntimeError("RCB_STAGE05_ROUTER_API_KEY or RCB_SUITABILITY_API_KEY is required")
    os.environ["RCB_STAGE05_ROUTER_API_KEY"] = router_key
    base_url = os.environ.get("RCB_SUITABILITY_BASE_URL")
    if not base_url:
        raise RuntimeError("RCB_SUITABILITY_BASE_URL is required")
    router_base_url = os.environ.get("RCB_STAGE05_ROUTER_BASE_URL") or base_url

    stage04_root = source_run / "stage_04_mineru_deep_normalization"
    stage04_records = read_jsonl(stage04_root / "decisions.jsonl")
    documents = read_jsonl(stage04_root / "deep_normalization/documents.jsonl")
    eligible_ids = {str(row["paper_id"]) for row in stage04_records if row.get("passed")}
    reference = {
        str(row["paper_id"]): row for row in read_jsonl(args.reference.expanduser().resolve())
    }
    if args.paper_id:
        requested = set(args.paper_id)
        unknown = requested - eligible_ids
        if unknown:
            raise RuntimeError(f"unknown or ineligible --paper-id values: {sorted(unknown)}")
        stage04_records = [row for row in stage04_records if str(row["paper_id"]) in requested]
        documents = [row for row in documents if str(row["paper_id"]) in requested]
        reference = {key: value for key, value in reference.items() if key in requested}
        eligible_ids = requested
    if eligible_ids != set(reference):
        raise RuntimeError(
            f"Stage04/reference mismatch: eligible={len(eligible_ids)}, reference={len(reference)}, "
            f"missing_reference={sorted(eligible_ids - set(reference))}, "
            f"missing_stage04={sorted(set(reference) - eligible_ids)}"
        )

    router = RoleModelClient(
        role="stage05_router",
        config={
            "model": args.router_model,
            "base_url": router_base_url,
            "api_key_env": "RCB_STAGE05_ROUTER_API_KEY",
            "workers": args.workers,
            "cache": True,
            "use_proxy": True,
            "timeout_seconds": 1200,
            "retries": 2,
            "max_tokens": 3072,
            "thinking": "disabled",
        },
        cache_root=output / "model_calls",
    )
    auditor = RoleModelClient(
        role="suitability",
        config={
            "model": args.auditor_model,
            "base_url": base_url,
            "api_key_env": "RCB_SUITABILITY_API_KEY",
            "workers": args.workers,
            "cache": True,
            "use_proxy": True,
            "timeout_seconds": 1200,
            "retries": 2,
            "max_tokens": 16000,
            "thinking": "disabled",
        },
        cache_root=output / "model_calls",
    )
    stage_config = {
        "workers": args.workers,
        "router_candidate_limit": 3,
        "router_index_characters": 60000,
        "router_max_tokens": 3072,
        "auditor_evidence_characters": 90000,
        "auditor_max_tokens": 16000,
        "candidate_limit": 1,
        "contract_retry": True,
    }
    write_json(
        output / "evaluation_config.json",
        {
            "run_id": run_id,
            "source_run": str(source_run),
            "eligible_papers": len(eligible_ids),
            "reference": str(args.reference.expanduser().resolve()),
            "router_model": args.router_model,
            "auditor_model": args.auditor_model,
            "stage05": stage_config,
        },
    )
    started = time.time()
    result = run_stage05(
        stage04_records=stage04_records,
        documents=documents,
        config=stage_config,
        router_model=router,
        auditor_model=auditor,
        workspace=output,
        run_id=run_id,
    )
    elapsed = round(time.time() - started, 3)
    manual = None
    if args.manual_reference:
        manual = {
            str(row["paper_id"]): {**row, "decision": row.get("manual_decision")}
            for row in read_jsonl(args.manual_reference.expanduser().resolve())
        }
    comparison = _compare(result["records"], reference, manual)
    comparison["elapsed_seconds"] = elapsed
    comparison["stage_summary"] = result["summary"]
    rows = comparison.pop("rows")
    write_json(output / "comparison_summary.json", comparison)
    write_jsonl(output / "comparison_rows.jsonl", rows)
    (output / "ANALYSIS_REPORT.md").write_text(
        _markdown_report(comparison, rows),
        encoding="utf-8",
    )
    print(json.dumps(comparison, ensure_ascii=False, indent=2))
    return 0


def _compare(records, reference, manual=None):
    rows = []
    exact = binary = 0
    manual_exact = 0
    confusion = Counter()
    for record in records:
        paper_id = str(record["paper_id"])
        predicted = str(record.get("decision") or "processing_failed")
        expected = str(reference[paper_id]["decision"])
        predicted_forward = predicted in {"pass", "needs_builder_review"}
        expected_forward = expected in {"pass", "needs_builder_review"}
        exact += predicted == expected
        binary += predicted_forward == expected_forward
        confusion[(expected, predicted)] += 1
        manual_expected = str((manual or {}).get(paper_id, {}).get("decision") or "")
        manual_exact += bool(manual_expected and predicted == manual_expected)
        response = record.get("model_response") or {}
        rows.append(
            {
                "paper_id": paper_id,
                "expected_gpt56": expected,
                "predicted": predicted,
                "exact_match": predicted == expected,
                "binary_match": predicted_forward == expected_forward,
                "manual_expected": manual_expected or None,
                "manual_match": predicted == manual_expected if manual_expected else None,
                "blocking_dimensions": response.get("blocking_dimensions") or [],
                "review_dimensions": response.get("review_dimensions") or [],
                "rationale": response.get("rationale") or "",
                "validation_rejections": record.get("validation_rejections") or [],
            }
        )
    count = len(rows)
    forward_metrics = _forward_metrics(rows, "expected_gpt56")
    manual_forward_metrics = _forward_metrics(rows, "manual_expected") if manual else None
    return {
        "papers": count,
        "prediction_counts": dict(Counter(row["predicted"] for row in rows)),
        "reference_counts": dict(Counter(row["expected_gpt56"] for row in rows)),
        "exact_matches": exact,
        "exact_accuracy": round(exact / count, 4) if count else 0,
        "binary_forward_matches": binary,
        "binary_forward_accuracy": round(binary / count, 4) if count else 0,
        "manual_exact_matches": manual_exact if manual else None,
        "forward_metrics": forward_metrics,
        "manual_forward_metrics": manual_forward_metrics,
        "confusion": {
            f"{expected} -> {predicted}": value
            for (expected, predicted), value in sorted(confusion.items())
        },
        "rows": rows,
    }


def _forward_metrics(rows, reference_key):
    forward = {"pass", "needs_builder_review"}
    predicted = {row["paper_id"] for row in rows if row["predicted"] in forward}
    expected = {
        row["paper_id"] for row in rows if str(row.get(reference_key) or "") in forward
    }
    overlap = predicted & expected
    union = predicted | expected
    return {
        "predicted_forward": len(predicted),
        "reference_forward": len(expected),
        "overlap": len(overlap),
        "precision": round(len(overlap) / len(predicted), 4) if predicted else 0,
        "recall": round(len(overlap) / len(expected), 4) if expected else 0,
        "jaccard": round(len(overlap) / len(union), 4) if union else 1,
        "overlap_paper_ids": sorted(overlap),
        "false_positive_paper_ids": sorted(predicted - expected),
        "false_negative_paper_ids": sorted(expected - predicted),
    }


def _markdown_report(summary, rows):
    manual = summary.get("manual_forward_metrics")
    lines = [
        "# Stage05 Two-Pass Evaluation",
        "",
        f"- Papers: {summary['papers']}",
        f"- Runtime: {summary['elapsed_seconds']} seconds",
        f"- Predictions: `{json.dumps(summary['prediction_counts'], ensure_ascii=False)}`",
        f"- GPT-5.6-sol exact agreement: {summary['exact_matches']}/{summary['papers']} "
        f"({summary['exact_accuracy']:.1%})",
        f"- GPT-5.6-sol forward/reject agreement: {summary['binary_forward_matches']}/"
        f"{summary['papers']} ({summary['binary_forward_accuracy']:.1%})",
        f"- GPT-5.6-sol forward overlap: {summary['forward_metrics']['overlap']}/"
        f"{summary['forward_metrics']['reference_forward']}",
        f"- Forward precision/recall/Jaccard: {summary['forward_metrics']['precision']:.1%} / "
        f"{summary['forward_metrics']['recall']:.1%} / "
        f"{summary['forward_metrics']['jaccard']:.1%}",
    ]
    if manual:
        lines.extend(
            [
                f"- Manual full-text forward overlap: {manual['overlap']}/"
                f"{manual['reference_forward']}",
                f"- Manual forward precision/recall/Jaccard: {manual['precision']:.1%} / "
                f"{manual['recall']:.1%} / {manual['jaccard']:.1%}",
            ]
        )
    lines.extend(
        [
            "",
            "| Paper | GPT-5.6-sol | Stage05 | Exact | Blocking/review dimensions |",
            "|---|---|---|---:|---|",
        ]
    )
    for row in rows:
        dimensions = row["blocking_dimensions"] or row["review_dimensions"]
        lines.append(
            f"| `{row['paper_id']}` | {row['expected_gpt56']} | {row['predicted']} | "
            f"{'yes' if row['exact_match'] else 'no'} | {', '.join(dimensions)} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
