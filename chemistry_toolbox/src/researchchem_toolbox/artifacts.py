"""Semantic Artifact store used to connect independently callable actions."""

from __future__ import annotations

import hashlib
import json
import os
import re
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .models import ArtifactRef


_LOCK = threading.Lock()
_ARTIFACT_ID_PATTERN = re.compile(r"^art_[0-9a-f]{32}$")


def workspace_root() -> Path:
    configured = (
        os.environ.get("RESEARCHCHEM_MCP_WORKSPACE", "").strip()
        or os.environ.get("RESEARCHCHEMBENCH_WORKSPACE", "").strip()
    )
    root = Path(configured).expanduser().resolve() if configured else Path.cwd().resolve()
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
        record = {
            **reference.model_dump(mode="json"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with _LOCK:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            with self.index_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")

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
            path=relative_workspace_path(path),
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
        path = resolve_workspace_path(path_value, must_exist=True)
        if not path.is_file():
            raise ValueError(f"Artifact path is not a regular file: {path}")
        reference = ArtifactRef(
            artifact_id=f"art_{uuid.uuid4().hex}",
            semantic_type=semantic_type,
            media_type=media_type,
            sha256=_sha256(path),
            path=relative_workspace_path(path),
            producer_action=producer_action,
            producer_backend=producer_backend,
            parent_artifact_ids=list(parent_artifact_ids),
        )
        self._append_index(reference)
        return reference

    def load(self, reference: str | dict[str, Any] | ArtifactRef) -> Any:
        if isinstance(reference, ArtifactRef):
            item = reference
        elif isinstance(reference, dict):
            if set(reference) == {"artifact_id"}:
                item = self.find(str(reference["artifact_id"]))
            else:
                item = ArtifactRef.model_validate(reference)
        else:
            item = self.find(reference)
        path = resolve_workspace_path(item.path, must_exist=True)
        if _sha256(path) != item.sha256:
            raise ValueError(f"Artifact hash mismatch: {item.artifact_id}")
        if item.media_type == "application/json" or path.suffix.lower() == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
        return {"path": relative_workspace_path(path), "artifact": item.model_dump(mode="json")}

    def find(self, artifact_id: str) -> ArtifactRef:
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
        return value.model_dump(mode="json")
    if isinstance(value, str) and _ARTIFACT_ID_PATTERN.fullmatch(value):
        return artifact_store.find(value).model_dump(mode="json")
    if isinstance(value, dict):
        if "artifact_id" in value:
            if set(value) == {"artifact_id"}:
                return artifact_store.find(str(value["artifact_id"])).model_dump(mode="json")
            required = {"artifact_id", "semantic_type", "media_type", "sha256", "path"}
            if required <= set(value):
                return ArtifactRef.model_validate(value).model_dump(mode="json")
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
