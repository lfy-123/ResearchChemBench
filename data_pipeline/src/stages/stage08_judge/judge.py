from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.agents import run_agent
from src.agents.workspace import create_agent_run
from src.core.io import write_json, write_jsonl
from src.core.logging import log_progress, value_counts
from src.stages.stage07_builder.context import materialize_agent_context
from src.stages.stage08_judge.probe import public_input_probe
from src.stages.task_schemas import JUDGE_SCHEMA


def run_judge_stage(
    documents: list[dict[str, Any]],
    asset_result: dict[str, Any],
    builder_result: dict[str, Any],
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
    candidates = [
        item
        for item in builder_result.get("records", [])
        if item.get("status") == "candidate_ready"
    ]
    records: list[dict[str, Any]] = []
    for index, builder in enumerate(candidates, start=1):
        paper_id = str(builder["paper_id"])
        candidate_dir = Path(str(builder["candidate_dir"]))
        task = json.loads((candidate_dir / "candidate_task.json").read_text(encoding="utf-8"))
        task_id = str(task["task_id"])
        task_root = root / task_id
        task_root.mkdir(parents=True, exist_ok=True)
        probe = public_input_probe(candidate_dir)
        write_json(task_root / "public_probe" / "report.json", probe)
        paths = create_agent_run(task_root, "judge")
        materialize_agent_context(
            paths["input"],
            document=document_map[paper_id],
            assets=assets_by_paper.get(paper_id, []),
            toolbox=toolbox,
            extra_files=[
                (candidate_dir, "candidate"),
                (task_root / "public_probe" / "report.json", "public_probe.json"),
            ],
            max_readable_bytes=int(config.get("max_agent_readable_bytes", 50 * 1024**2)),
        )
        prompt = _judge_prompt()
        write_json(
            task_root / "judge_request.json",
            {
                "task_id": task_id,
                "paper_id": paper_id,
                "agent_run": str(paths["run_root"]),
                "schema": JUDGE_SCHEMA,
            },
        )
        agent = run_agent(
            cli_config=config.get("agent", {}),
            paths=paths,
            prompt=prompt,
            response_schema=JUDGE_SCHEMA,
            label=f"judge-{task_id}",
        )
        response = agent.get("parsed_response")
        status = "error"
        if isinstance(response, dict):
            write_json(task_root / "judge_response.json", response)
            write_json(task_root / "audit_report.json", response)
            (task_root / "audit_report.md").write_text(_render_report(response), encoding="utf-8")
            status = str(response["decision"])
        record = {
            "task_id": task_id,
            "paper_id": paper_id,
            "status": status,
            "public_probe": probe,
            "agent_run": {key: value for key, value in agent.items() if key != "parsed_response"},
            "audit_report_path": str(task_root / "audit_report.json") if response else None,
            "error": agent.get("error") if status == "error" else None,
        }
        write_json(task_root / "judge_record.json", record)
        records.append(record)
        log_progress("stage_08_judge", index, len(candidates), task_id, status=status)
    write_jsonl(root / "judge_records.jsonl", records)
    summary = {"tasks": len(records), "statuses": value_counts(item["status"] for item in records)}
    write_json(root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _judge_prompt() -> str:
    return """You are the independent Judge Agent for ResearchChemBench. Work only inside this isolated workspace.
First read input/candidate, input/document_summary.json, input/asset_overview.md, input/toolbox.json,
input/public_probe.json, and response_schema.json. Use the full document and assets only for targeted evidence checks.
Use logical_path to identify archive members and read at most 16 individual asset content files. Do not scan the whole
workspace, inspect opencode.json/work/output, or attempt to access another Agent run.
Audit the candidate for paper fidelity, a non-trivial claim/figure/table target, sufficient public inputs,
toolbox support, answer leakage, machine-computable scoring, ground-truth quality, and resource feasibility.
Reject tasks that only read an existing output, extract a published value, or redraw a figure. Every criticism must
identify concrete fields, files, asset IDs, or evidence.
Do not assume access to the Builder conversation or scratch work. Return pass only when there is no blocking issue;
return revise for repairable candidate defects and reject when the paper/assets cannot support the proposed task.
Return only the required JSON object."""


def _render_report(report: dict[str, Any]) -> str:
    lines = [f"# Judge Audit: {report['decision']}", "", report["summary"], "", "## Checks", ""]
    for name, check in report.get("checks", {}).items():
        lines.append(
            f"- **{name}**: {check.get('status')} - {'; '.join(check.get('evidence', []))}"
        )
    for heading, key in (
        ("Blocking Issues", "blocking_issues"),
        ("Revision Suggestions", "revision_suggestions"),
        ("Residual Risks", "residual_risks"),
    ):
        lines.extend(["", f"## {heading}", ""])
        lines.extend(f"- {item}" for item in report.get(key, []))
    return "\n".join(lines) + "\n"
