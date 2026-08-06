#!/usr/bin/env python3
"""Prepare 1000 grouped remote papers and run the redesigned pipeline through Stage 06."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any

PIPELINE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PYTHON = PIPELINE_ROOT / ".envs" / "researchchem-data-pipeline" / "bin" / "python"
DEFAULT_CREDENTIALS = Path(
    "/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt"
)
DEFAULT_WORK_ROOT = PIPELINE_ROOT / "runs" / "redesigned_stage00_06_1000"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="en-paper-hzzj")
    parser.add_argument("--count", "--limit", type=int, default=1000, dest="count")
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--outside", action="store_true")
    parser.add_argument("--work-root", type=Path, default=DEFAULT_WORK_ROOT)
    parser.add_argument("--config-template", type=Path, default=PIPELINE_ROOT / "config.json")
    parser.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    parser.add_argument("--backend", choices=("sandbox", "local"), default="sandbox")
    parser.add_argument("--sandbox-cpu", type=int, default=128)
    parser.add_argument("--sandbox-memory", default="256Gi")
    parser.add_argument("--sandbox-lifecycle-minutes", type=int, default=1440)
    parser.add_argument("--sandbox-cleanup", choices=("keep", "stop", "delete"), default="stop")
    parser.add_argument("--stage01-workers", type=int, default=32)
    parser.add_argument("--stage02-workers", type=int, default=32)
    parser.add_argument("--stage03-workers", type=int, default=32)
    parser.add_argument("--stage04-workers", type=int, default=16)
    parser.add_argument("--stage05-workers", type=int, default=16)
    parser.add_argument("--stage06-workers", type=int, default=16)
    parser.add_argument("--disable-publisher-network", action="store_true")
    parser.add_argument("--disable-mineru", action="store_true")
    parser.add_argument("--plan-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    for name in (
        "count",
        "sandbox_cpu",
        "stage01_workers",
        "stage02_workers",
        "stage03_workers",
        "stage04_workers",
        "stage05_workers",
        "stage06_workers",
    ):
        if int(getattr(args, name)) < 1:
            raise ValueError(f"{name} must be positive")
    work_root = _pipeline_path(args.work_root)
    template = _pipeline_path(args.config_template)
    python = _pipeline_path(args.python)
    credentials = _pipeline_path(args.credentials)
    for label, path in (
        ("config template", template),
        ("pipeline Python", python),
        ("Xinghe credentials", credentials),
    ):
        if not path.is_file():
            raise FileNotFoundError(f"{label} does not exist: {path}")
    config_path = work_root / "config.stage00-06.json"
    summary_path = work_root / "run_summary.json"
    config = _build_config(args, template, work_root, credentials)
    command = _pipeline_command(args, python, config_path, summary_path)
    plan = {
        "pipeline_schema_version": 2,
        "dataset": args.dataset,
        "papers": args.count,
        "copy_existing_supplementary": True,
        "stages": [f"stage{stage:02d}" for stage in range(7)],
        "stop_after": "stage06",
        "work_root": str(work_root),
        "backend": args.backend,
        "sandbox": {"cpu": args.sandbox_cpu, "memory": args.sandbox_memory},
        "command": command,
    }
    if args.plan_only:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    work_root.mkdir(parents=True, exist_ok=True)
    _write_json(config_path, config)
    _write_json(work_root / "run_plan.json", plan)
    started = time.monotonic()
    subprocess.run(command, cwd=PIPELINE_ROOT, check=True)
    result = json.loads(summary_path.read_text(encoding="utf-8"))
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    _write_json(summary_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _pipeline_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    return (path if path.is_absolute() else PIPELINE_ROOT / path).resolve()


def _build_config(
    args: argparse.Namespace, template: Path, work_root: Path, credentials: Path
) -> dict[str, Any]:
    config = json.loads(template.read_text(encoding="utf-8"))
    config.update(
        {
            "model_cache_directory": str(PIPELINE_ROOT / ".model_cache"),
            "pdf_directory": str(work_root / "stage_00_remote_corpus" / "corpus"),
            "run_directory": str(work_root / "run"),
            "exclude_supplementary": False,
            "stop_after": "stage06",
            "resume_completed_stages": True,
            "stage00_remote_corpus": {
                "enabled": True,
                "dataset": args.dataset,
                "count": args.count,
                "output_directory": str(work_root / "stage_00_remote_corpus"),
                "credentials": str(credentials),
                "outside": bool(args.outside),
                "resume": True,
                "selection": "seeded_sample",
                "seed": 20260806,
                "copy_existing_supplementary": True,
            },
            "stage03_computation_relevance": {
                "use_llm": False,
                "method_ontology": str(PIPELINE_ROOT / "assets/computational_method_ontology.yaml"),
                "evidence_rules": str(PIPELINE_ROOT / "assets/computation_evidence_rules.yaml"),
                "negative_contexts": str(PIPELINE_ROOT / "assets/computation_negative_contexts.yaml"),
                "workers": args.stage03_workers,
            },
            "stage04_supplementary_acquisition": {
                "enabled": True,
                "enable_network": not args.disable_publisher_network,
                "publisher_adapters": ["acs", "rsc", "elsevier", "wiley", "nature", "mdpi"],
                "allowed_extensions": ["pdf"],
                "read_timeout_seconds": 20,
                "connect_timeout_seconds": 15,
                "paper_timeout_seconds": 180,
                "workers": args.stage04_workers,
            },
            "stage05_preliminary_coverage": {
                "capability_catalog": str(PIPELINE_ROOT / "assets/toolbox_capabilities.json"),
                "continue_without_software_name": True,
                "softcite_instances": min(8, args.stage05_workers),
            },
            "stage06_supplementary_extraction": {
                "pdftotext_command": "pdftotext",
                "minimum_text_quality": 60,
                "workers": args.stage06_workers,
            },
        }
    )
    config.setdefault("stage01", {})["workers"] = args.stage01_workers
    grobid = config.setdefault("grobid", {})
    grobid["workers"] = args.stage02_workers
    grobid["reuse_existing"] = True
    grobid["working_directory"] = str(
        _template_path(template, grobid.get("working_directory", "third_party/grobid"))
    )
    softcite = config.setdefault("softcite", {})
    softcite["workers"] = args.stage05_workers
    softcite["working_directory"] = str(
        _template_path(
            template, softcite.get("working_directory", "third_party/software-mentions")
        )
    )
    softcite["delft_directory"] = str(
        _template_path(template, softcite.get("delft_directory", "third_party/delft"))
    )
    for key, default in (
        ("aliases_file", "assets/software_aliases.json"),
        ("role_rules_file", "assets/software_role_rules.json"),
        ("capability_map_file", "assets/software_capability_map.json"),
    ):
        softcite[key] = str(_template_path(template, softcite.get(key, default)))
    config.setdefault("mineru", {})["enabled"] = not args.disable_mineru
    config.setdefault("toolbox", {})["file"] = str(PIPELINE_ROOT / "assets/toolbox.json")
    return config


def _template_path(template: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (template.parent / path).resolve()


def _pipeline_command(
    args: argparse.Namespace, python: Path, config: Path, summary: Path
) -> list[str]:
    command = [
        str(python),
        "-m",
        "src",
        "run",
        "--config",
        str(config),
        "--output",
        str(summary),
        "--execution-backend",
        args.backend,
    ]
    if args.backend == "sandbox":
        command.extend(
            [
                "--sandbox-cpu",
                str(args.sandbox_cpu),
                "--sandbox-memory",
                str(args.sandbox_memory),
                "--sandbox-lifecycle-minutes",
                str(args.sandbox_lifecycle_minutes),
                "--sandbox-cleanup",
                args.sandbox_cleanup,
            ]
        )
    return command


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


if __name__ == "__main__":
    raise SystemExit(main())
