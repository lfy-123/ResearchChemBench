#!/usr/bin/env python3
"""Read-only status inspection for ResearchChemBench ARCHE/Codex results."""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import socket
import sqlite3
import sys

ACTIVE = {"running", "starting", "queued", "launching", "preparing", "recovering", "resuming"}
FAILED = {"failed", "error", "cancelled", "budget_exhausted", "timeout", "timed_out"}
SKIP = {"outputs", "report", "code", "data", "local_data", "tool_logs",
        "recovery", "scoring", "task_snapshot", "launch", "__pycache__"}
LABELS = {"running": "运行中", "remote_running": "运行中（远端记录，未验活）",
          "completed": "已结束", "failed": "失败/停止",
          "interrupted": "已中断（本机进程已退出）", "unknown": "待确认"}
ROOT = Path(__file__).resolve().parents[2]


def read_json(path, warnings):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("expected object")
        return value
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as exc:
        warnings.append(f"无法读取 {path.name}：{type(exc).__name__}")
        return {}


def discover(root):
    """Traverse directory wrappers, never scientific outputs or logs."""
    found, seen = [], set()

    def visit(path, depth):
        physical = path.resolve()
        if physical in seen:
            return
        seen.add(physical)
        if any((path / name).is_file() for name in ("_meta.json", "recovery/run.json")):
            found.append(physical)
            return
        before = len(found)
        if depth < 6:
            # Case folders also contain archived scoring revisions. Only the
            # canonical runs/cli_runs subtree represents execution attempts.
            children = ([path / n for n in ("runs", "cli_runs") if (path / n).is_dir()]
                        if (path / "submission.json").is_file() else sorted(path.iterdir()))
            for child in children:
                if child.is_dir() and not child.name.startswith(".") and child.name not in SKIP:
                    visit(child, depth + 1)
        if len(found) == before and (path / "submission.json").is_file():
            found.append(physical)

    visit(root, 0)
    return sorted(set(found))


def find_case(run):
    for parent in (run, *run.parents[:5]):
        if (parent / "submission.json").is_file():
            return parent
    return None


def read_ledger(run, run_id, warnings):
    suffix = "" if run.name == run_id else "-" + hashlib.sha256(str(run).encode()).hexdigest()[:12]
    database = run.parent / ".rcb_recovery" / (run_id + suffix) / "execution.sqlite3"
    if not database.is_file():
        return {}
    try:
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True, timeout=2)) as db:
            rows = db.execute("SELECT namespace, payload FROM records WHERE "
                              "(namespace='run' AND key='manifest') OR "
                              "(namespace IN ('controller','agent') AND key='identity')").fetchall()
        values = {namespace: json.loads(payload) for namespace, payload in rows}
        return {key: value for key, value in values.items() if isinstance(value, dict)}
    except (sqlite3.Error, ValueError, OSError) as exc:
        warnings.append(f"无法读取运行账本：{type(exc).__name__}")
        return {}


def process_state(identity, fallback_host, local_host):
    """Verify PID, host, boot ID and start ticks; never trust a PID alone."""
    if not identity or not identity.get("pid"):
        return "unknown"
    host = identity.get("host") or fallback_host
    if host and host != local_host:
        return "remote"
    if not host or identity.get("start_ticks") is None or not identity.get("boot_id"):
        return "unknown"
    try:
        pid = int(identity["pid"])
        if pid <= 0:
            return "unknown"
        boot = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        if boot != identity["boot_id"]:
            return "dead"
        stat = Path(f"/proc/{pid}/stat").read_text()
        fields = stat[stat.rfind(")") + 2:].split()
        if fields[0] in {"Z", "X"} or str(fields[19]) != str(identity["start_ticks"]):
            return "dead"
        return "alive"
    except FileNotFoundError:
        return "dead" if Path("/proc/self/stat").exists() else "unknown"
    except (OSError, ValueError, IndexError, KeyError):
        return "unknown"


def classify(execution, submission, processes, host, local_host, is_resume=False):
    # Run state outranks stale launcher metadata, common with Codex cases.
    if execution == "completed" and not is_resume:
        return "completed"
    if execution in FAILED and not is_resume:
        return "failed"
    if submission in FAILED and "alive" not in processes:
        return "failed"
    active = is_resume or execution in ACTIVE or (not execution and submission in ACTIVE)
    if active:
        if "alive" in processes:
            return "running"
        if "remote" in processes or (host and host != local_host):
            return "remote_running"
        if processes and all(state == "dead" for state in processes):
            return "interrupted"
    if not execution and submission == "completed":
        return "completed"
    return "unknown"


def scoring_status(score, attempt):
    if score.get("status") == "scored" and isinstance(score.get("score"), (int, float)):
        label = f"{score['score']:g}/{score.get('score_max', 100):g}"
        if attempt.get("score_id") and attempt.get("score_id") != score.get("score_id"):
            label += f"（另有评分尝试：{attempt.get('status', '未知')}）"
        return label
    state = attempt.get("status") or score.get("status")
    labels = {"preparing": "评分准备中", "running": "评分中",
              "suspended_infrastructure": "评分因基础设施问题暂停",
              "needs_review": "评分待复核", "in_doubt": "评分状态待确认", "failed": "评分失败"}
    return labels.get(state, f"评分状态：{state}" if state else "尚无评分")


def inspect(run):
    warnings = []
    local_host = socket.gethostname()
    case = find_case(run)
    meta = read_json(run / "_meta.json", warnings)
    manifest = read_json(run / "recovery/run.json", warnings)
    sub = read_json(case / "submission.json", warnings) if case else {}
    settings = read_json(case / "test_settings.json", warnings) if case else {}
    run_id = meta.get("run_id") or manifest.get("run_id") or run.name
    ledger = read_ledger(run, run_id, warnings)
    manifest = ledger.get("run") or manifest
    execution = manifest.get("run_state") or meta.get("status") or ""
    identities = [ledger.get("controller", {}), ledger.get("agent", {})]
    # controller.lock is an advisory lock, not a complete process identity.
    identity_files = []
    if case:
        identity_files += [case / ".runtime/launcher_identity.json", case / "launch/evaluator_identity.json"]
        resume_log = sub.get("resume_log")
        if isinstance(resume_log, str):
            candidate = Path(resume_log).parent / "evaluator_identity.json"
            if candidate.is_absolute() and case in candidate.resolve().parents:
                identity_files.append(candidate)
    identities += [read_json(p, warnings) for p in identity_files]
    identities = [i for i in identities if i.get("pid")]
    host = next((i.get("host") for i in identities if i.get("host")), None) or settings.get("host")
    processes = [process_state(i, host, local_host) for i in identities]
    resuming = sub.get("phase") == "resume" and sub.get("status") in ACTIVE
    state = classify(execution, sub.get("status"), processes, host, local_host, resuming)
    score = read_json(run / "_score.json", warnings)
    attempt = read_json(run / "_scoring_attempt.json", warnings)
    arche = run / "outputs/arche"
    budget = read_json(arche / "model_budget.json", warnings)
    investigations = read_json(arche / "investigation_states.json", warnings).get("sessions", [])
    application = read_json(arche / "application_result.json", warnings)
    outcome = read_json(arche / "adapter_outcome.json", warnings)
    note = []
    if state == "remote_running":
        note.append("共享存储上的远端运行记录；本机不能验证远端 PID，请在原服务器检查")
    elif state == "interrupted":
        note.append("文件仍标记运行，但保存的本机进程身份均已失效；不是已完成")
    elif state == "unknown":
        note.append("状态证据不足；不会仅根据日志多久未更新判断失败")
    if resuming:
        note.append("已请求续跑，优先显示续跑进程状态")
    if state in {"failed", "interrupted"}:
        reason = application.get("reason_code") or meta.get("termination") or sub.get("phase")
        if reason:
            note.append("记录原因：" + str(reason))
        if outcome.get("error_type"):
            note.append("异常类型：" + str(outcome["error_type"]))
    if state == "completed" and score.get("status") != "scored":
        note.append("Agent 执行已结束，不等于 Judger 已完成评分")
    if state == "completed" and "alive" in processes:
        note.append("评估进程仍存活，可能正在评分或收尾")
    activity_files = [run / n for n in ("_meta.json", "_score.json", "_scoring_attempt.json",
        "_live_progress.log", "_agent_output.jsonl", "_tool_call_events.jsonl", "recovery/run.json")]
    activity_files += [arche / "model_budget.json", arche / "investigation_states.json"]
    if case:
        activity_files.append(case / "submission.json")
    times = []
    for p in activity_files:
        try:
            times.append(p.stat().st_mtime)
        except OSError:
            pass
    latest = datetime.fromtimestamp(max(times), timezone.utc).isoformat(timespec="seconds") if times else None
    tasks = sub.get("tasks") or [{}]
    paper = meta.get("paper_id") or manifest.get("paper_id") or tasks[0].get("paper_id") or "未知"
    agent = meta.get("agent_key") or manifest.get("agent_key") or sub.get("agent") or "未知"
    return {"paper_id": paper, "agent": agent, "status": state, "status_label": LABELS[state],
            "execution_state": execution or sub.get("status"), "score_status": scoring_status(score, attempt),
            "score": score.get("score"), "scored": score.get("status") == "scored",
            "judge_model": score.get("judge_model"), "host": host, "process_states": processes,
            "last_update_utc": latest, "case_dir": str(case or run), "run_dir": str(run),
            "report_present": (run / "report/report.md").is_file(),
            "results_present": (run / "report/results.json").is_file(),
            "investigations_completed": sum(s.get("state") == "completed" for s in investigations),
            "investigations_total": len(investigations),
            "counted_calls": budget.get("counted_calls"),
            "call_limit": budget.get("limits", {}).get("max_turns"),
            "rate_limited_calls": budget.get("rate_limited_calls"), "notes": note, "warnings": warnings}


def print_detail(row):
    print(f"\n任务：{row['paper_id']}  |  Agent：{row['agent']}")
    print(f"状态：{row['status_label']}  |  评分：{row['score_status']}")
    print(f"运行主机：{row['host'] or '未记录'}")
    print(f"最近记录更新（UTC）：{row['last_update_utc'] or '未知'}")
    if row["counted_calls"] is not None:
        limit = row["call_limit"] if row["call_limit"] is not None else "未设上限"
        print(f"模型调用：{row['counted_calls']}/{limit}；限流：{row['rate_limited_calls']} 次")
    if row["investigations_total"]:
        print(f"调查完成：{row['investigations_completed']}/{row['investigations_total']}")
    print("最终交付：report.md=" + ("存在" if row["report_present"] else "缺失")
          + "，results.json=" + ("存在" if row["results_present"] else "缺失"))
    print("结果目录：" + row["case_dir"])
    if row["run_dir"] != row["case_dir"]:
        print("运行目录：" + row["run_dir"])
    for note in row["notes"] + row["warnings"]:
        print("说明：" + note)


def main(argv=None):
    parser = argparse.ArgumentParser(description="只读检查 ARCHE/Codex 评估状态；不启动、停止或恢复任务，不调用模型。")
    parser.add_argument("path", help="单个结果目录、内部运行目录或包含多个结果的父目录")
    parser.add_argument("--json", action="store_true", help="输出结构化 JSON")
    parser.add_argument("--details", action="store_true", help="批量查看时也输出各任务详细信息")
    args = parser.parse_args(argv)
    path = Path(args.path).expanduser()
    if not path.exists() and not path.is_absolute():
        path = ROOT / path
    if not path.is_dir():
        parser.error("结果目录不存在：" + str(path))
    try:
        paths = discover(path.resolve())
        if not paths:
            raise ValueError("没有找到结果记录（submission.json、_meta.json 或 recovery/run.json）")
        rows = [inspect(p) for p in paths]
    except (OSError, ValueError) as exc:
        print("检查失败：" + str(exc), file=sys.stderr)
        return 2
    summary = dict(Counter(row["status"] for row in rows))
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "local_host": socket.gethostname(), "runs": len(rows),
              "papers": len({r["paper_id"] for r in rows}), "states": summary,
              "scored_runs": sum(r["scored"] for r in rows),
              "completed_papers": len({r["paper_id"] for r in rows if r["status"] == "completed"}),
              "results": rows}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"检查时间：{result['checked_at_utc']}  本机：{result['local_host']}")
        print(f"共 {result['runs']} 次运行 / {result['papers']} 个任务；已结束 {summary.get('completed', 0)} 次，"
              f"已评分 {result['scored_runs']} 次（零分也算已评分）。")
        print("状态统计：" + "；".join(f"{LABELS[k]} {v}" for k, v in summary.items()))
        if len(rows) == 1 or args.details:
            for row in rows:
                print_detail(row)
        else:
            print("\n任务 ID | Agent | 状态 | 评分 | 最近记录更新（UTC） | 结果目录名")
            for row in rows:
                print(" | ".join(str(row[k] or "—") for k in
                      ("paper_id", "agent", "status_label", "score_status", "last_update_utc"))
                      + " | " + Path(row["case_dir"]).name)
            print("\n每一行对应一次运行，历史失败与重跑分别列出；用 --details 查看具体路径和说明。")
        print("\n运行中仅表示进程存活或远端记录，不能保证科学计算持续推进；不会按日志静默时间直接判失败。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
