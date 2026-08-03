from __future__ import annotations

from pathlib import Path
from typing import Any

from src.assets import run_asset_collection
from src.core.config import normalize_config
from src.core.io import read_json, read_jsonl, write_json, write_jsonl
from src.core.logging import configure_pipeline_logging, pipeline_logger
from src.curation.toolbox import load_toolbox_profile
from src.ingestion.corpus import inventory_corpus
from src.ingestion.grobid import extract_documents_with_grobid, grobid_service
from src.ingestion.grobid_quantities import grobid_quantities_service
from src.ingestion.softcite import softcite_service
from src.screening.resource_limits import assess_resource_limits, resource_limits_summary
from src.screening.software_coverage import assess_software_coverage, software_coverage_summary
from src.tasks import run_builder_stage, run_judge_stage


def run_pipeline(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path).expanduser().resolve()
    raw = read_json(path)
    config = normalize_config(raw, path.parent)
    configure_pipeline_logging(config.get("log_file", Path(config["workspace"]) / "pipeline.log"))
    if (config.get("source") or {}).get("mode") != "corpus":
        raise ValueError("the redesigned pipeline supports corpus mode only")
    return run_corpus_pipeline(path, config, path.parent)


def run_corpus_pipeline(config_path: Path, config: dict[str, Any], base: Path) -> dict[str, Any]:
    workspace = _resolve(base, config.get("workspace", "work"))
    workspace.mkdir(parents=True, exist_ok=True)
    source = config["source"]
    corpus_root = _resolve(base, source["root"])
    _write_stage_index(workspace)

    stage = _stage_dir(workspace, "stage_01_inventory")
    inventory = inventory_corpus(corpus_root)
    exclude_supplementary = bool(source.get("exclude_supplementary", True))
    supplementary_inventory = [
        item for item in inventory if item.get("document_role") == "supplementary"
    ]
    eligible_inventory = [
        item
        for item in inventory
        if not exclude_supplementary or item.get("document_role") != "supplementary"
    ]
    canonical_inventory = [item for item in eligible_inventory if not item.get("duplicate_of")]
    duplicate_inventory = [item for item in inventory if item.get("duplicate_of")]
    write_jsonl(stage / "corpus_inventory.jsonl", inventory)
    write_jsonl(stage / "pdf_paths.jsonl", _pdf_path_rows(inventory, "inventory_status"))
    write_jsonl(
        stage / "canonical_pdf_paths.jsonl", _pdf_path_rows(canonical_inventory, "inventory_status")
    )
    write_jsonl(
        stage / "duplicate_pdf_paths.jsonl", _pdf_path_rows(duplicate_inventory, "inventory_status")
    )
    write_jsonl(
        stage / "supplementary_pdf_paths.jsonl",
        _pdf_path_rows(supplementary_inventory, "document_role"),
    )
    write_jsonl(
        stage / "main_paper_pdf_paths.jsonl",
        _pdf_path_rows(
            [item for item in inventory if item.get("document_role") == "main_paper"],
            "document_role",
        ),
    )
    _write_stage_summary(
        stage,
        {
            "pdf_files": len(inventory),
            "canonical_pdfs": sum(1 for item in inventory if not item.get("duplicate_of")),
            "duplicate_pdfs": len(duplicate_inventory),
            "supplementary_pdfs": len(supplementary_inventory),
            "supplementary_excluded": len(supplementary_inventory) if exclude_supplementary else 0,
            "downstream_main_papers": len(canonical_inventory),
        },
    )

    grobid_config = config.get("grobid_extract", {})
    stage = _stage_dir(workspace, "stage_02_grobid_extract")
    with grobid_service(grobid_config) as client:
        extracted_records = extract_documents_with_grobid(
            canonical_inventory,
            client,
            _resolve(base, grobid_config.get("tei_dir", str(stage / "tei"))),
            _resolve(base, grobid_config.get("text_dir", str(stage / "text"))),
            max_chars=grobid_config.get("max_chars", 2_000_000),
            reuse_existing=grobid_config.get("reuse_existing", True),
            exclude_supplementary=exclude_supplementary,
        )
    write_jsonl(stage / "documents.jsonl", extracted_records)
    _write_stage_summary(
        stage,
        {
            **_field_summary(extracted_records, "grobid_extract_status", "documents"),
            "input_pdf_files": len(inventory),
            "duplicates_excluded": len(duplicate_inventory),
            "supplementary_excluded": len(supplementary_inventory) if exclude_supplementary else 0,
        },
    )
    if config.get("stop_after") == "grobid_extract":
        return _summary(
            config_path, corpus_root, workspace, inventory, stopped_after="grobid_extract"
        )

    toolbox_profile = _load_toolbox(config, base)
    software_config = config.get("software_coverage", {})
    stage = _stage_dir(workspace, "stage_03_software_coverage")
    with softcite_service(software_config) as client:
        software_records = assess_software_coverage(
            extracted_records,
            client,
            toolbox_profile,
            aliases_file=_resolve(base, software_config["aliases_file"]),
            role_rules_file=_resolve(base, software_config["role_rules_file"]),
            capability_map_file=_resolve(base, software_config["capability_map_file"]),
            raw_output_dir=stage / "softcite_raw",
        )
    write_jsonl(stage / "software_coverage_documents.jsonl", software_records)
    write_jsonl(
        stage / "direct_covered_pdf_paths.jsonl",
        _pdf_path_rows(
            [
                item
                for item in software_records
                if (item.get("software_coverage") or {}).get("decision") == "direct_covered"
            ]
        ),
    )
    write_jsonl(
        stage / "capability_equivalent_pdf_paths.jsonl",
        _pdf_path_rows(
            [
                item
                for item in software_records
                if (item.get("software_coverage") or {}).get("decision") == "capability_equivalent"
            ]
        ),
    )
    software_summary = software_coverage_summary(software_records)
    _write_stage_summary(stage, software_summary)
    if config.get("stop_after") == "software_coverage":
        return _summary(
            config_path,
            corpus_root,
            workspace,
            inventory,
            stopped_after="software_coverage",
            stage03=software_summary,
        )

    stage = _stage_dir(workspace, "stage_04_resource_limits")
    resource_inputs = [
        item
        for item in software_records
        if (item.get("software_coverage") or {}).get("decision") == "direct_covered"
    ]
    with grobid_quantities_service(config.get("grobid_quantities", {})) as client:
        classified = assess_resource_limits(
            resource_inputs,
            client,
            config.get("resource_limits", {}),
            config.get("resource_interpretation", {}),
            output_dir=stage,
        )
    write_jsonl(stage / "resource_screened_documents.jsonl", classified)
    write_jsonl(
        stage / "selected_pdf_paths.jsonl",
        _pdf_path_rows(
            [item for item in classified if (item.get("resource_limits") or {}).get("passed")]
        ),
    )
    resource_summary = resource_limits_summary(classified)
    _write_stage_summary(stage, resource_summary)
    if config.get("stop_after") == "resource_limits":
        return _summary(
            config_path,
            corpus_root,
            workspace,
            inventory,
            stopped_after="resource_limits",
            stage03=software_summary,
            stage04=resource_summary,
        )
    classified = [item for item in classified if (item.get("resource_limits") or {}).get("passed")]
    return run_late_stages_records(
        classified,
        config=config,
        base=base,
        workspace=workspace,
        run_metadata={
            "source_mode": "corpus",
            "config": str(config_path),
            "corpus_root": str(corpus_root),
            "pdf_files": len(inventory),
            "stage_03_software_coverage": software_summary,
            "stage_04_resource_limits": resource_summary,
        },
    )


def run_late_stages(
    input_path: str | Path,
    config_path: str | Path,
    workspace_override: str | Path | None = None,
) -> dict[str, Any]:
    config_file = Path(config_path).expanduser().resolve()
    config = normalize_config(read_json(config_file), config_file.parent)
    workspace = (
        Path(workspace_override).expanduser().resolve()
        if workspace_override
        else _resolve(config_file.parent, config["workspace"])
    )
    workspace.mkdir(parents=True, exist_ok=True)
    configure_pipeline_logging(workspace / "pipeline.log")
    _write_stage_index(workspace)
    records = [
        item for item in read_jsonl(input_path) if (item.get("resource_limits") or {}).get("passed")
    ]
    return run_late_stages_records(
        records,
        config=config,
        base=config_file.parent,
        workspace=workspace,
        run_metadata={
            "source_mode": "stage04_reuse",
            "config": str(config_file),
            "input": str(Path(input_path).resolve()),
        },
    )


def run_late_stages_records(
    records: list[dict[str, Any]],
    *,
    config: dict[str, Any],
    base: Path,
    workspace: Path,
    run_metadata: dict[str, Any],
) -> dict[str, Any]:
    toolbox = _load_toolbox(config, base)
    stage05 = _stage_dir(workspace, "stage_05_asset_collection")
    asset_result = run_asset_collection(
        records, stage05, config.get("stage05", {}), config.get("mineru", {})
    )
    _write_stage_summary(stage05, asset_result["summary"])
    if config.get("stop_after") == "asset_collection":
        return {
            **run_metadata,
            "workspace": str(workspace),
            "stopped_after": "asset_collection",
            "stage_05": asset_result["summary"],
        }

    stage06 = _stage_dir(workspace, "stage_06_builder")
    builder_result = run_builder_stage(
        records, asset_result, stage06, config.get("stage06", {}), toolbox
    )
    _write_stage_summary(stage06, builder_result["summary"])
    if any(item.get("status") == "error" for item in builder_result["records"]):
        raise RuntimeError("Stage 06 agent execution failed; inspect stage_06_builder agent logs")
    if config.get("stop_after") == "builder":
        return {
            **run_metadata,
            "workspace": str(workspace),
            "stopped_after": "builder",
            "stage_05": asset_result["summary"],
            "stage_06": builder_result["summary"],
        }

    stage07 = _stage_dir(workspace, "stage_07_judge")
    judge_result = run_judge_stage(
        records, asset_result, builder_result, stage07, config.get("stage07", {}), toolbox
    )
    _write_stage_summary(stage07, judge_result["summary"])
    if any(item.get("status") == "error" for item in judge_result["records"]):
        raise RuntimeError("Stage 07 agent execution failed; inspect stage_07_judge agent logs")
    summary = {
        **run_metadata,
        "workspace": str(workspace),
        "stopped_after": "judge",
        "stage_05": asset_result["summary"],
        "stage_06": builder_result["summary"],
        "stage_07": judge_result["summary"],
    }
    write_json(workspace / "run_summary.json", summary)
    return summary


_STARTED_STAGES: set[str] = set()


def _stage_dir(workspace: Path, name: str) -> Path:
    stage = workspace / name
    stage.mkdir(parents=True, exist_ok=True)
    key = str(stage.resolve())
    if key not in _STARTED_STAGES:
        _STARTED_STAGES.add(key)
        pipeline_logger().info("STAGE START | %s | output=%s", name, stage)
    return stage


def _write_stage_summary(stage: Path, summary: dict[str, Any]) -> None:
    write_json(stage / "summary.json", summary)
    pipeline_logger().info("STAGE COMPLETE | %s | summary=%s", stage.name, summary)


def _write_stage_index(workspace: Path) -> None:
    stages = [
        ("stage_01_inventory", "PDF inventory, roles, hashes, and duplicate detection"),
        ("stage_02_grobid_extract", "GROBID metadata, structure, text, references, and TEI XML"),
        (
            "stage_03_software_coverage",
            "Softcite core-software extraction and toolbox coverage gate",
        ),
        (
            "stage_04_resource_limits",
            "explicit resource normalization and configured hard-limit gate",
        ),
        (
            "stage_05_asset_collection",
            "bounded asset discovery, download, provenance, expansion, and incremental parsing",
        ),
        (
            "stage_06_builder",
            "isolated Builder Agent task construction and deterministic validation",
        ),
        ("stage_07_judge", "isolated Judge Agent audit and final pipeline decision"),
    ]
    write_json(
        workspace / "stage_index.json",
        {
            "output_root": str(workspace),
            "stages": [
                {"order": index, "directory": directory, "description": description}
                for index, (directory, description) in enumerate(stages, 1)
            ],
        },
    )


def _load_toolbox(config: dict[str, Any], base: Path) -> dict[str, Any]:
    toolbox = dict(config.get("toolbox", {}))
    return load_toolbox_profile(_resolve(base, toolbox["profile"]), toolbox)


def _resolve(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def _field_summary(records: list[dict[str, Any]], field: str, count_label: str) -> dict[str, Any]:
    return {count_label: len(records), field: _value_counts(item.get(field) for item in records)}


def _value_counts(values: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = "unknown" if value is None else str(value)
        counts[key] = counts.get(key, 0) + 1
    return counts


def _pdf_path_rows(
    records: list[dict[str, Any]], status_field: str | None = None
) -> list[dict[str, Any]]:
    output = []
    for item in records:
        source_path = item.get("source_path")
        if not source_path:
            continue
        row = {
            "document_id": item.get("document_id"),
            "paper_id": item.get("paper_id"),
            "title": item.get("title"),
            "pdf_path": str(Path(source_path).expanduser().resolve()),
            "relative_path": item.get("relative_path"),
        }
        if status_field:
            row["status"] = item.get(status_field)
        output.append(row)
    return output


def _summary(
    config_path: Path,
    corpus_root: Path,
    workspace: Path,
    inventory: list[dict[str, Any]],
    *,
    stopped_after: str,
    stage03: dict[str, Any] | None = None,
    stage04: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_mode": "corpus",
        "stopped_after": stopped_after,
        "config": str(config_path),
        "corpus_root": str(corpus_root),
        "workspace": str(workspace),
        "pdf_files": len(inventory),
        "stage_03_software_coverage": stage03,
        "stage_04_resource_limits": stage04,
    }
