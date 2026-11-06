#!/usr/bin/env python3
"""Read only the newest V3 case for each small-molecule task and agent."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import socket
import sys
import time

import check_eval_status as status


def launch_order(case):
    """Use the immutable launch timestamp, never a log/directory modification time."""
    match = re.search(r"(?:_|-)(\d{8}_\d{6})(?:_|-|$)", case.name)
    if match:
        try:
            stamp = datetime.strptime(match[1], "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc)
            return stamp.timestamp(), case.name
        except ValueError:
            pass
    submission = status.read_json(case / "submission.json", [])
    try:
        stamp = datetime.fromisoformat(submission["submitted_at"].replace("Z", "+00:00"))
        return stamp.replace(tzinfo=stamp.tzinfo or timezone.utc).timestamp(), case.name
    except (KeyError, TypeError, ValueError):
        return 0, case.name


def latest_result(paper_id, agent, result_root):
    cases = [p for p in result_root.glob(paper_id + "_*") if p.is_dir()]
    if not cases:
        return {"paper_id": paper_id, "agent": agent, "status": "not_started",
                "status_label": "未运行", "scored": False, "score_status": "尚无评分",
                "case_dir": None, "run_dir": None, "host": None, "last_update_utc": None,
                "notes": [], "warnings": []}
    case = max(cases, key=launch_order)
    # Only inspect canonical execution records inside the selected case. Never
    # fall back to an older scored case when the newest launch failed or is empty.
    runs = [p for p in case.glob("runs/cli_runs/batch_*/autonomous_research-*")
            if p.is_dir() and any((p / name).is_file()
                                 for name in ("_meta.json", "recovery/run.json"))]
    run = max(runs, key=launch_order) if runs else case
    row = status.inspect(run)
    row.update(paper_id=paper_id, agent=agent, case_dir=str(case), run_dir=str(run))
    if row["execution_state"] in {"preflight_failed", "startup_failed", "launch_failed"}:
        row.update(status="failed", status_label="启动失败")
    elif not runs and row["status"] == "unknown":
        submission = status.read_json(case / "submission.json", row["warnings"])
        if submission.get("phase") == "preflight":
            row.update(status="preflight", status_label="仅预检记录，尚未进入评估")
    return row


def collect(tasks_root, workspaces, agents):
    tasks = sorted(p.name for p in tasks_root.glob("paper_*")
                   if (p / "agent_input/task.md").is_file())
    if not tasks:
        raise ValueError("没有找到顶层评估任务：" + str(tasks_root))
    rows = [latest_result(paper, agent, workspaces / f"{agent}_gpt61_high_small_molecules_v3")
            for paper in tasks for agent in agents]
    return {"checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "local_host": socket.gethostname(), "scope": "small_molecules_v3_latest_only",
            "tasks": len(tasks), "entries": len(rows),
            "states": dict(Counter(row["status"] for row in rows)),
            "scored_entries": sum(row["scored"] for row in rows), "results": rows}


def display(report, details=False):
    print(f"检查时间（UTC）：{report['checked_at_utc']}  本机：{report['local_host']}")
    print(f"V3 共 {report['tasks']} 个任务；每个任务/智能体只显示最新结果。")
    for agent in dict.fromkeys(row["agent"] for row in report["results"]):
        rows = [r for r in report["results"] if r["agent"] == agent]
        print(f"{agent}: 有运行目录 {sum(r['case_dir'] is not None for r in rows)}，"
              f"未运行 {sum(r['status'] == 'not_started' for r in rows)}，"
              f"最新结果已评分 {sum(r['scored'] for r in rows)}")
    print("\n任务 ID | Agent | 状态 | 评分 | 调查完成 | 最近更新（UTC） | 运行服务器")
    for row in report["results"]:
        count = row.get("investigations_total", 0)
        investigation = f"{row['investigations_completed']}/{count}" if count else "—"
        print(" | ".join((row["paper_id"], row["agent"], row["status_label"], row["score_status"],
                          investigation, row["last_update_utc"] or "—",
                          row["host"].split("--", 1)[0] if row["host"] else "—")))
    if details:
        for row in report["results"]:
            if row["case_dir"]:
                status.print_detail(row)
    print("\n远端运行记录未验证远端进程；在对应服务器执行可核验本机进程。"
          "评分与执行状态分开显示，0 分也算已评分。只读检查，不自动恢复任务。", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=("arche", "codex", "both"), default="both")
    parser.add_argument("--tasks-root", type=Path,
                        default=status.ROOT / "tasks/small_molecules_verified_autonomous_research")
    parser.add_argument("--workspaces", type=Path, default=status.ROOT / "workspaces")
    parser.add_argument("--watch", type=int, metavar="SECONDS", help="持续监控的刷新间隔，如 60")
    parser.add_argument("--json", action="store_true", help="输出一次结构化 JSON")
    parser.add_argument("--details", action="store_true", help="包含最新目录、调用次数和诊断说明")
    args = parser.parse_args(argv)
    if args.watch is not None and (args.watch < 1 or args.json):
        parser.error("--watch 必须大于零，且不能与 --json 同时使用")
    agents = ("arche", "codex") if args.agent == "both" else (args.agent,)
    try:
        while True:
            report = collect(args.tasks_root.resolve(), args.workspaces.resolve(), agents)
            if args.json:
                print(json.dumps(report, ensure_ascii=False, indent=2))
            else:
                if args.watch and sys.stdout.isatty():
                    print("\033[2J\033[H", end="")
                display(report, args.details)
            if not args.watch:
                break
            time.sleep(args.watch)
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError) as exc:
        print("检查失败：" + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
