"""Task/run discovery, file trees, and safe path helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .config import TASKS_DIR, WORKSPACES_DIR
from .task_schema import GroundTruth, TaskInfo


def list_tasks() -> list[str]:
    if not TASKS_DIR.exists():
        return []
    return sorted(
        path.name
        for path in TASKS_DIR.iterdir()
        if path.is_dir() and (path / "task_info.json").is_file()
    )


def load_task_info(task_id: str) -> dict:
    path = TASKS_DIR / task_id / "task_info.json"
    return TaskInfo.model_validate_json(path.read_text(encoding="utf-8")).model_dump()


def load_ground_truth(task_id: str) -> dict:
    path = TASKS_DIR / task_id / "target_study" / "ground_truth.json"
    return GroundTruth.model_validate_json(path.read_text(encoding="utf-8")).model_dump()


def list_tasks_grouped() -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for task_id in list_tasks():
        category = load_task_info(task_id).get("category", "uncategorized")
        groups.setdefault(category, []).append(task_id)
    return dict(sorted(groups.items()))


def list_runs(task_id: Optional[str] = None) -> list[dict]:
    if not WORKSPACES_DIR.exists():
        return []
    runs: list[dict] = []
    candidates = list(WORKSPACES_DIR.glob("*/_meta.json"))
    candidates.extend(WORKSPACES_DIR.glob("cli_runs/*/*/_meta.json"))
    for meta_path in sorted(candidates, reverse=True):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if task_id and meta.get("task_id") != task_id:
            continue
        runs.append(
            {
                "run_id": meta.get("run_id", meta_path.parent.name),
                "task_id": meta.get("task_id"),
                "timestamp": meta.get("timestamp"),
                "status": meta.get("status", "unknown"),
                "agent_name": meta.get("agent_name", ""),
                "agent_key": meta.get("agent_key", ""),
                "model": meta.get("model", ""),
                "duration_seconds": meta.get("duration_seconds"),
                "report_exists": meta.get("report_exists", False),
                "workspace": str(meta_path.parent),
            }
        )
    return runs


def _is_run_workspace(path: Path, run_id: str) -> bool:
    try:
        meta = json.loads((path / "_meta.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return meta.get("run_id") == run_id


def get_run_workspace(run_id: str) -> Optional[Path]:
    if not run_id or "/" in run_id or "\\" in run_id:
        return None
    direct = WORKSPACES_DIR / run_id
    if direct.is_dir() and _is_run_workspace(direct, run_id):
        return direct
    for candidate in (WORKSPACES_DIR / "cli_runs").glob(f"*/{run_id}"):
        if candidate.is_dir() and _is_run_workspace(candidate, run_id):
            return candidate
    return None


def safe_resolve(base: Path, user_path: str) -> Optional[Path]:
    try:
        base_resolved = base.resolve()
        resolved = (base_resolved / user_path).resolve()
        resolved.relative_to(base_resolved)
        return resolved
    except (ValueError, OSError):
        return None


def build_file_tree(
    root: Path,
    prefix: str = "",
    max_per_dir: int = 0,
    max_depth: int = 0,
) -> list[dict]:
    tree: list[dict] = []
    skip_names = {".claude", ".codex", "__pycache__"}

    def walk(path: Path, display_prefix: str, depth: int) -> None:
        try:
            entries = sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
        except (PermissionError, FileNotFoundError):
            return
        entries = [item for item in entries if item.name not in skip_names]
        total = len(entries)
        if max_per_dir and total > max_per_dir:
            entries = entries[:max_per_dir]
        for entry in entries:
            rel = f"{display_prefix}/{entry.name}" if display_prefix else entry.name
            if entry.is_dir():
                node = {"name": entry.name, "path": rel, "type": "directory"}
                tree.append(node)
                if max_depth and depth >= max_depth:
                    node["truncated"] = True
                else:
                    walk(entry, rel, depth + 1)
            else:
                try:
                    stat = entry.stat()
                except OSError:
                    continue
                tree.append(
                    {
                        "name": entry.name,
                        "path": rel,
                        "type": "file",
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                    }
                )
        if max_per_dir and total > max_per_dir:
            tree.append(
                {
                    "name": f"… {total - max_per_dir} more items",
                    "path": f"{display_prefix}/_more",
                    "type": "truncated",
                }
            )

    walk(root, prefix, 1)
    return tree

