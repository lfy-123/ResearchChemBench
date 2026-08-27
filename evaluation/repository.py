"""Discovery and loading for current paper-scoped task packages."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional

from .contracts import TASK_TYPES, TaskInfo, read_evaluation, validate_task_package
from .settings import TASK_ROOTS, WORKSPACES_DIR


class TaskRepositoryError(RuntimeError):
    pass


class DuplicateTaskError(TaskRepositoryError):
    pass


class InvalidTaskPackageError(TaskRepositoryError):
    pass


@dataclass(frozen=True)
class TaskPackage:
    paper_id: str
    task_type: str
    directory: Path
    category: str
    difficulty: str
    difficulty_reasons: tuple[str, ...]
    package_content_sha256: str

    @property
    def key(self) -> tuple[str, str]:
        return self.task_type, self.paper_id


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


class TaskRepository:
    """Validated index keyed by ``(task_type, paper_id)``."""

    def __init__(self, roots: Iterable[str | Path] | None = None):
        self.roots = tuple(
            dict.fromkeys(Path(root).expanduser().resolve() for root in (roots or TASK_ROOTS))
        )
        self._index = self._build_index()

    def _candidate_directories(self) -> list[Path]:
        candidates: list[Path] = []
        for root in self.roots:
            if not root.exists():
                continue
            if root.is_symlink():
                raise InvalidTaskPackageError(f"task_root_is_symlink:{root}")
            for task_type in TASK_TYPES:
                mode_root = root / task_type
                if not mode_root.is_dir():
                    continue
                candidates.extend(
                    path.resolve()
                    for path in sorted(mode_root.iterdir())
                    if path.is_dir() and not path.is_symlink()
                )
        return candidates

    def _build_index(self) -> dict[tuple[str, str], TaskPackage]:
        index: dict[tuple[str, str], TaskPackage] = {}
        paper_modes: dict[str, set[str]] = {}
        for directory in self._candidate_directories():
            validation = validate_task_package(directory)
            if validation.status != "passed":
                raise InvalidTaskPackageError(
                    f"invalid_task_package:{directory}:{';'.join(validation.findings)}"
                )
            info = TaskInfo.model_validate(_read_json(directory / "task_info.json"))
            manifest = _read_json(directory / "package_manifest.json")
            package = TaskPackage(
                paper_id=info.paper_id,
                task_type=info.task_type,
                directory=directory,
                category=info.category,
                difficulty=info.difficulty,
                difficulty_reasons=tuple(info.difficulty_reasons),
                package_content_sha256=str(manifest["package_content_sha256"]),
            )
            if package.key in index:
                previous = index[package.key]
                raise DuplicateTaskError(
                    f"duplicate_task:{package.task_type}:{package.paper_id}:"
                    f"{previous.directory}:{package.directory}"
                )
            index[package.key] = package
            paper_modes.setdefault(package.paper_id, set()).add(package.task_type)
        for paper_id, modes in paper_modes.items():
            if "experiment_validation" in modes and modes & {
                "autonomous_research", "paper_reproduction"
            }:
                raise InvalidTaskPackageError(f"mixed_paper_mode_set:{paper_id}")
        return index

    def get(self, *, paper_id: str, task_type: str) -> TaskPackage:
        try:
            return self._index[(task_type, paper_id)]
        except KeyError as exc:
            raise FileNotFoundError(f"task not found: {task_type}/{paper_id}") from exc

    def list(self, *, task_type: str | None = None) -> list[TaskPackage]:
        values = list(self._index.values())
        if task_type:
            values = [item for item in values if item.task_type == task_type]
        return sorted(values, key=lambda item: (item.task_type, item.paper_id))


def _repository(repository: TaskRepository | None = None) -> TaskRepository:
    return repository or TaskRepository()


def list_tasks(task_type: str | None = None, *, repository: TaskRepository | None = None) -> list[dict[str, Any]]:
    return [
        {
            "paper_id": item.paper_id,
            "task_type": item.task_type,
            "title": load_task_info(
                paper_id=item.paper_id, task_type=item.task_type, repository=repository
            )["title"],
            "category": item.category,
            "difficulty": item.difficulty,
            "difficulty_reasons": list(item.difficulty_reasons),
        }
        for item in _repository(repository).list(task_type=task_type)
    ]


def load_task_package(*, paper_id: str, task_type: str, repository: TaskRepository | None = None) -> TaskPackage:
    return _repository(repository).get(paper_id=paper_id, task_type=task_type)


def get_task_directory(*, paper_id: str, task_type: str, repository: TaskRepository | None = None) -> Path:
    return load_task_package(paper_id=paper_id, task_type=task_type, repository=repository).directory


def load_task_info(*, paper_id: str, task_type: str, repository: TaskRepository | None = None) -> dict[str, Any]:
    package = load_task_package(paper_id=paper_id, task_type=task_type, repository=repository)
    return TaskInfo.model_validate(_read_json(package.directory / "task_info.json")).model_dump(mode="json")


def load_task_text(*, paper_id: str, task_type: str, repository: TaskRepository | None = None) -> str:
    package = load_task_package(paper_id=paper_id, task_type=task_type, repository=repository)
    return (package.directory / "agent_input" / "task.md").read_text(encoding="utf-8")


def load_submission_schema(*, paper_id: str, task_type: str, repository: TaskRepository | None = None) -> dict[str, Any]:
    package = load_task_package(paper_id=paper_id, task_type=task_type, repository=repository)
    return _read_json(package.directory / "agent_input" / "submission_schema.json")


def load_public_task(*, paper_id: str, task_type: str, repository: TaskRepository | None = None) -> dict[str, Any]:
    return {
        "paper_id": paper_id,
        "task_type": task_type,
        "task_text": load_task_text(paper_id=paper_id, task_type=task_type, repository=repository),
        "task_info": load_task_info(paper_id=paper_id, task_type=task_type, repository=repository),
        "submission_schema": load_submission_schema(paper_id=paper_id, task_type=task_type, repository=repository),
    }


def load_private_reference(*, paper_id: str, task_type: str, evaluator_context: bool = False, repository: TaskRepository | None = None) -> dict[str, dict[str, Any]]:
    if not evaluator_context:
        raise PermissionError("private references require evaluator_context=True")
    package = load_task_package(paper_id=paper_id, task_type=task_type, repository=repository)
    return read_evaluation(package.directory / "evaluation")


def materialize_agent_files(*, paper_id: str, task_type: str, destination: str | Path, repository: TaskRepository | None = None) -> list[str]:
    package = load_task_package(paper_id=paper_id, task_type=task_type, repository=repository)
    source = package.directory / "agent_input"
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(relative.as_posix())
    return copied


def list_tasks_grouped() -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = {}
    for item in list_tasks():
        groups.setdefault(item["category"], []).append(item)
    return dict(sorted(groups.items()))


def list_runs(*, paper_id: str | None = None, task_type: str | None = None) -> list[dict[str, Any]]:
    if not WORKSPACES_DIR.exists():
        return []
    runs: list[dict[str, Any]] = []
    candidates = list(WORKSPACES_DIR.glob("*/_meta.json"))
    candidates.extend(WORKSPACES_DIR.glob("cli_runs/*/*/_meta.json"))
    for meta_path in sorted(candidates, reverse=True):
        try:
            meta = _read_json(meta_path)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if paper_id and meta.get("paper_id") != paper_id:
            continue
        if task_type and meta.get("task_type") != task_type:
            continue
        runs.append({**meta, "workspace": str(meta_path.parent)})
    return runs


def get_run_workspace(run_id: str) -> Optional[Path]:
    if not run_id or "/" in run_id or "\\" in run_id:
        return None
    direct = WORKSPACES_DIR / run_id
    if direct.is_dir():
        try:
            if _read_json(direct / "_meta.json").get("run_id") == run_id:
                return direct
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    for candidate in (WORKSPACES_DIR / "cli_runs").glob(f"*/{run_id}"):
        try:
            if candidate.is_dir() and _read_json(candidate / "_meta.json").get("run_id") == run_id:
                return candidate
        except (OSError, ValueError, json.JSONDecodeError):
            continue
    return None


def safe_resolve(base: Path, user_path: str) -> Optional[Path]:
    try:
        base = base.resolve()
        resolved = (base / user_path).resolve()
        resolved.relative_to(base)
        return resolved
    except (ValueError, OSError):
        return None


def build_file_tree(root: Path, prefix: str = "", max_per_dir: int = 0, max_depth: int = 0) -> list[dict[str, Any]]:
    tree: list[dict[str, Any]] = []

    def walk(path: Path, display_prefix: str, depth: int) -> None:
        try:
            entries = sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name))
        except (OSError, PermissionError):
            return
        if max_per_dir:
            entries = entries[:max_per_dir]
        for entry in entries:
            relative = f"{display_prefix}/{entry.name}" if display_prefix else entry.name
            if entry.is_dir():
                tree.append({"name": entry.name, "path": relative, "type": "directory"})
                if not max_depth or depth < max_depth:
                    walk(entry, relative, depth + 1)
            else:
                tree.append({"name": entry.name, "path": relative, "type": "file", "size": entry.stat().st_size})

    walk(root, prefix, 1)
    return tree
