"""Semantic Artifact store used to connect independently callable actions."""

from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .models import ArtifactRef
from .recovery_io import file_lock


_ARTIFACT_ID_PATTERN = re.compile(r"^art_[0-9a-f]{32}$")


def workspace_root() -> Path:
    configured = (
        os.environ.get("RESEARCHCHEM_MCP_WORKSPACE", "").strip()
        or os.environ.get("RESEARCHCHEMBENCH_WORKSPACE", "").strip()
    )
    if not configured:
        raise RuntimeError(
            "RESEARCHCHEM_MCP_WORKSPACE or RESEARCHCHEMBENCH_WORKSPACE must be "
            "set before calling chemistry tools"
        )
    root = Path(configured).expanduser().resolve()
    if not root.is_dir():
        raise RuntimeError(f"Chemistry workspace does not exist: {root}")
    return root


def resolve_workspace_path(value: str | Path, *, must_exist: bool = False) -> Path:
    root = workspace_root()
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes chemistry workspace: {value}") from exc
    if must_exist and not resolved.exists():
        raise FileNotFoundError(f"Workspace path does not exist: {resolved}")
    return resolved


def relative_workspace_path(value: str | Path) -> str:
    return str(Path(value).resolve(strict=False).relative_to(workspace_root()))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class ArtifactStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or workspace_root()).resolve()
        self.directory = self.root / "_tool_artifacts" / "objects"
        self.index_path = self.root / "_tool_artifacts" / "index.jsonl"
        self.directory.mkdir(parents=True, exist_ok=True)

    def _append_index(self, reference: ArtifactRef) -> None:
        self.import_reference(reference)

    def _path(self, value: str | Path) -> Path:
        candidate = Path(value)
        candidate = candidate if candidate.is_absolute() else self.root / candidate
        try:
            relative = candidate.relative_to(self.root)
            resolved = candidate.resolve()
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise ValueError(f"Artifact path escapes workspace: {value}") from exc
        cursor = self.root
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError(f"Artifact symlink is not allowed: {value}")
        if not resolved.is_file():
            raise FileNotFoundError(f"Artifact file does not exist: {value}")
        return resolved

    def resolve(self, reference: str | dict[str, Any] | ArtifactRef) -> ArtifactRef:
        """Resolve compact or complete refs without discarding their metadata."""
        if isinstance(reference, str):
            return self.find(reference)
        if isinstance(reference, dict) and set(reference) == {"artifact_id"}:
            return self.find(str(reference["artifact_id"]))
        item = ArtifactRef.model_validate(reference)
        try:
            existing = self.find(item.artifact_id)
        except KeyError:
            return item
        if existing != item:
            raise ValueError(f"Artifact reference conflict: {item.artifact_id}")
        return existing

    def import_reference(self, reference: dict[str, Any] | ArtifactRef) -> ArtifactRef:
        """Idempotently register a verified ref in this workspace's index."""
        item = ArtifactRef.model_validate(reference)
        if _sha256(self._path(item.path)) != item.sha256:
            raise ValueError(f"Artifact hash mismatch: {item.artifact_id}")
        with file_lock(self.index_path.with_suffix(".lock")):
            try:
                existing = self._find_unlocked(item.artifact_id)
            except KeyError:
                pass
            else:
                if existing != item:
                    raise ValueError(f"Artifact reference conflict: {item.artifact_id}")
                return existing
            record = {**item.model_dump(mode="json"),
                      "created_at": datetime.now(timezone.utc).isoformat()}
            with self.index_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        return item

    def put_json(
        self,
        value: Any,
        *,
        semantic_type: str,
        producer_action: str,
        producer_backend: str | None,
        parent_artifact_ids: Iterable[str] = (),
    ) -> ArtifactRef:
        artifact_id = f"art_{uuid.uuid4().hex}"
        path = self.directory / f"{artifact_id}.json"
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n",
            encoding="utf-8",
        )
        reference = ArtifactRef(
            artifact_id=artifact_id,
            semantic_type=semantic_type,
            media_type="application/json",
            sha256=_sha256(path),
            path=str(path.relative_to(self.root)),
            producer_action=producer_action,
            producer_backend=producer_backend,
            parent_artifact_ids=list(parent_artifact_ids),
        )
        self._append_index(reference)
        return reference

    def register_file(
        self,
        path_value: str | Path,
        *,
        semantic_type: str,
        producer_action: str,
        producer_backend: str | None,
        media_type: str = "application/octet-stream",
        parent_artifact_ids: Iterable[str] = (),
    ) -> ArtifactRef:
        path = self._path(path_value)
        if not path.is_file():
            raise ValueError(f"Artifact path is not a regular file: {path}")
        reference = ArtifactRef(
            artifact_id=f"art_{uuid.uuid4().hex}",
            semantic_type=semantic_type,
            media_type=media_type,
            sha256=_sha256(path),
            path=str(path.relative_to(self.root)),
            producer_action=producer_action,
            producer_backend=producer_backend,
            parent_artifact_ids=list(parent_artifact_ids),
        )
        self._append_index(reference)
        return reference

    def load(self, reference: str | dict[str, Any] | ArtifactRef) -> Any:
        item = self.resolve(reference)
        path = self._path(item.path)
        if _sha256(path) != item.sha256:
            raise ValueError(f"Artifact hash mismatch: {item.artifact_id}")
        if item.media_type == "application/json" or path.suffix.lower() == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
        return {"path": str(path.relative_to(self.root)), "artifact": item.model_dump(mode="json")}

    def find(self, artifact_id: str) -> ArtifactRef:
        # Readers share the writers' short index lock, so a concurrent export
        # cannot expose a partly appended JSON record to another job.
        with file_lock(self.index_path.with_suffix(".lock")):
            return self._find_unlocked(artifact_id)

    def _find_unlocked(self, artifact_id: str) -> ArtifactRef:
        if not self.index_path.is_file():
            raise KeyError(f"Unknown ArtifactRef: {artifact_id}")
        for line in reversed(self.index_path.read_text(encoding="utf-8").splitlines()):
            if not line.strip():
                continue
            value = json.loads(line)
            if value.get("artifact_id") == artifact_id:
                value.pop("created_at", None)
                return ArtifactRef.model_validate(value)
        raise KeyError(f"Unknown ArtifactRef: {artifact_id}")


def canonicalize_artifact_refs(
    value: Any,
    *,
    store: ArtifactStore | None = None,
) -> Any:
    """Expand explicit compact ArtifactRefs without loading their payloads.

    Public Action calls commonly pass only ``{"artifact_id": "art_..."}`` or the
    artifact id string copied from a previous result.  Canonicalization verifies
    that exact reference and expands it to the immutable full reference before a
    worker is launched.  It never substitutes another artifact or scientific
    value.
    """

    artifact_store = store or ArtifactStore()
    if isinstance(value, ArtifactRef):
        return artifact_store.resolve(value).model_dump(mode="json")
    if isinstance(value, str) and _ARTIFACT_ID_PATTERN.fullmatch(value):
        return artifact_store.find(value).model_dump(mode="json")
    if isinstance(value, dict):
        if "artifact_id" in value:
            if set(value) == {"artifact_id"}:
                return artifact_store.find(str(value["artifact_id"])).model_dump(mode="json")
            required = {"artifact_id", "semantic_type", "media_type", "sha256", "path"}
            if required <= set(value):
                return artifact_store.resolve(value).model_dump(mode="json")
            missing = sorted(required - set(value))
            extra = sorted(set(value) - {"artifact_id"})
            raise ValueError(
                "ArtifactRef dictionaries must be either the artifact id string, "
                "{'artifact_id': 'art_...'}, or a complete immutable ArtifactRef. "
                f"This partial reference has extra fields {extra} and is missing {missing}; "
                "pass only artifact_id to let the toolbox load the canonical reference."
            )
        return {
            key: canonicalize_artifact_refs(item, store=artifact_store)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [canonicalize_artifact_refs(item, store=artifact_store) for item in value]
    if isinstance(value, tuple):
        return tuple(canonicalize_artifact_refs(item, store=artifact_store) for item in value)
    return value


def collect_artifact_refs(value: Any) -> list[ArtifactRef]:
    references: list[ArtifactRef] = []
    if isinstance(value, ArtifactRef):
        references.append(value)
    elif isinstance(value, dict):
        if set(("artifact_id", "semantic_type", "media_type", "sha256", "path")) <= set(value):
            references.append(ArtifactRef.model_validate(value))
        else:
            for item in value.values():
                references.extend(collect_artifact_refs(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            references.extend(collect_artifact_refs(item))
    return references
