"""Read-only scientific-resource registry with explicit agent selection.

The resource configuration is controlled by the benchmark operator. Requests may
refer only to entries declared there; arbitrary host paths remain forbidden. No
function in this module chooses a pseudopotential or parameter family for the
agent.
"""

from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESOURCE_CONFIG = PROJECT_ROOT / "config" / "toolbox_resources.json"
_RESOURCE_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_ELEMENT = re.compile(r"^[A-Z][a-z]?$|^[A-Z][a-z]{2}$")


def resource_config_path() -> Path:
    configured = os.environ.get("RESEARCHCHEM_RESOURCE_CONFIG", "").strip()
    return Path(configured).expanduser().resolve() if configured else DEFAULT_RESOURCE_CONFIG


def _declared_path(value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


@lru_cache(maxsize=4)
def _load_config_at(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("selection_policy") != "agent_explicit_no_default":
        raise ValueError("Resource registry must declare agent_explicit_no_default")
    resources = payload.get("resources")
    if not isinstance(resources, list):
        raise ValueError("Resource registry requires a resources list")
    seen: set[str] = set()
    for item in resources:
        if not isinstance(item, dict):
            raise ValueError("Every resource entry must be an object")
        resource_id = str(item.get("id", ""))
        if not _RESOURCE_ID.fullmatch(resource_id) or resource_id in seen:
            raise ValueError(f"Invalid or duplicate resource id: {resource_id!r}")
        seen.add(resource_id)
        if not str(item.get("path", "")).strip():
            raise ValueError(f"Resource {resource_id} requires a path")
        if item.get("kind") == "element_file_collection" and not (
            item.get("manifest") or item.get("element_pattern")
        ):
            raise ValueError(
                f"Element-file resource {resource_id} requires manifest or element_pattern"
            )
    return payload


def load_resource_config() -> dict[str, Any]:
    """Load the operator-controlled registry without probing or selecting entries."""

    return _load_config_at(str(resource_config_path()))


def resource_specs() -> dict[str, dict[str, Any]]:
    return {str(item["id"]): dict(item) for item in load_resource_config()["resources"]}


def is_resource_reference(value: Any) -> bool:
    return (
        isinstance(value, str)
        and value.startswith("resource://")
    ) or (
        isinstance(value, dict)
        and isinstance(value.get("resource_id"), str)
    )


def parse_resource_reference(value: Any) -> tuple[str, str | None]:
    if isinstance(value, dict) and isinstance(value.get("resource_id"), str):
        resource_id = value["resource_id"].strip()
        element_value = value.get("element")
        element = str(element_value).strip() if element_value is not None else None
        extra = sorted(set(value) - {"resource_id", "element"})
        if extra:
            raise ValueError(f"Unknown ResourceRef fields: {extra}")
        return resource_id, element
    if isinstance(value, str) and value.startswith("resource://"):
        remainder = unquote(value[len("resource://") :])
        if not remainder or remainder.startswith("/"):
            raise ValueError("Resource URI must contain a resource id")
        parts = remainder.split("/")
        if len(parts) > 2 or any(not part for part in parts):
            raise ValueError("Resource URI syntax is resource://<resource_id>[/<element>]")
        return parts[0], parts[1] if len(parts) == 2 else None
    raise ValueError("Expected ResourceRef object or resource:// URI")


def _manifest(specification: dict[str, Any]) -> dict[str, Any] | None:
    value = specification.get("manifest")
    if not value:
        return None
    path = _declared_path(str(value))
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Resource manifest must be an object: {path}")
    return payload


def resolve_resource_reference(value: Any) -> Path:
    """Resolve exactly one declared ResourceRef to a read-only file/directory.

    This function performs validation only. It never searches across collections,
chooses a default family, model, or substitutes an unavailable entry.
    """

    resource_id, element = parse_resource_reference(value)
    specifications = resource_specs()
    if resource_id not in specifications:
        raise ValueError(f"Unknown scientific resource: {resource_id!r}")
    specification = specifications[resource_id]
    if not bool(specification.get("selectable", True)):
        raise ValueError(f"Resource {resource_id!r} is runtime-managed, not request-selectable")
    root = _declared_path(str(specification["path"]))
    kind = specification.get("kind")
    if kind == "element_file_collection":
        if not element or not _ELEMENT.fullmatch(element):
            raise ValueError(
                f"Resource {resource_id!r} requires an explicit chemical element"
            )
        manifest = _manifest(specification)
        if manifest is not None:
            if element not in manifest:
                raise ValueError(f"Resource {resource_id!r} does not contain element {element}")
            filename_field = str(specification.get("manifest_filename_field", "filename"))
            record = manifest[element]
            if not isinstance(record, dict) or not isinstance(record.get(filename_field), str):
                raise ValueError(
                    f"Resource manifest has no {filename_field!r} for element {element}"
                )
            candidate = (root / record[filename_field]).resolve()
        else:
            candidate = (root / str(specification["element_pattern"]).format(element=element)).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ValueError("Resource reference escapes its declared root") from exc
        if not candidate.is_file():
            raise FileNotFoundError(f"Registered resource file is missing: {candidate}")
        return candidate
    if element is not None:
        raise ValueError(f"Resource {resource_id!r} does not accept an element suffix")
    if kind == "slater_koster_parameter_set":
        if not root.is_dir():
            raise FileNotFoundError(f"Registered parameter directory is missing: {root}")
        return root
    if kind in {"model_checkpoint", "single_file_resource"}:
        if not root.is_file():
            raise FileNotFoundError(f"Registered resource file is missing: {root}")
        return root
    raise ValueError(f"Resource {resource_id!r} is not a request-selectable file resource")


def resource_reference_metadata(value: Any) -> dict[str, Any]:
    resource_id, element = parse_resource_reference(value)
    specification = resource_specs().get(resource_id)
    if specification is None:
        return {"resource_id": resource_id, "element": element, "registered": False}
    result: dict[str, Any] = {
        "resource_id": resource_id,
        "element": element,
        "registered": True,
        "kind": specification.get("kind"),
        "version": specification.get("version"),
        "format": specification.get("format"),
        "compatible_backends": list(specification.get("compatible_backends") or []),
    }
    for key in ("model_branches", "model_branch_aliases", "single_task"):
        if key in specification:
            result[key] = specification[key]
    manifest = _manifest(specification)
    if manifest is not None and element in manifest:
        result["element_metadata"] = manifest[element]
    return result


def collect_resource_references(value: Any) -> list[dict[str, Any]]:
    """Collect explicit references from a nested request for provenance."""

    found: list[dict[str, Any]] = []

    def visit(item: Any) -> None:
        if is_resource_reference(item):
            found.append(resource_reference_metadata(item))
            return
        if isinstance(item, dict):
            for child in item.values():
                visit(child)
        elif isinstance(item, (list, tuple)):
            for child in item:
                visit(child)

    visit(value)
    unique: dict[tuple[str, str | None], dict[str, Any]] = {}
    for item in found:
        unique[(str(item["resource_id"]), item.get("element"))] = item
    return list(unique.values())


def _element_names(specification: dict[str, Any], root: Path) -> list[str]:
    manifest = _manifest(specification)
    if manifest is not None:
        return sorted(str(key) for key in manifest)
    pattern = str(specification.get("element_pattern") or "")
    if "{element}" not in pattern:
        return []
    prefix, suffix = pattern.split("{element}", 1)
    names = []
    for path in root.glob(f"{prefix}*{suffix}"):
        name = path.name
        element = name[len(prefix) : len(name) - len(suffix) if suffix else None]
        if _ELEMENT.fullmatch(element):
            names.append(element)
    return sorted(set(names))


def _skf_coverage(root: Path, file_glob: str) -> tuple[list[str], list[str]]:
    pairs = sorted(path.stem for path in root.glob(file_glob) if "-" in path.stem)
    elements = sorted({part for pair in pairs for part in pair.split("-", 1)})
    return elements, pairs


def resource_snapshot() -> list[dict[str, Any]]:
    """Return catalog-safe resource metadata and lightweight availability probes."""

    result = []
    for specification in load_resource_config()["resources"]:
        item = dict(specification)
        root = _declared_path(str(item["path"]))
        file_kinds = {"backend_executable", "model_checkpoint", "single_file_resource"}
        available = root.is_file() if item.get("kind") in file_kinds else root.is_dir()
        item["available"] = available
        item["selection_required"] = bool(item.get("selectable", True))
        if item.get("kind") == "element_file_collection":
            item["selection_syntax"] = f"resource://{item['id']}/<Element>"
            if available:
                try:
                    elements = _element_names(item, root)
                    item["elements"] = elements
                    item["element_count"] = len(elements)
                    manifest = _manifest(item)
                    if manifest is not None:
                        item["element_metadata"] = manifest
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    item["available"] = False
                    item["probe_error"] = str(exc)
        elif item.get("kind") == "slater_koster_parameter_set":
            item["selection_syntax"] = f"resource://{item['id']}"
            if available:
                elements, pairs = _skf_coverage(root, str(item.get("file_glob", "*.skf")))
                item["elements"] = elements
                item["element_count"] = len(elements)
                item["pair_count"] = len(pairs)
                item["available_pairs"] = pairs
        elif item.get("kind") in {"model_checkpoint", "single_file_resource"}:
            item["selection_syntax"] = f"resource://{item['id']}"
            if available:
                item["size_bytes"] = root.stat().st_size
        elif item.get("kind") == "backend_executable":
            target_value = item.get("install_target")
            target = None
            if target_value:
                configured = Path(str(target_value)).expanduser()
                target = Path(
                    os.path.abspath(
                        configured if configured.is_absolute() else PROJECT_ROOT / configured
                    )
                )
            item["configured_target"] = bool(target and target.is_file())
        result.append(item)
    return result


def resources_for_backends(backend_ids: Iterable[str]) -> list[dict[str, Any]]:
    selected = set(backend_ids)
    return [
        item for item in resource_snapshot()
        if selected.intersection(item.get("compatible_backends") or [])
    ]
