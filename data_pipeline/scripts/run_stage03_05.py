#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from src.core.config import normalize_config
from src.core.io import read_json, read_jsonl, write_json, write_jsonl
from src.core.logging import configure_pipeline_logging, pipeline_logger
from src.curation.toolbox import load_toolbox_profile
from src.ingestion.grobid_quantities import grobid_quantities_service
from src.ingestion.softcite import softcite_service
from src.screening.computation_completeness import (
    assess_computation_completeness,
    computation_completeness_summary,
)
from src.screening.resource_limits import assess_resource_limits, resource_limits_summary
from src.screening.software_coverage import assess_software_coverage, software_coverage_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the redesigned Stage 03-05 gates")
    parser.add_argument("--config", required=True)
    parser.add_argument("--stage2-documents", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    base = config_path.parent
    config = normalize_config(read_json(config_path), base)
    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    configure_pipeline_logging(output_root / "stage_03_05.log")
    documents = _load_documents(args.stage2_documents, args.manifest)
    pipeline_logger().info(
        "STAGE 03-05 START | documents=%d | source=%s | output=%s",
        len(documents),
        Path(args.stage2_documents).resolve(),
        output_root,
    )

    toolbox_config = config["toolbox"]
    toolbox = load_toolbox_profile(toolbox_config["profile"], toolbox_config)

    stage03 = output_root / "stage_03_software_coverage"
    softcite_config = dict(config["software_coverage"])
    softcite_config["service_log"] = str(stage03 / "softcite_service.log")
    with softcite_service(softcite_config) as client:
        software_records = assess_software_coverage(
            documents,
            client,
            toolbox,
            aliases_file=softcite_config["aliases_file"],
            role_rules_file=softcite_config["role_rules_file"],
            capability_map_file=softcite_config["capability_map_file"],
            raw_output_dir=stage03 / "softcite_raw",
        )
    write_jsonl(stage03 / "software_coverage_documents.jsonl", software_records)
    write_jsonl(
        stage03 / "direct_covered_pdf_paths.jsonl",
        _pdf_rows(
            item
            for item in software_records
            if item["software_coverage"]["decision"] == "direct_covered"
        ),
    )
    write_jsonl(
        stage03 / "capability_equivalent_pdf_paths.jsonl",
        _pdf_rows(
            item
            for item in software_records
            if item["software_coverage"]["decision"] == "capability_equivalent"
        ),
    )
    stage03_summary = software_coverage_summary(software_records)
    write_json(stage03 / "summary.json", stage03_summary)

    stage04 = output_root / "stage_04_computation_completeness"
    stage04_inputs = [
        item for item in software_records if item["software_coverage"]["decision"] == "direct_covered"
    ]
    completeness_records = assess_computation_completeness(
        stage04_inputs,
        config["computation_completeness"],
        output_dir=stage04,
    )
    write_jsonl(stage04 / "computation_completeness_documents.jsonl", completeness_records)
    write_jsonl(
        stage04 / "selected_pdf_paths.jsonl",
        _pdf_rows(
            item for item in completeness_records if item["computation_completeness"]["passed"]
        ),
    )
    stage04_summary = computation_completeness_summary(completeness_records)
    write_json(stage04 / "summary.json", stage04_summary)

    stage05 = output_root / "stage_05_resource_limits"
    stage05_inputs = [
        item for item in completeness_records if item["computation_completeness"]["passed"]
    ]
    quantities_config = dict(config["grobid_quantities"])
    quantities_config["service_log"] = str(stage05 / "grobid_quantities.log")
    with grobid_quantities_service(quantities_config) as client:
        resource_records = assess_resource_limits(
            stage05_inputs,
            client,
            config["resource_limits"],
            output_dir=stage05,
        )
    write_jsonl(stage05 / "resource_screened_documents.jsonl", resource_records)
    write_jsonl(
        stage05 / "selected_pdf_paths.jsonl",
        _pdf_rows(item for item in resource_records if item["resource_limits"]["passed"]),
    )
    stage05_summary = resource_limits_summary(resource_records)
    write_json(stage05 / "summary.json", stage05_summary)

    summary = {
        "input_documents": len(documents),
        "stage_03_software_coverage": stage03_summary,
        "stage_04_computation_completeness": stage04_summary,
        "stage_05_resource_limits": stage05_summary,
        "output_root": str(output_root),
    }
    write_json(output_root / "summary.json", summary)
    pipeline_logger().info("STAGE 03-05 COMPLETE | summary=%s", summary)
    return 0


def _load_documents(documents_path: str, manifest_path: str | None) -> list[dict[str, Any]]:
    documents = read_jsonl(Path(documents_path).expanduser().resolve())
    if not manifest_path:
        return documents
    manifest = read_json(Path(manifest_path).expanduser().resolve())
    selected = [str(item["document_id"]) for item in manifest["selected"]]
    by_id = {str(item["document_id"]): item for item in documents}
    missing = [document_id for document_id in selected if document_id not in by_id]
    if missing:
        raise ValueError(f"Stage 02 documents are missing manifest IDs: {', '.join(missing)}")
    return [by_id[document_id] for document_id in selected]


def _pdf_rows(records) -> list[dict[str, Any]]:
    return [
        {
            "document_id": item["document_id"],
            "paper_id": item["paper_id"],
            "title": item.get("title"),
            "pdf_path": str(Path(item["source_path"]).resolve()),
        }
        for item in records
    ]


if __name__ == "__main__":
    raise SystemExit(main())
