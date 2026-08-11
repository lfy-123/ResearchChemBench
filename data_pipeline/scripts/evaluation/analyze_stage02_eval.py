#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

LABELS = (
    "computational_content_confirmed",
    "computational_primary_mixed_confirmed",
    "computational_experimental_co_primary_confirmed",
    "experimental_primary_benchmarkable_computation",
    "computational_workflow_not_benchmarkable",
    "computational_content_not_found",
    "uncertain",
)
PASS_LABELS = frozenset(LABELS[:4])
OPERATIONAL_MAP = {"non_original_article": "computational_content_not_found"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze frozen Stage02 challenge-set results.")
    parser.add_argument("--evaluation-root", type=Path, required=True)
    parser.add_argument("--sampling-audit", type=Path)
    parser.add_argument("--reference-dir", default="human_labels_v2")
    parser.add_argument(
        "--reference-adjudications",
        type=Path,
        help="Optional JSONL of consensus adjudications applied after loading reference labels.",
    )
    args = parser.parse_args()

    root = args.evaluation_root.expanduser().resolve()
    manifest = _read_jsonl(root / "manifest.jsonl")
    references = _load_reference_labels(root / args.reference_dir)
    references, adjudicated_ids = _apply_reference_adjudications(
        references,
        args.reference_adjudications.expanduser().resolve()
        if args.reference_adjudications
        else root / "reference_adjudications.jsonl",
    )
    predictions = _by_id(
        _read_jsonl(root / "model_run/stage_02_computational_content/decisions.jsonl")
    )
    expected = {str(row["paper_id"]): row for row in manifest}
    _require_exact_ids("reference labels", expected, references)
    _require_exact_ids("model predictions", expected, predictions)

    sampling = (
        _by_id(_read_jsonl(args.sampling_audit.expanduser().resolve()))
        if args.sampling_audit
        else {}
    )
    rows = []
    for paper_id, item in expected.items():
        reference = references[paper_id]
        prediction = predictions[paper_id]
        reference_label = str(reference["label"])
        raw_prediction = str(prediction.get("decision") or "processing_failed")
        mapped_prediction = OPERATIONAL_MAP.get(raw_prediction, raw_prediction)
        if reference_label not in LABELS:
            raise RuntimeError(f"invalid reference label for {paper_id}: {reference_label}")
        rows.append(
            {
                "eval_id": item["eval_id"],
                "paper_id": paper_id,
                "title": item.get("title"),
                "journal_name": item.get("journal_name"),
                "reference_label": reference_label,
                "prediction": raw_prediction,
                "mapped_prediction": mapped_prediction,
                "reference": reference,
                "model_record": prediction,
                "sampling_stratum": (sampling.get(paper_id) or {}).get("sampling_stratum"),
            }
        )

    result = _metrics(rows)
    result["reference_adjudications"] = {
        "count": len(adjudicated_ids),
        "eval_ids": adjudicated_ids,
    }
    result["model_stage_summary"] = _read_json(
        root / "model_run/stage_02_computational_content/stage_summary.json"
    )
    result["model_run"] = _read_json(root / "model_run_result.json")
    disagreements = [row for row in rows if row["mapped_prediction"] != row["reference_label"]]
    output = root / "analysis"
    output.mkdir(parents=True, exist_ok=True)
    _write_json(output / "metrics.json", result)
    _write_jsonl(output / "disagreements.jsonl", disagreements)
    _write_jsonl(output / "paired_results.jsonl", rows)
    (output / "report.md").write_text(_render_report(result), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    semantic = [row for row in rows if row["mapped_prediction"] in LABELS]
    failures = [row for row in rows if row["mapped_prediction"] not in LABELS]
    matrix = {
        reference: {
            predicted: sum(
                row["reference_label"] == reference and row["mapped_prediction"] == predicted
                for row in semantic
            )
            for predicted in LABELS
        }
        for reference in LABELS
    }
    per_label = {}
    for label in LABELS:
        true_positive = matrix[label][label]
        predicted = sum(matrix[reference][label] for reference in LABELS)
        actual = sum(matrix[label].values())
        precision = _ratio(true_positive, predicted)
        recall = _ratio(true_positive, actual)
        per_label[label] = {
            "support": actual,
            "predicted": predicted,
            "precision": precision,
            "recall": recall,
            "f1": _f1(precision, recall),
        }

    pass_tp = sum(
        row["reference_label"] in PASS_LABELS and row["mapped_prediction"] in PASS_LABELS
        for row in semantic
    )
    pass_fp = sum(
        row["reference_label"] not in PASS_LABELS and row["mapped_prediction"] in PASS_LABELS
        for row in semantic
    )
    pass_fn = sum(
        row["reference_label"] in PASS_LABELS and row["mapped_prediction"] not in PASS_LABELS
        for row in semantic
    )
    pass_tn = len(semantic) - pass_tp - pass_fp - pass_fn
    pass_precision = _ratio(pass_tp, pass_tp + pass_fp)
    pass_recall = _ratio(pass_tp, pass_tp + pass_fn)
    exact = sum(row["reference_label"] == row["mapped_prediction"] for row in semantic)
    return {
        "evaluation_type": "stratified_challenge_set",
        "papers": len(rows),
        "semantic_predictions": len(semantic),
        "operational_failures": len(failures),
        "operational_failure_counts": dict(Counter(row["prediction"] for row in failures)),
        "reference_counts": dict(Counter(row["reference_label"] for row in rows)),
        "prediction_counts_raw": dict(Counter(row["prediction"] for row in rows)),
        "prediction_counts_mapped": dict(Counter(row["mapped_prediction"] for row in rows)),
        "exact_accuracy_on_semantic_predictions": _ratio(exact, len(semantic)),
        "macro_f1_on_semantic_predictions": _mean([per_label[label]["f1"] for label in LABELS]),
        "pass_binary": {
            "true_positive": pass_tp,
            "false_positive": pass_fp,
            "false_negative": pass_fn,
            "true_negative": pass_tn,
            "precision": pass_precision,
            "recall": pass_recall,
            "f1": _f1(pass_precision, pass_recall),
        },
        "hold_rate": _ratio(
            sum(row["mapped_prediction"] == "uncertain" for row in rows), len(rows)
        ),
        "disagreements": len(rows) - exact,
        "confusion_matrix": matrix,
        "per_label": per_label,
        "sampling_strata": dict(
            Counter(row["sampling_stratum"] for row in rows if row["sampling_stratum"])
        ),
    }


def _render_report(result: dict[str, Any]) -> str:
    binary = result["pass_binary"]
    lines = [
        "# Stage02 200-paper challenge-set evaluation",
        "",
        "> This is a deliberately stratified historical challenge set. Its raw rates do not estimate ",
        "> prevalence or end-to-end yield on the remote corpus.",
        "",
        "## Summary",
        "",
        f"- Papers: {result['papers']}",
        f"- Semantic predictions: {result['semantic_predictions']}",
        f"- Operational failures: {result['operational_failures']}",
        f"- Exact seven-class accuracy: {_percent(result['exact_accuracy_on_semantic_predictions'])}",
        f"- Macro F1: {result['macro_f1_on_semantic_predictions']:.3f}",
        f"- Pass precision: {_percent(binary['precision'])}",
        f"- Pass recall: {_percent(binary['recall'])}",
        f"- Pass F1: {binary['f1']:.3f}",
        f"- Hold rate: {_percent(result['hold_rate'])}",
        f"- Disagreements: {result['disagreements']}",
        f"- Runtime: {result['model_run'].get('elapsed_seconds', 0):.1f} seconds",
        f"- Semantic calls: {result['model_stage_summary'].get('model_calls', 0)}",
        "- Successful HTTP attempts: "
        f"{result['model_stage_summary'].get('successful_model_http_requests', 0)}",
        "",
        "## Confusion Matrix",
        "",
        "Rows are independent reference labels; columns are Stage02 predictions.",
        "",
        "| Reference \\ Prediction | " + " | ".join(LABELS) + " |",
        "|---|" + "---:|" * len(LABELS),
    ]
    for reference in LABELS:
        lines.append(
            f"| {reference} | "
            + " | ".join(
                str(result["confusion_matrix"][reference][predicted]) for predicted in LABELS
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Per-label Metrics",
            "",
            "| Label | Support | Precision | Recall | F1 |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for label in LABELS:
        row = result["per_label"][label]
        lines.append(
            f"| {label} | {row['support']} | {row['precision']:.3f} | "
            f"{row['recall']:.3f} | {row['f1']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Detailed paired records and every disagreement are stored beside this report.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_reference_labels(root: Path) -> dict[str, dict[str, Any]]:
    rows = [row for path in sorted(root.glob("labels-part-*.jsonl")) for row in _read_jsonl(path)]
    duplicate_ids = [
        paper_id
        for paper_id, count in Counter(str(row.get("paper_id") or "") for row in rows).items()
        if paper_id and count > 1
    ]
    if duplicate_ids:
        raise RuntimeError(f"duplicate reference paper IDs: {duplicate_ids[:10]}")
    return _by_id(rows)


def _apply_reference_adjudications(
    references: dict[str, dict[str, Any]], path: Path
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if not path.is_file():
        return references, []
    adjudications = _read_jsonl(path)
    duplicate_ids = [
        paper_id
        for paper_id, count in Counter(
            str(row.get("paper_id") or "") for row in adjudications
        ).items()
        if paper_id and count > 1
    ]
    if duplicate_ids:
        raise RuntimeError(f"duplicate adjudication paper IDs: {duplicate_ids[:10]}")
    output = {paper_id: dict(row) for paper_id, row in references.items()}
    applied: list[str] = []
    for adjudication in adjudications:
        paper_id = str(adjudication.get("paper_id") or "")
        if paper_id not in output:
            raise RuntimeError(f"adjudication paper ID is absent from references: {paper_id}")
        label = str(adjudication.get("adjudicated_label") or "")
        if label not in LABELS:
            raise RuntimeError(f"invalid adjudicated label for {paper_id}: {label}")
        reference = dict(output[paper_id])
        reference["independent_label"] = reference["label"]
        reference["label"] = label
        reference["adjudication"] = adjudication
        output[paper_id] = reference
        applied.append(str(adjudication.get("eval_id") or paper_id))
    return output, applied


def _require_exact_ids(
    name: str, expected: dict[str, dict[str, Any]], actual: dict[str, dict[str, Any]]
) -> None:
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    if missing or unexpected:
        raise RuntimeError(
            f"{name} does not match manifest: missing={missing[:10]}, unexpected={unexpected[:10]}"
        )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row["paper_id"]): row for row in rows if row.get("paper_id")}


def _ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _f1(precision: float, recall: float) -> float:
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _percent(value: float) -> str:
    return f"{100 * value:.1f}%"


if __name__ == "__main__":
    raise SystemExit(main())
