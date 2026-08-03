from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from src.agents import run_agent
from src.agents.workspace import create_agent_run
from src.core.io import stable_id, write_json, write_jsonl
from src.core.logging import log_progress, value_counts
from src.tasks.context import materialize_agent_context
from src.tasks.schemas import BUILDER_SCHEMA
from src.tasks.validation import validate_builder_candidate


def run_builder_stage(
    documents: list[dict[str, Any]],
    asset_result: dict[str, Any],
    output_dir: str | Path,
    config: dict[str, Any],
    toolbox: dict[str, Any],
) -> dict[str, Any]:
    root = Path(output_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    document_map = {str(item["paper_id"]): item for item in documents}
    assets_by_paper: dict[str, list[dict[str, Any]]] = {}
    for asset in asset_result.get("assets", []):
        assets_by_paper.setdefault(str(asset["paper_id"]), []).append(asset)
    records: list[dict[str, Any]] = []
    papers = [item for item in asset_result.get("papers", []) if item.get("status") != "failed"]
    for index, paper in enumerate(papers, start=1):
        paper_id = str(paper["paper_id"])
        paper_root = root / paper_id
        paper_root.mkdir(parents=True, exist_ok=True)
        paths = create_agent_run(paper_root, "builder")
        document = document_map[paper_id]
        assets = assets_by_paper.get(paper_id, [])
        materialize_agent_context(
            paths["input"],
            document=document,
            assets=assets,
            toolbox=toolbox,
            max_readable_bytes=int(config.get("max_agent_readable_bytes", 50 * 1024**2)),
        )
        prompt = _builder_prompt()
        write_json(
            paper_root / "builder_request.json",
            {"paper_id": paper_id, "agent_run": str(paths["run_root"]), "schema": BUILDER_SCHEMA},
        )
        agent = run_agent(
            cli_config=config.get("agent", {}),
            paths=paths,
            prompt=prompt,
            response_schema=BUILDER_SCHEMA,
            label=f"builder-{paper_id}",
        )
        response = agent.get("parsed_response")
        record: dict[str, Any] = {
            "paper_id": paper_id,
            "title": document.get("title"),
            "agent_run": {key: value for key, value in agent.items() if key != "parsed_response"},
            "status": "error",
            "candidate_dir": None,
            "validation": None,
        }
        if isinstance(response, dict):
            write_json(paper_root / "builder_response.json", response)
            if response.get("decision") == "abstain":
                record["status"] = "abstain"
                record["abstain_reasons"] = response.get("abstain_reasons", [])
            else:
                validation = validate_builder_candidate(
                    response, assets=assets, document=document, toolbox=toolbox
                )
                record["validation"] = validation
                write_json(paper_root / "validation_report.json", validation)
                if validation["passed"]:
                    candidate_dir = paper_root / "candidate"
                    _materialize_candidate(candidate_dir, paper_id, response, assets)
                    record["status"] = "candidate_ready"
                    record["candidate_dir"] = str(candidate_dir)
                else:
                    record["status"] = "builder_invalid"
        record["error"] = agent.get("error") if record["status"] == "error" else None
        write_json(paper_root / "builder_record.json", record)
        records.append(record)
        log_progress("stage_06_builder", index, len(papers), paper_id, status=record["status"])
    write_jsonl(root / "builder_records.jsonl", records)
    summary = {"papers": len(records), "statuses": value_counts(item["status"] for item in records)}
    write_json(root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _builder_prompt() -> str:
    return """You are the Builder Agent for ResearchChemBench. Work only inside this isolated workspace.
First read input/document_summary.json, input/asset_overview.md, input/toolbox.json, and response_schema.json.
Use input/document.json, input/asset_manifest.jsonl, and input/assets only for targeted evidence checks. Do not scan
the whole workspace, inspect opencode.json/work/output, or read duplicate files without a specific need. Use each
asset's logical_path to distinguish archive members, choose one defensible system, and read at most 12 individual
asset content files.
Build exactly one computational-chemistry agent-evaluation task only when the evidence is sufficient.
The task must use the core software identified by Stage 03, choose only real toolbox actions, cite exact asset IDs,
keep answer-bearing results in hidden_reference, and make the rubric total exactly 100 points.
Public assets must contain all required starting inputs without exposing reference outputs. Do not make an archive
public when it bundles answer-bearing outputs. Select only essential, directly relevant toolbox actions.
Do not invent methods, parameters, files, numerical results, or repository contents. If a defensible standalone task
cannot be built, return decision=abstain and explain the missing evidence. Return only the required JSON object."""


def _materialize_candidate(
    root: Path, paper_id: str, response: dict[str, Any], assets: list[dict[str, Any]]
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    task_id = stable_id("task", paper_id, str((response.get("task") or {}).get("title")), length=16)
    task = {"task_id": task_id, "paper_id": paper_id, **response["task"]}
    write_json(root / "candidate_task.json", task)
    write_json(root / "scientific_record.json", response["scientific_record"])
    write_json(root / "hidden_reference" / "reference.json", response["hidden_reference"])
    write_json(root / "scoring" / "rubric.json", response["scoring_rubric"])
    write_json(root / "evidence_map.json", response["evidence_map"])
    asset_map = {str(item["asset_id"]): item for item in assets}
    manifest = []
    for asset_id in task.get("public_asset_ids", []):
        asset = asset_map[str(asset_id)]
        source = Path(str(asset["original_path"]))
        name = _safe_name(str(asset.get("file_name") or source.name))
        target = root / "public_inputs" / f"{asset_id}_{name}"
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(source, target)
        except OSError:
            shutil.copy2(source, target)
        manifest.append(
            {
                "asset_id": asset_id,
                "path": str(target.relative_to(root)),
                "sha256": asset.get("sha256"),
            }
        )
    write_json(root / "public_inputs" / "manifest.json", manifest)
    (root / "task.md").write_text(_render_task(task), encoding="utf-8")


def _render_task(task: dict[str, Any]) -> str:
    instructions = "\n".join(
        f"{index}. {item}" for index, item in enumerate(task.get("instructions", []), 1)
    )
    deliverables = "\n".join(f"- {item}" for item in task.get("expected_deliverables", []))
    return f"# {task['title']}\n\n## Objective\n\n{task['objective']}\n\n## Instructions\n\n{instructions}\n\n## Deliverables\n\n{deliverables}\n"


def _safe_name(value: str) -> str:
    return "".join(
        character if character.isalnum() or character in "._-" else "_" for character in value
    )[:120]
