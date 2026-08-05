#!/usr/bin/env python3
"""Download and screen a remote Xinghe PDF dataset in disposable Stage 01-04 batches."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Iterable

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORK_ROOT = PIPELINE_ROOT / "runs" / "stage04_batches_10000"
DEFAULT_ENV_PYTHON = PIPELINE_ROOT / ".envs" / "researchchem-data-pipeline" / "bin" / "python"
DEFAULT_CREDENTIALS = Path(
    "/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt"
)
DEFAULT_DOWNLOADER = PIPELINE_ROOT / "scripts" / "xinghe_dataset" / "download_xinghe_batch.py"
DEFAULT_WORKFLOW = PIPELINE_ROOT / "scripts" / "workflows" / "run_stage_01_04_screening.sh"
SCHEMA_VERSION = 2


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="en-paper-hzzj")
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--outside", action="store_true")
    parser.add_argument("--work-root", type=Path, default=DEFAULT_WORK_ROOT)
    parser.add_argument("--config-template", type=Path, default=PIPELINE_ROOT / "config.json")
    parser.add_argument("--python", type=Path, default=DEFAULT_ENV_PYTHON)
    parser.add_argument("--downloader", type=Path, default=DEFAULT_DOWNLOADER)
    parser.add_argument("--workflow", type=Path, default=DEFAULT_WORKFLOW)
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--limit", type=int, default=10_000)
    parser.add_argument("--backend", choices=("sandbox", "local"), default="sandbox")
    parser.add_argument("--sandbox-cpu", type=int, default=128)
    parser.add_argument("--sandbox-memory", default="256Gi")
    parser.add_argument(
        "--sandbox-fallback-resource",
        action="append",
        default=["96:192Gi", "64:128Gi", "32:96Gi"],
        metavar="CPU:MEMORY",
        help="fallback requested when the preferred sandbox cannot be scheduled",
    )
    parser.add_argument("--sandbox-lifecycle-minutes", type=int, default=1440)
    parser.add_argument("--stage01-workers", type=int, default=32)
    parser.add_argument("--stage02-workers", type=int, default=32)
    parser.add_argument("--stage03-workers", type=int, default=16)
    parser.add_argument("--stage04-workers", type=int, default=8)
    parser.add_argument("--min-free-gib", type=float, default=10.0)
    parser.add_argument("--keep-batch-workspaces", action="store_true")
    parser.add_argument("--max-batches", type=int)
    parser.add_argument("--plan-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    for label, value in (
        ("batch size", args.batch_size),
        ("limit", args.limit),
        ("Stage 01 workers", args.stage01_workers),
        ("Stage 02 workers", args.stage02_workers),
        ("Stage 03 workers", args.stage03_workers),
        ("Stage 04 workers", args.stage04_workers),
    ):
        _validate_positive(label, value)
    if args.max_batches is not None:
        _validate_positive("max batches", args.max_batches)
    if args.min_free_gib < 0:
        raise ValueError("min free GiB cannot be negative")

    work_root = args.work_root.expanduser().resolve()
    config_template = args.config_template.expanduser().resolve()
    python = args.python.expanduser().resolve()
    credentials = args.credentials.expanduser().resolve()
    downloader = args.downloader.expanduser().resolve()
    workflow = args.workflow.expanduser().resolve()
    for label, path in (
        ("config template", config_template),
        ("pipeline Python", python),
        ("Xinghe credentials", credentials),
        ("Xinghe downloader", downloader),
        ("Stage 01-04 workflow", workflow),
    ):
        if not path.is_file():
            raise FileNotFoundError(f"{label} does not exist: {path}")
    if work_root == PIPELINE_ROOT or work_root in PIPELINE_ROOT.parents:
        raise ValueError("work root must not be the data pipeline or one of its parents")

    if args.plan_only:
        print(json.dumps(_plan(args, work_root), ensure_ascii=False, indent=2))
        return 0

    work_root.mkdir(parents=True, exist_ok=True)
    state_path = work_root / "batch_state.json"
    state = _load_or_initialize_state(args, work_root, config_template, state_path)
    batches = list(_batch_numbers(args.limit, args.batch_size))
    completed = set(state.get("completed_batches") or [])
    pending = [(number, count) for number, count in batches if str(number) not in completed]
    if args.max_batches is not None:
        pending = pending[: args.max_batches]
    if not pending:
        _refresh_aggregate_manifests(work_root)
        print(json.dumps(_final_status(state, work_root), ensure_ascii=False, indent=2))
        return 0

    sandbox_started = False
    started = time.monotonic()
    try:
        if args.backend == "sandbox":
            _create_sandbox_with_fallback(python, args, state, state_path)
            sandbox_started = True
        for batch_number, count in pending:
            _run_batch(
                batch_number=batch_number,
                count=count,
                work_root=work_root,
                config_template=config_template,
                python=python,
                credentials=credentials,
                downloader=downloader,
                workflow=workflow,
                args=args,
                state=state,
                state_path=state_path,
            )
            _refresh_aggregate_manifests(work_root)
    except KeyboardInterrupt:
        print("batch screening interrupted; completed batches remain resumable", file=sys.stderr)
        return 130
    finally:
        if sandbox_started:
            try:
                _sandbox_command(python, "stop", args)
            except Exception as exc:  # pragma: no cover - external cleanup failure
                print(f"warning: failed to stop managed sandbox: {exc}", file=sys.stderr)

    state["last_invocation_seconds"] = round(time.monotonic() - started, 3)
    _write_json(state_path, state)
    print(json.dumps(_final_status(state, work_root), ensure_ascii=False, indent=2))
    return 0


def _load_or_initialize_state(
    args: argparse.Namespace,
    work_root: Path,
    config_template: Path,
    state_path: Path,
) -> dict[str, Any]:
    expected = {
        "schema_version": SCHEMA_VERSION,
        "dataset": args.dataset,
        "work_root": str(work_root),
        "config_template": str(config_template),
        "limit": args.limit,
        "batch_size": args.batch_size,
    }
    if state_path.is_file():
        state = _read_json(state_path)
        for key, value in expected.items():
            if state.get(key) != value:
                raise RuntimeError(
                    f"existing state has {key}={state.get(key)!r}, requested {value!r}; "
                    "use a different --work-root"
                )
        return state
    state = {
        **expected,
        "completed_batches": [],
        "batches": {},
        "concurrency": {
            "stage01": args.stage01_workers,
            "stage02": args.stage02_workers,
            "stage03": args.stage03_workers,
            "stage04": args.stage04_workers,
        },
        "requested_sandbox": {"cpu": args.sandbox_cpu, "memory": args.sandbox_memory},
    }
    _write_json(state_path, state)
    return state


def _run_batch(
    *,
    batch_number: int,
    count: int,
    work_root: Path,
    config_template: Path,
    python: Path,
    credentials: Path,
    downloader: Path,
    workflow: Path,
    args: argparse.Namespace,
    state: dict[str, Any],
    state_path: Path,
) -> None:
    key = str(batch_number)
    batch_name = f"batch_{batch_number:04d}"
    batch_root = work_root / "workspaces" / batch_name
    input_root = batch_root / "input"
    run_root = batch_root / "run"
    report_root = work_root / "reports" / batch_name
    config_path = batch_root / "config.local.json"
    download_manifest = batch_root / "download_batch_manifest.jsonl"
    started = time.monotonic()
    state.setdefault("batches", {})[key] = {"status": "downloading", "requested": count}
    _write_json(state_path, state)

    input_root.mkdir(parents=True, exist_ok=True)
    _require_space(work_root, 0, args.min_free_gib)
    records = _download_batch(
        count=count,
        input_root=input_root,
        download_manifest=download_manifest,
        download_state=work_root / "download_state",
        python=python,
        downloader=downloader,
        credentials=credentials,
        args=args,
    )
    batch_bytes = sum(int(row.get("size_bytes") or 0) for row in records)
    _require_space(work_root, batch_bytes, args.min_free_gib)
    config = _batch_config(config_template, input_root, run_root, args)
    _write_json(config_path, config)

    state["batches"][key].update(
        {"status": "running", "downloaded": len(records), "batch_bytes": batch_bytes}
    )
    _write_json(state_path, state)
    command = [
        "bash",
        str(workflow),
        "--config",
        str(config_path),
        "--backend",
        args.backend,
        "--sandbox-cpu",
        str(args.sandbox_cpu),
        "--sandbox-memory",
        args.sandbox_memory,
        "--sandbox-lifecycle-minutes",
        str(args.sandbox_lifecycle_minutes),
        "--sandbox-cleanup",
        "keep" if args.backend == "sandbox" else "stop",
        "--output",
        str(batch_root / "run_summary.json"),
    ]
    try:
        subprocess.run(command, cwd=PIPELINE_ROOT, check=True)
        source_by_relative = {
            str(Path(row["local_path"]).resolve().relative_to(input_root.resolve())): row
            for row in records
        }
        retained = _retain_selected_pdfs(
            batch_number=batch_number,
            input_root=input_root,
            outputs=run_root / "outputs",
            retained_root=work_root / "retained_pdfs",
            source_by_relative=source_by_relative,
        )
        _write_batch_report(
            batch_number=batch_number,
            records=records,
            input_root=input_root,
            outputs=run_root / "outputs",
            report_root=report_root,
            retained=retained,
            source_by_relative=source_by_relative,
            elapsed_seconds=time.monotonic() - started,
        )
    except Exception as exc:
        state["batches"][key].update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
        _write_json(state_path, state)
        raise

    state["batches"][key].update(
        {
            "status": "finalizing",
            "retained_pdfs": len(retained),
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }
    )
    _write_json(state_path, state)
    if not args.keep_batch_workspaces:
        _safe_remove_batch(batch_root, work_root / "workspaces")
    completed = set(state.get("completed_batches") or [])
    completed.add(key)
    state["completed_batches"] = sorted(completed, key=int)
    state["batches"][key]["status"] = "complete"
    _write_json(state_path, state)


def _download_batch(
    *,
    count: int,
    input_root: Path,
    download_manifest: Path,
    download_state: Path,
    python: Path,
    downloader: Path,
    credentials: Path,
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    if download_manifest.is_file():
        records = _read_jsonl(download_manifest)
        if len(records) == count and all(Path(row["local_path"]).is_file() for row in records):
            return records

    download_state.mkdir(parents=True, exist_ok=True)
    persistent_manifest = download_state / "download_manifest.jsonl"
    records = _records_for_output(persistent_manifest, input_root)
    remaining = count - len(records)
    if remaining > 0:
        command = [
            str(python),
            str(downloader),
            "--credentials",
            str(credentials),
            "--dataset",
            args.dataset,
            "--count",
            str(remaining),
            "--output",
            str(input_root),
            "--state-directory",
            str(download_state),
        ]
        if args.outside:
            command.append("--outside")
        subprocess.run(command, cwd=PIPELINE_ROOT, check=True)
        records = _records_for_output(persistent_manifest, input_root)
    if len(records) != count:
        raise RuntimeError(
            f"remote dataset produced {len(records)} PDFs for this batch, expected {count}"
        )
    _write_jsonl(download_manifest, records)
    return records


def _records_for_output(manifest: Path, output: Path) -> list[dict[str, Any]]:
    root = output.resolve()
    records: dict[str, dict[str, Any]] = {}
    for row in _read_jsonl(manifest):
        local = Path(str(row.get("local_path") or "")).resolve()
        if root not in local.parents or not local.is_file():
            continue
        records[str(row["remote_uri"])] = {**row, "local_path": str(local)}
    return sorted(records.values(), key=lambda row: str(row["remote_uri"]))


def _batch_config(
    config_template: Path,
    input_root: Path,
    run_root: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    config = _read_json(config_template)
    base = config_template.parent
    config["model_cache_directory"] = str(PIPELINE_ROOT / ".model_cache")
    config["pdf_directory"] = str(input_root)
    config["run_directory"] = str(run_root)
    config["exclude_supplementary"] = True
    config["stop_after"] = "resource_limits"
    config.setdefault("stage01", {})["workers"] = args.stage01_workers

    grobid = config.setdefault("grobid", {})
    grobid["working_directory"] = str(
        _resolve_from(base, grobid.get("working_directory", "third_party/grobid"))
    )
    grobid["workers"] = args.stage02_workers
    grobid.setdefault("reuse_existing", True)

    softcite = config.setdefault("softcite", {})
    softcite["working_directory"] = str(
        _resolve_from(base, softcite.get("working_directory", "third_party/software-mentions"))
    )
    softcite["delft_directory"] = str(
        _resolve_from(base, softcite.get("delft_directory", "third_party/delft"))
    )
    softcite["workers"] = args.stage03_workers
    for field, default in (
        ("aliases_file", "assets/software_aliases.json"),
        ("role_rules_file", "assets/software_role_rules.json"),
        ("capability_map_file", "assets/software_capability_map.json"),
    ):
        softcite[field] = str(_resolve_from(base, softcite.get(field, default)))

    config.setdefault("stage04", {})["workers"] = args.stage04_workers
    quantities = config.setdefault("grobid_quantities", {})
    quantities["working_directory"] = str(
        _resolve_from(base, quantities.get("working_directory", "third_party/grobid-quantities"))
    )
    toolbox = config.setdefault("toolbox", {})
    toolbox["file"] = str(_resolve_from(base, toolbox.get("file", "assets/toolbox.json")))
    return config


def _retain_selected_pdfs(
    *,
    batch_number: int,
    input_root: Path,
    outputs: Path,
    retained_root: Path,
    source_by_relative: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    selected_path = outputs / "stage_04_resource_limits" / "selected_pdf_paths.jsonl"
    if not selected_path.is_file():
        raise RuntimeError(f"Stage 04 selected PDF manifest is missing: {selected_path}")
    retained: list[dict[str, Any]] = []
    for row in _read_jsonl(selected_path):
        batch_pdf = Path(str(row["pdf_path"])).resolve()
        try:
            relative = batch_pdf.relative_to(input_root.resolve())
        except ValueError as exc:
            raise RuntimeError(f"selected PDF is outside the batch input: {batch_pdf}") from exc
        source = source_by_relative.get(str(relative))
        if source is None:
            raise RuntimeError(f"download provenance is missing for selected PDF: {relative}")
        target = retained_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(batch_pdf, target)
        retained.append(
            {
                **row,
                "batch_number": batch_number,
                "relative_path": str(relative),
                "remote_uri": source["remote_uri"],
                "retained_path": str(target.resolve()),
            }
        )
    return retained


def _write_batch_report(
    *,
    batch_number: int,
    records: list[dict[str, Any]],
    input_root: Path,
    outputs: Path,
    report_root: Path,
    retained: list[dict[str, Any]],
    source_by_relative: dict[str, dict[str, Any]],
    elapsed_seconds: float,
) -> None:
    report_root.mkdir(parents=True, exist_ok=True)
    _write_jsonl(report_root / "download_manifest.jsonl", records)
    _write_jsonl(report_root / "retained_manifest.jsonl", retained)
    retained_by_relative = {str(row["relative_path"]): row for row in retained}
    screening = _screening_manifest(outputs, input_root, retained_by_relative, source_by_relative)
    _write_jsonl(report_root / "screening_manifest.jsonl", screening)
    stage_summaries: dict[str, Any] = {}
    for stage in (
        "stage_01_inventory",
        "stage_02_grobid_extract",
        "stage_03_software_coverage",
        "stage_04_resource_limits",
    ):
        summary_path = outputs / stage / "summary.json"
        if not summary_path.is_file():
            raise RuntimeError(f"stage summary is missing: {summary_path}")
        value = _read_json(summary_path)
        stage_summaries[stage] = value
        _write_json(report_root / f"{stage}_summary.json", value)
    pipeline_log = outputs / "pipeline.log"
    if pipeline_log.is_file():
        shutil.copy2(pipeline_log, report_root / "pipeline.log")
    _write_json(
        report_root / "batch_summary.json",
        {
            "schema_version": SCHEMA_VERSION,
            "batch_number": batch_number,
            "downloaded_pdfs": len(records),
            "retained_pdfs": len(retained),
            "elapsed_seconds": round(elapsed_seconds, 3),
            "stage_summaries": stage_summaries,
        },
    )


def _screening_manifest(
    outputs: Path,
    input_root: Path,
    retained: dict[str, dict[str, Any]],
    source_by_relative: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    stage1 = _read_jsonl(outputs / "stage_01_inventory" / "corpus_inventory.jsonl")
    stage2 = _rows_by_source(outputs / "stage_02_grobid_extract" / "documents.jsonl")
    stage3 = _rows_by_source(
        outputs / "stage_03_software_coverage" / "software_coverage_documents.jsonl"
    )
    stage4 = _rows_by_source(
        outputs / "stage_04_resource_limits" / "resource_screened_documents.jsonl"
    )
    rows = []
    for item in stage1:
        copied = Path(str(item["source_path"])).resolve()
        relative = copied.relative_to(input_root.resolve())
        relative_key = str(relative)
        key = str(copied)
        software = stage3.get(key, {}).get("software_coverage") or {}
        resources = stage4.get(key, {}).get("resource_limits") or {}
        kept = retained.get(relative_key)
        source = source_by_relative.get(relative_key) or {}
        rows.append(
            {
                "relative_path": relative_key,
                "remote_uri": source.get("remote_uri"),
                "document_id": item.get("document_id"),
                "document_role": item.get("document_role"),
                "duplicate_of": item.get("duplicate_of"),
                "stage_01": item.get("inventory_status"),
                "stage_02": stage2.get(key, {}).get("grobid_extract_status"),
                "stage_03": software.get("decision"),
                "stage_04": resources.get("decision"),
                "passed_stage_04": bool(resources.get("passed")),
                "retained_path": kept.get("retained_path") if kept else None,
            }
        )
    return rows


def _rows_by_source(path: Path) -> dict[str, dict[str, Any]]:
    return {str(Path(str(row["source_path"])).resolve()): row for row in _read_jsonl(path)}


def _refresh_aggregate_manifests(work_root: Path) -> None:
    retained: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    reports = work_root / "reports"
    if reports.is_dir():
        for report in sorted(reports.glob("batch_*")):
            retained.extend(_read_jsonl(report / "retained_manifest.jsonl"))
            sources.extend(_read_jsonl(report / "download_manifest.jsonl"))
    _write_jsonl(work_root / "retained_manifest.jsonl", retained)
    _write_jsonl(work_root / "source_manifest.jsonl", sources)


def _sandbox_command(python: Path, action: str, args: argparse.Namespace) -> None:
    subprocess.run(
        [
            str(python),
            "-m",
            "src",
            "sandbox",
            action,
            "--sandbox-cpu",
            str(args.sandbox_cpu),
            "--sandbox-memory",
            args.sandbox_memory,
            "--sandbox-lifecycle-minutes",
            str(args.sandbox_lifecycle_minutes),
        ],
        cwd=PIPELINE_ROOT,
        check=True,
    )


def _create_sandbox_with_fallback(
    python: Path,
    args: argparse.Namespace,
    state: dict[str, Any],
    state_path: Path,
) -> None:
    effective = state.get("effective_sandbox") or {}
    candidates: list[tuple[int, str]] = []
    if effective:
        candidates.append((int(effective["cpu"]), str(effective["memory"])))
    else:
        preferred_cpu = int(args.sandbox_cpu)
        candidates.append((preferred_cpu, str(args.sandbox_memory)))
        for value in args.sandbox_fallback_resource:
            cpu_text, separator, memory = str(value).partition(":")
            if not separator or not cpu_text.isdigit() or not memory:
                raise ValueError(
                    f"invalid --sandbox-fallback-resource {value!r}; expected CPU:MEMORY"
                )
            candidate = (int(cpu_text), memory)
            if candidate[0] < preferred_cpu and candidate not in candidates:
                candidates.append(candidate)

    failures = []
    for cpu, memory in candidates:
        args.sandbox_cpu = cpu
        args.sandbox_memory = memory
        print(f"SANDBOX REQUEST | cpu={cpu} | memory={memory}", flush=True)
        try:
            _sandbox_command(python, "create", args)
        except subprocess.CalledProcessError as exc:
            failures.append({"cpu": cpu, "memory": memory, "return_code": exc.returncode})
            _delete_failed_sandbox_pool(python, args)
            continue
        state["effective_sandbox"] = {"cpu": cpu, "memory": memory}
        state["sandbox_failures"] = failures
        _write_json(state_path, state)
        return
    raise RuntimeError(f"none of the requested sandbox resources could be scheduled: {failures}")


def _delete_failed_sandbox_pool(
    python: Path, args: argparse.Namespace
) -> None:  # pragma: no cover - external cleanup
    command = [
        str(python),
        "-m",
        "src",
        "sandbox",
        "delete",
        "--sandbox-cpu",
        str(args.sandbox_cpu),
        "--sandbox-memory",
        args.sandbox_memory,
        "--sandbox-lifecycle-minutes",
        str(args.sandbox_lifecycle_minutes),
        "--delete-environment",
    ]
    subprocess.run(command, cwd=PIPELINE_ROOT, check=False)


def _safe_remove_batch(batch_root: Path, workspaces_root: Path) -> None:
    resolved = batch_root.resolve()
    allowed = workspaces_root.resolve()
    if resolved.parent != allowed or not resolved.name.startswith("batch_"):
        raise RuntimeError(f"refusing to remove unsafe batch path: {resolved}")
    if resolved.is_dir():
        shutil.rmtree(resolved)


def _require_space(work_root: Path, batch_bytes: int, min_free_gib: float) -> None:
    free = shutil.disk_usage(work_root).free
    required = batch_bytes * 2 + int(min_free_gib * 1024**3)
    if free < required:
        raise RuntimeError(
            f"insufficient free space: {free / 1024**3:.1f} GiB available, "
            f"{required / 1024**3:.1f} GiB required"
        )


def _batch_numbers(limit: int, size: int) -> Iterable[tuple[int, int]]:
    for offset in range(0, limit, size):
        yield offset // size + 1, min(size, limit - offset)


def _plan(args: argparse.Namespace, work_root: Path) -> dict[str, Any]:
    return {
        "dataset": args.dataset,
        "limit": args.limit,
        "batch_size": args.batch_size,
        "batches": [
            {"batch_number": number, "papers": count}
            for number, count in _batch_numbers(args.limit, args.batch_size)
        ],
        "sandbox": {
            "preferred": {"cpu": args.sandbox_cpu, "memory": args.sandbox_memory},
            "fallbacks": args.sandbox_fallback_resource,
        },
        "workers": {
            "stage01": args.stage01_workers,
            "stage02": args.stage02_workers,
            "stage03": args.stage03_workers,
            "stage04": args.stage04_workers,
        },
        "work_root": str(work_root),
    }


def _final_status(state: dict[str, Any], work_root: Path) -> dict[str, Any]:
    retained_path = work_root / "retained_manifest.jsonl"
    retained = len(_read_jsonl(retained_path)) if retained_path.is_file() else 0
    total_batches = len(list(_batch_numbers(int(state["limit"]), int(state["batch_size"]))))
    return {
        "status": (
            "complete" if len(state.get("completed_batches") or []) == total_batches else "partial"
        ),
        "completed_batches": state.get("completed_batches") or [],
        "retained_pdfs": retained,
        "work_root": str(work_root),
    }


def _resolve_from(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def _validate_positive(label: str, value: int) -> None:
    if value < 1:
        raise ValueError(f"{label} must be positive")


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(temporary, path)


if __name__ == "__main__":
    raise SystemExit(main())
