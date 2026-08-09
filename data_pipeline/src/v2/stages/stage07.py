from __future__ import annotations

import json
import shlex
import subprocess
import time
from pathlib import Path

from src.core.concurrency import ordered_parallel_map
from src.v2.contracts import (
    read_json,
    read_jsonl,
    record_header,
    safe_component,
    write_json,
    write_jsonl,
)
from src.v2.prompts import STAGE07_SYSTEM, STAGE07_VERSION


def run_stage07(*, build_records, documents, config, model, workspace: Path, run_id: str):
    stage_root = workspace / "stage_07_task_judge"
    eligible = [row for row in build_records if row.get("passed")]
    evidence_by_id = {
        block["evidence_id"]: block
        for document in documents
        if document.get("decision") == "pass"
        for block in read_jsonl(document["content_blocks_path"])
    }

    def judge(record):
        paper_id = record["paper_id"]
        task_pair_id = record["task_pair_id"]
        try:
            pair = _load_pair(Path(record["task_pair_path"]))
            deterministic = deterministic_judge_audit(pair)
            if not deterministic["passed"]:
                decision, response, audit = (
                    "reject",
                    {"decision": "reject", "findings": deterministic["findings"]},
                    None,
                )
            else:
                response, audit = model.call_json(
                    namespace="stage07_judge",
                    record_id=task_pair_id,
                    prompt_version=STAGE07_VERSION,
                    system_prompt=STAGE07_SYSTEM,
                    user_content=json.dumps(
                        {
                            "task_pair": pair,
                            "deterministic_audit": deterministic,
                            "source_evidence_blocks": [
                                evidence_by_id[evidence_id]
                                for evidence_id in _evidence_ids(pair.get("evidence_map"))
                                if evidence_id in evidence_by_id
                            ],
                        },
                        ensure_ascii=False,
                    ),
                    max_tokens=int(config.get("max_tokens", 4096)),
                )
                decision = str(response.get("decision") or "judge_error")
                if decision not in {"pass", "revise", "reject"}:
                    raise ValueError(f"invalid Judge decision: {decision}")
            gold = run_gold(record, config.get("gold_run") or {}, stage_root)
            benchmark_ready = decision == "pass" and gold["status"] == "pass"
            target = stage_root / safe_component(task_pair_id)
            write_json(target / "deterministic_audit.json", deterministic)
            write_json(target / "judge_response.json", {"response": response, "audit": audit})
            write_json(target / "gold_run" / "manifest.json", gold)
            release = {
                **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
                "task_pair_id": task_pair_id,
                "processing_status": "completed",
                "decision": decision,
                "judge_passed": decision == "pass",
                "gold_run_status": gold["status"],
                "benchmark_ready": benchmark_ready,
                "judge_response": response,
                "model_audit": audit,
            }
            write_json(target / "release_decision.json", release)
            return release
        except Exception as exc:
            return {
                **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
                "task_pair_id": task_pair_id,
                "processing_status": "failed",
                "decision": "judge_error",
                "judge_passed": False,
                "gold_run_status": "not_run",
                "benchmark_ready": False,
                "error": {"error_type": type(exc).__name__, "message": str(exc)},
            }

    records = ordered_parallel_map(
        judge, eligible, max_workers=int(config.get("workers", model.config.get("workers", 1)))
    )
    write_jsonl(stage_root / "release_decisions.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage07"),
        "task_pairs": len(records),
        "judge_passed": sum(row.get("judge_passed", False) for row in records),
        "benchmark_ready": sum(row.get("benchmark_ready", False) for row in records),
        "model_role": model.role,
        "model": model.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def deterministic_judge_audit(pair):
    findings = []
    for mode in ("autonomous", "reproduction"):
        if not pair.get(mode, {}).get("task_info") or not pair.get(mode, {}).get("task_markdown"):
            findings.append(f"{mode}_incomplete")
    if (
        not pair.get("scientific_record")
        or not pair.get("hidden_reference")
        or not pair.get("evidence_map")
    ):
        findings.append("shared_record_incomplete")
    return {"passed": not findings, "findings": findings}


def run_gold(record, config, stage_root):
    if not config.get("enabled", False):
        return {"status": "not_run", "reason": "gold_run_disabled"}
    command_template = config.get("command")
    if not command_template:
        return {"status": "not_run", "reason": "gold_run_command_missing"}
    values = {"task_pair_path": record["task_pair_path"], "task_pair_id": record["task_pair_id"]}
    command = [
        str(value).format(**values)
        for value in (
            shlex.split(command_template) if isinstance(command_template, str) else command_template
        )
    ]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=int(config.get("timeout_seconds", 21600)),
        check=False,
    )
    trace_root = stage_root / safe_component(record["task_pair_id"]) / "gold_run"
    trace_root.mkdir(parents=True, exist_ok=True)
    (trace_root / "stdout.log").write_text(completed.stdout, encoding="utf-8")
    (trace_root / "stderr.log").write_text(completed.stderr, encoding="utf-8")
    return {
        "status": "pass" if completed.returncode == 0 else "fail",
        "return_code": completed.returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "command": command,
    }


def _load_pair(root):
    output = {
        "scientific_record": read_json(root / "shared" / "scientific_record.json"),
        "hidden_reference": read_json(root / "shared" / "hidden_reference.json"),
        "evidence_map": read_json(root / "evidence_map.json"),
    }
    for mode in ("autonomous", "reproduction"):
        output[mode] = {
            "task_info": read_json(root / mode / "task_info.json"),
            "task_markdown": (root / mode / "task.md").read_text(encoding="utf-8"),
        }
    return output


def _evidence_ids(value):
    output = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "evidence_id" and isinstance(item, str):
                output.add(item)
            elif key == "evidence_ids" and isinstance(item, list):
                output.update(str(entry) for entry in item)
            else:
                output.update(_evidence_ids(item))
    elif isinstance(value, list):
        for item in value:
            output.update(_evidence_ids(item))
    return output
