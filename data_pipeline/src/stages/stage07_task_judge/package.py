"""Assemble an audited pair into the current isolated release layout."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import uuid
from pathlib import Path
from typing import Any

from src.agents.workspace import atomic_commit_tree, make_writable, prepare_clean_directory
from src.contracts import read_json, write_json


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from evaluation.contracts import (  # noqa: E402
    EVALUATION_FILES,
    PackageManifest,
    package_content_hash,
    package_payload_entries,
    validate_task_package,
)


TASK_TYPES = ("autonomous_research", "paper_reproduction")


def _paper_summary(paper_info: dict[str, Any]) -> dict[str, str]:
    return {
        key: str(paper_info.get(key) or "")
        for key in ("title", "doi", "journal", "publication_date")
    }


def _write_manifest(root: Path, *, paper_id: str, task_type: str) -> None:
    entries = package_payload_entries(root)
    write_json(
        root / "package_manifest.json",
        PackageManifest(
            paper_id=paper_id,
            task_type=task_type,
            package_content_sha256=package_content_hash(entries),
            entries=entries,
        ).model_dump(mode="json"),
    )


def _assemble_mode(
    *, pair_root: Path, staging_root: Path, paper_id: str, task_type: str,
    paper_info: dict[str, Any]
) -> dict[str, Any]:
    source = pair_root / task_type
    destination = staging_root / "tasks" / task_type / paper_id
    agent_input = destination / "agent_input"
    evaluation = destination / "evaluation"
    agent_input.mkdir(parents=True)
    evaluation.mkdir()

    for name in ("task.md", "submission_schema.json"):
        shutil.copy2(source / name, agent_input / name)
    source_data = source / "data"
    if source_data.is_dir():
        shutil.copytree(source_data, agent_input / "data")
    else:
        (agent_input / "data").mkdir()
    task_info = read_json(source / "task_info.json")
    task_info["paper_id"] = paper_id
    task_info["task_type"] = task_type
    task_info["paper"] = _paper_summary(paper_info)
    write_json(destination / "task_info.json", task_info)

    evaluator = pair_root / "evaluator_reference" / task_type
    for name in EVALUATION_FILES:
        shutil.copy2(evaluator / name, evaluation / name)
    _write_manifest(destination, paper_id=paper_id, task_type=task_type)
    report = validate_task_package(destination)
    return {
        "paper_id": paper_id,
        "task_type": task_type,
        "status": report.status,
        "findings": report.findings,
        "diagnostics": report.diagnostics,
        "path": str(destination),
        "package_sha256": (
            read_json(destination / "package_manifest.json")["package_content_sha256"]
            if report.status == "passed"
            else ""
        ),
    }


def _copy_paper(*, pair_root: Path, destination: Path, paper_id: str) -> dict[str, Any]:
    source_info = read_json(pair_root / "paper_info.json")
    documents: list[dict[str, Any]] = []
    document_root = destination / "documents"
    document_root.mkdir(parents=True)
    supplement_index = 0
    source_documents = [
        row for row in source_info.get("documents") or [] if isinstance(row, dict)
    ]
    has_explicit_main = any(
        str(row.get("document_type") or "")
        in {"main_paper", "main_article", "paper", "article"}
        for row in source_documents
    )
    for index, row in enumerate(source_documents):
        if not isinstance(row, dict) or not row.get("source_path"):
            continue
        source = Path(str(row["source_path"])).expanduser().resolve()
        if not source.is_file() or source.suffix.casefold() != ".pdf":
            continue
        role = str(row.get("document_type") or "")
        if (
            role in {"main_paper", "main_article", "paper", "article"}
            or (index == 0 and not has_explicit_main)
        ) and not (document_root / "main.pdf").exists():
            name = "main.pdf"
            document_type = "main_article"
        else:
            supplement_index += 1
            name = f"supplementary_{supplement_index:03d}.pdf"
            document_type = "supplementary_information"
        target = document_root / name
        shutil.copy2(source, target)
        documents.append(
            {
                "document_type": document_type,
                "path": f"documents/{name}",
                "original_filename": row.get("original_filename") or source.name,
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
        )
    if not documents or not (document_root / "main.pdf").is_file():
        raise FileNotFoundError("release requires one readable main-article PDF")
    paper_info = {
        "paper_id": paper_id,
        **_paper_summary(source_info),
        "publication_year": (
            int(str(source_info.get("publication_date"))[:4])
            if str(source_info.get("publication_date") or "")[:4].isdigit()
            else None
        ),
        "authors": source_info.get("authors") or [],
        "documents": documents,
    }
    write_json(destination / "paper_info.json", paper_info)
    return paper_info


def assemble_release_pair(
    *, pair_root: Path, release_root: Path, paper_id: str
) -> dict[str, Any]:
    """Validate both task packages privately, then publish the complete paper pair."""

    pair_root = pair_root.resolve()
    release_root = release_root.resolve()
    staging = prepare_clean_directory(
        release_root.parent / f".{release_root.name}-{paper_id}-{uuid.uuid4().hex[:8]}"
    )
    try:
        paper_destination = staging / "papers" / paper_id
        paper_info = _copy_paper(
            pair_root=pair_root, destination=paper_destination, paper_id=paper_id
        )
        reports = {
            task_type: _assemble_mode(
                pair_root=pair_root,
                staging_root=staging,
                paper_id=paper_id,
                task_type=task_type,
                paper_info=paper_info,
            )
            for task_type in TASK_TYPES
        }
        findings = sorted(
            {
                finding
                for report in reports.values()
                for finding in report["findings"]
            }
        )
        if findings:
            return {"status": "failed", "findings": findings, "tasks": reports}

        destinations = [
            (paper_destination, release_root / "papers" / paper_id),
            *[
                (
                    staging / "tasks" / task_type / paper_id,
                    release_root / "tasks" / task_type / paper_id,
                )
                for task_type in TASK_TYPES
            ],
        ]
        for source, destination in destinations:
            atomic_commit_tree(source, destination)
        for report in reports.values():
            report["path"] = str(
                release_root / "tasks" / report["task_type"] / paper_id
            )
        return {
            "status": "passed",
            "findings": [],
            "paper_path": str(release_root / "papers" / paper_id),
            "tasks": reports,
        }
    finally:
        if staging.exists():
            make_writable(staging)
            shutil.rmtree(staging)


def write_release_manifest(
    *, release_root: Path, run_id: str, records: list[dict[str, Any]]
) -> None:
    published = [row for row in records if row.get("publish_ready")]
    papers = [
        {"paper_id": row["paper_id"], "path": f"papers/{row['paper_id']}"}
        for row in published
    ]
    tasks = []
    for row in published:
        for task_type in TASK_TYPES:
            report = (row.get("release_report") or {}).get("tasks", {}).get(task_type, {})
            tasks.append(
                {
                    "paper_id": row["paper_id"],
                    "task_type": task_type,
                    "path": f"tasks/{task_type}/{row['paper_id']}",
                    "package_sha256": report.get("package_sha256", ""),
                }
            )
    write_json(
        release_root / "release_manifest.json",
        {
            "release_id": run_id,
            "source_run_id": run_id,
            "papers": papers,
            "tasks": tasks,
        },
    )


__all__ = ["TASK_TYPES", "assemble_release_pair", "write_release_manifest"]
