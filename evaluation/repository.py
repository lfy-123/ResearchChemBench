"""Task-package discovery, loading, run discovery, and safe path helpers.

Task Package v1 is the canonical runtime format.  Legacy benchmark tasks are
handled by a deliberately isolated read-only adapter so old fields never leak
into the v1 contract or producer output.
"""

from __future__ import annotations

import fnmatch
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal, Optional

from researchchembench_contracts import (
    TASK_INFO_SCHEMA_V1,
    PackageManifestV1,
    SubmissionSchemaV1,
    TaskInfoV1,
    validate_task_package,
)

from .schemas.task import GroundTruth, TaskInfo
from .settings import TASK_ROOTS, WORKSPACES_DIR


class TaskRepositoryError(RuntimeError):
    """Base class for explicit task catalog failures."""


class DuplicateTaskIdError(TaskRepositoryError):
    """Raised when distinct packages claim the same globally unique task ID."""


class InvalidTaskPackageError(TaskRepositoryError):
    """Raised when a discovered Task Package v1 fails its transport contract."""


class TaskNotRunnableError(TaskRepositoryError):
    """Raised when a catalogued task is not eligible for benchmark execution."""


@dataclass(frozen=True)
class TaskPackage:
    """One indexed task definition with its real on-disk location."""

    task_id: str
    directory: Path
    package_format: Literal["task_package_v1", "legacy"]
    task_type: str
    category: str
    runtime_readiness: str
    reference_schema: str
    package_content_sha256: str = ""

    @property
    def is_v1(self) -> bool:
        return self.package_format == "task_package_v1"

    @property
    def evaluation_ready(self) -> bool:
        if not self.is_v1:
            return True
        try:
            from .scoring.adapters import evaluator_adapter_available
        except ImportError:
            return False
        return evaluator_adapter_available(self.task_type, self.reference_schema)

    @property
    def runnable(self) -> bool:
        return self.runtime_readiness == "ready" and self.evaluation_ready

    @property
    def unavailable_reasons(self) -> tuple[str, ...]:
        reasons: list[str] = []
        if self.runtime_readiness != "ready":
            reasons.append(f"runtime_readiness:{self.runtime_readiness}")
        if not self.evaluation_ready:
            reasons.append(
                f"evaluator_adapter_unavailable:{self.task_type}:{self.reference_schema}"
            )
        return tuple(reasons)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def _legacy_task_type(info: dict[str, Any]) -> str:
    values = {
        str(info.get("task_mode") or "").strip().casefold(),
        str(info.get("scientific_mode") or "").strip().casefold(),
    }
    if values & {"guided_reproduction", "paper_reproduction"}:
        return "paper_reproduction"
    return "autonomous_research"


class TaskRepository:
    """Build a globally unique, validated index over one or more task roots."""

    def __init__(self, roots: Iterable[str | Path] | None = None):
        selected = tuple(Path(root).expanduser().resolve() for root in (roots or TASK_ROOTS))
        self.roots = tuple(dict.fromkeys(selected))
        self._index = self._build_index()

    def _candidate_info_paths(self) -> list[Path]:
        candidates: set[Path] = set()
        for root in self.roots:
            if not root.exists():
                continue
            if root.is_symlink():
                raise InvalidTaskPackageError(f"task_root_is_symlink:{root}")
            direct = root / "task_info.json"
            if direct.is_file():
                candidates.add(direct.resolve())
            for path in root.rglob("task_info.json"):
                if path.is_file():
                    candidates.add(path.resolve())
        return sorted(candidates)

    def _record(self, info_path: Path) -> TaskPackage | None:
        root = info_path.parent
        try:
            raw = _read_json(info_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise InvalidTaskPackageError(
                f"task_info_unreadable:{info_path}:{type(exc).__name__}:{exc}"
            ) from exc
        is_v1 = (
            raw.get("schema_version") == TASK_INFO_SCHEMA_V1
            or (root / "package_manifest.json").is_file()
        )
        if is_v1:
            validation = validate_task_package(root)
            if validation.status != "passed":
                raise InvalidTaskPackageError(
                    f"invalid_task_package:{root}:" + ";".join(validation.findings)
                )
            info = TaskInfoV1.model_validate(raw)
            manifest = PackageManifestV1.model_validate(
                _read_json(root / "package_manifest.json")
            )
            if root.parent.name != info.task_type:
                raise InvalidTaskPackageError(
                    f"task_type_directory_mismatch:{root}:{info.task_type}"
                )
            return TaskPackage(
                task_id=info.task_id,
                directory=root,
                package_format="task_package_v1",
                task_type=info.task_type,
                category=info.category,
                runtime_readiness=info.runtime_readiness,
                reference_schema=info.reference_schema,
                package_content_sha256=manifest.package_content_sha256,
            )

        # Legacy is intentionally permissive only at this compatibility edge.
        # A non-empty embedded task instruction substitutes for task.md, but no
        # legacy value is ever written into or accepted by Task Package v1.
        task_id = str(raw.get("task_id") or "").strip()
        task_text = str(raw.get("task") or "").strip()
        if not task_id or (not (root / "task.md").is_file() and not task_text):
            return None
        try:
            validated = TaskInfo.model_validate(raw)
        except Exception as exc:
            raise InvalidTaskPackageError(
                f"legacy_task_info_invalid:{root}:{type(exc).__name__}:{exc}"
            ) from exc
        if root.name != task_id:
            raise InvalidTaskPackageError(f"legacy_task_directory_id_mismatch:{root}")
        return TaskPackage(
            task_id=task_id,
            directory=root,
            package_format="legacy",
            task_type=_legacy_task_type(raw),
            category=validated.category,
            runtime_readiness="ready",
            reference_schema="legacy-ground-truth.v1",
        )

    def _build_index(self) -> dict[str, TaskPackage]:
        index: dict[str, TaskPackage] = {}
        for info_path in self._candidate_info_paths():
            record = self._record(info_path)
            if record is None:
                continue
            previous = index.get(record.task_id)
            if previous and previous.directory != record.directory:
                raise DuplicateTaskIdError(
                    f"duplicate_task_id:{record.task_id}:{previous.directory}:{record.directory}"
                )
            index[record.task_id] = record
        return index

    def get(self, task_id: str) -> TaskPackage:
        try:
            return self._index[task_id]
        except KeyError as exc:
            raise FileNotFoundError(f"Task not found: {task_id}") from exc

    def list(
        self,
        *,
        task_type: str | None = None,
        readiness: str | None = None,
        capability: str | None = None,
        runnable_only: bool = False,
    ) -> list[TaskPackage]:
        values = sorted(self._index.values(), key=lambda item: item.task_id)
        if task_type:
            values = [item for item in values if item.task_type == task_type]
        if readiness:
            values = [item for item in values if item.runtime_readiness == readiness]
        if capability:
            values = [
                item
                for item in values
                if capability
                in {
                    str(entry.get("capability") or "")
                    for entry in load_task_info(item.task_id, repository=self).get(
                        "required_capabilities", []
                    )
                }
            ]
        if runnable_only:
            values = [item for item in values if item.runnable]
        return values


def _repository(repository: TaskRepository | None = None) -> TaskRepository:
    return repository or TaskRepository()


def list_tasks(
    task_type: str | None = None,
    readiness: str | None = None,
    capability: str | None = None,
    runnable_only: bool = False,
    *,
    repository: TaskRepository | None = None,
) -> list[str]:
    return [
        item.task_id
        for item in _repository(repository).list(
            task_type=task_type,
            readiness=readiness,
            capability=capability,
            runnable_only=runnable_only,
        )
    ]


def load_task_package(
    task_id: str, *, repository: TaskRepository | None = None
) -> TaskPackage:
    return _repository(repository).get(task_id)


def get_task_directory(
    task_id: str, *, repository: TaskRepository | None = None
) -> Path:
    return load_task_package(task_id, repository=repository).directory


def load_task_info(
    task_id: str, *, repository: TaskRepository | None = None
) -> dict[str, Any]:
    package = load_task_package(task_id, repository=repository)
    raw = _read_json(package.directory / "task_info.json")
    if package.is_v1:
        return TaskInfoV1.model_validate(raw).model_dump(mode="json")
    value = TaskInfo.model_validate(raw).model_dump(mode="json")
    value["task"] = str(raw.get("task") or "")
    return value


def load_task_text(
    task_id: str, *, repository: TaskRepository | None = None
) -> str:
    package = load_task_package(task_id, repository=repository)
    path = package.directory / "task.md"
    if path.is_file():
        return path.read_text(encoding="utf-8")
    raw = _read_json(package.directory / "task_info.json")
    text = str(raw.get("task") or "").strip()
    if not text:
        raise FileNotFoundError(f"Task instruction not found: {task_id}")
    return text


def load_submission_schema(
    task_id: str, *, repository: TaskRepository | None = None
) -> dict[str, Any]:
    package = load_task_package(task_id, repository=repository)
    if package.is_v1:
        raw = _read_json(package.directory / "submission_schema.json")
        return SubmissionSchemaV1.model_validate(raw).model_dump(mode="json")
    info = load_task_info(task_id, repository=repository)
    required = [
        str(item.get("path") or "")
        for item in info.get("required_deliverables", [])
        if str(item.get("path") or "")
    ]
    return {
        "schema_version": "legacy-derived-submission-schema.v1",
        "task_id": task_id,
        "required_files": required,
        "primary_result_file": None,
        "result_schema": {},
        "allowed_extra_fields": True,
    }


def load_public_task(
    task_id: str, *, repository: TaskRepository | None = None
) -> dict[str, Any]:
    package = load_task_package(task_id, repository=repository)
    return {
        "task_id": task_id,
        "task_type": package.task_type,
        "runtime_readiness": package.runtime_readiness,
        "package_format": package.package_format,
        "task_text": load_task_text(task_id, repository=repository),
        "task_info": load_task_info(task_id, repository=repository),
        "submission_schema": load_submission_schema(task_id, repository=repository),
    }


def load_private_reference(
    task_id: str,
    *,
    evaluator_context: bool = False,
    repository: TaskRepository | None = None,
) -> dict[str, Any]:
    if not evaluator_context:
        raise PermissionError("Private task references require evaluator_context=True")
    package = load_task_package(task_id, repository=repository)
    if package.is_v1:
        return _read_json(package.directory / "evaluation" / "reference.json")
    path = package.directory / "target_study" / "ground_truth.json"
    return GroundTruth.model_validate_json(path.read_text(encoding="utf-8")).model_dump(
        mode="json"
    )


def load_ground_truth(
    task_id: str, *, repository: TaskRepository | None = None
) -> dict[str, Any]:
    """Compatibility loader; v1 runtime adaptation is supplied by the scorer."""

    return load_private_reference(
        task_id, evaluator_context=True, repository=repository
    )


def _allowlisted(relative: str, patterns: Iterable[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/**") and relative.startswith(pattern[:-2]):
            return True
        if fnmatch.fnmatchcase(relative, pattern):
            return True
    return False


def materialize_agent_files(
    task_id: str,
    destination: str | Path,
    *,
    repository: TaskRepository | None = None,
) -> list[str]:
    """Copy only the task package's declared Agent-visible files."""

    package = load_task_package(task_id, repository=repository)
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    if not package.is_v1:
        source = package.directory / "data"
        if source.exists():
            shutil.copytree(source, destination / "data", dirs_exist_ok=True)
            return sorted(
                path.relative_to(destination).as_posix()
                for path in (destination / "data").rglob("*")
                if path.is_file()
            )
        (destination / "data").mkdir(exist_ok=True)
        return []

    manifest = PackageManifestV1.model_validate(
        _read_json(package.directory / "package_manifest.json")
    )
    copied: list[str] = []
    for entry in manifest.entries:
        if not _allowlisted(entry.path, manifest.public_to_agent):
            continue
        if entry.visibility.startswith("private_"):
            raise InvalidTaskPackageError(
                f"private_entry_selected_for_agent:{entry.path}"
            )
        source = package.directory / entry.path
        target = destination / entry.path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(entry.path)
    return sorted(copied)


def list_tasks_grouped() -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    repository = TaskRepository()
    for item in repository.list():
        groups.setdefault(item.category or "uncategorized", []).append(item.task_id)
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
                    stat_result = entry.stat()
                except OSError:
                    continue
                tree.append(
                    {
                        "name": entry.name,
                        "path": rel,
                        "type": "file",
                        "size": stat_result.st_size,
                        "mtime": stat_result.st_mtime,
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
