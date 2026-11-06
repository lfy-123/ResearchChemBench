"""Compact terminal summaries; all inputs are existing read-only run records."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import time

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from ..provenance.evidence_archive import audit_directory, read_json
from ..provenance.model_io import redact_trace_value
from ..provenance.results import read_scoring_status

CONSOLE_INTERVAL_SECONDS = 600


def duration(seconds):
    if seconds is None:
        return "未知"
    minutes, seconds = divmod(max(0, int(seconds)), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def age(timestamp, now):
    return max(0, now - datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp()) if timestamp else None


def format_terminal_progress(workspace, *, judging=False):
    workspace = Path(workspace)
    now = time.time()
    meta = read_json(workspace / "_meta.json")
    snapshot = read_json(audit_directory(workspace) / "progress.json")
    store = ExecutionStore.open_existing(workspace)
    manifest = store.get_record("run", "manifest", {}) if store else {}
    usage = snapshot.get("usage") or meta.get("usage_details") or {}
    state = manifest.get("run_state") or meta.get("status", "starting")
    phase = "评分中" if judging else snapshot.get("phase", state) if state == snapshot.get("run_status") else state
    elapsed = age(meta.get("first_started_at"), now) if judging or state in {"ready", "running", "recovering", "finalizing"} else meta.get("run_elapsed_seconds", meta.get("duration_seconds"))
    phases = {"starting": "启动中", "ready": "准备中", "running": "研究中", "recovering": "恢复中",
              "waiting_for_compute": "等待计算", "waiting_for_provider": "等待模型服务",
              "finalizing": "收尾中", "completed": "研究运行结束", "cancelled": "已取消",
              "failed": "运行失败", "suspended_infrastructure": "运行中断", "budget_exhausted": "预算耗尽"}
    count = lambda value: "未知" if value is None else f"{value:,}"
    requests = usage.get("model_request_count")
    if requests is not None:
        model_count = f"已记录请求{count(requests)}次"
    elif (manifest.get("agent_kind") or meta.get("agent_key")) == "claude":
        model_count = f"已完成响应{count(usage.get('agent_completed_turns'))}次"
    else:
        model_count = f"可观察步骤{count(usage.get('observable_model_steps'))}（非精确请求数）"
    timestamp = datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [f"[RCB][{timestamp}][PROGRESS] {meta.get('paper_id', workspace.name)} | {phases.get(phase, phase)} | 已用时 {duration(elapsed)}",
             f"模型：{model_count} | 工具调用{count(snapshot.get('tool_call_count'))}次"]
    output = workspace / "_agent_output.jsonl"
    if output.is_file():
        lines[-1] += f" | 最近Agent输出 {duration(now - output.stat().st_mtime)}前"

    jobs = [j for j in store.execution_snapshot() if j["entity_type"] == "job"] if store else []
    counts = Counter(j["state"] for j in jobs)
    labels = {"success": "执行成功", "failed": "失败", "partial_success": "部分成功", "running": "运行",
              "queued": "排队", "launching": "启动", "cancelled": "取消", "cancel_requested": "取消中",
              "timeout": "超时", "invalid_request": "请求无效", "needs_reconciliation": "待核对"}
    lines.append("作业：" + (" | ".join([f"总{len(jobs)}"] + [f"{labels.get(k, k)}{v}" for k, v in sorted(counts.items())]) if store else "未知"))
    running, finished, allocated = [], [], []
    for job in jobs:
        facts = json.loads(job["state_json"])
        status, spec = facts.get("status") or {}, job["spec"]
        cores = (spec.get("resource_limits") or status.get("resource_limits") or {}).get("cpu_cores")
        metadata = spec.get("metadata") or {}
        label = metadata.get("label") or metadata.get("software_id") or spec.get("action_id") or spec.get("job_type", "")
        label = " ".join(str(label).split())[:70]
        text = f"  {job['entity_id'][:16]} {label} | {count(cores)}核"
        if job["state"] in {"running", "launching"}:
            allocated.append(cores)
            seconds = age(status.get("started_at"), now)
            running.append((seconds or 0, text + f" | 已运行 {duration(seconds)}"))
        elif status.get("finished_at"):
            seconds = status.get("duration_seconds")
            text += f" | {labels.get(job['state'], job['state'])} | 用时 {duration(seconds)}"
            cpu = status.get("resource_usage") or {}
            if seconds and cpu.get("user_cpu_seconds") is not None and cpu.get("system_cpu_seconds") is not None:
                average = (cpu["user_cpu_seconds"] + cpu["system_cpu_seconds"]) / seconds
                text += f" | 记录平均用核 {average:.1f}" + ("（中断记录可能不全）" if job["state"] in {"cancelled", "timeout"} else "")
            finished.append((status["finished_at"], text))
    budget = meta.get("resource_budget") or {}
    allocated_total = sum(allocated) if store and all(n is not None for n in allocated) else None
    lines.append(f"资源：运行/启动作业分配CPU {count(allocated_total)}/{count(budget.get('cpu_cores'))}核（非实际利用率）")
    for title, items in [("运行中", running), ("最近结束", finished)]:
        if items:
            lines.append(title + (f"（显示{min(3, len(items))}/{len(items)}项）" if title == "运行中" else "") + "：")
            lines.extend(text for _, text in sorted(items, reverse=True)[:3])
    scoring = read_scoring_status(workspace)
    if judging or scoring["evaluation_status"] != "not_started":
        judge_usage = scoring.get("judge_usage") or {}
        score = read_json(workspace / "_score.json").get("score")
        score_state = "preparing" if judging and scoring["evaluation_status"] == "not_started" else scoring["evaluation_status"]
        lines.append(f"评分记录：{score_state} | 已记录响应{count(judge_usage.get('request_count'))}次"
                     + (f" | 已发布分数{score:g}" if score is not None else ""))
    error = scoring.get("evaluation_reason") if judging or state == "completed" else manifest.get("error") or meta.get("error")
    if error:
        message = error.get("message", error) if isinstance(error, dict) else error
        lines.append("异常：" + " ".join(str(redact_trace_value(message)).split())[:300])
    return redact_trace_value("\n".join(lines))
