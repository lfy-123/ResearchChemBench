"""Compact predefined-Action results for the progressive MCP surface.

The dispatcher stores every successful primary scientific result as an immutable
JSON Artifact before this module is called.  Returning the same dense Hessian,
normal-mode tensor, or full coordinate table inline therefore adds model-context
cost without adding provenance.  This module keeps decision-relevant scalars and
typed ArtifactRefs inline while leaving the complete result in the artifact store.
It does not change a scientific value, choose a backend, retry, or fall back.
"""

from __future__ import annotations

import json
from typing import Any


MAX_INLINE_LIST_ITEMS = 160
MAX_INLINE_MAPPING_CHARS = 16_000
MAX_ERROR_CHARS = 4_000

_STRUCTURE_KEYS = {
    "structure",
    "optimized_structure",
    "transition_state",
    "transition_state_candidate",
    "reactant_structure",
    "product_structure",
}
_DENSE_ARRAY_KEYS = {
    "matrix",
    "hessian",
    "modes",
    "normal_modes",
    "trajectory_coordinates",
    "coordinates_by_frame",
    "eigenvectors",
    "density_grid",
    "potential_grid",
}


def _compact_artifact(reference: dict[str, Any]) -> dict[str, Any]:
    """Keep the immutable fields required for direct downstream handoff."""

    return {
        key: reference[key]
        for key in (
            "artifact_id",
            "semantic_type",
            "media_type",
            "sha256",
            "path",
            "producer_action",
            "producer_backend",
            "parent_artifact_ids",
        )
        if key in reference
    }


def _array_shape(value: Any) -> list[int | str]:
    shape: list[int | str] = []
    current = value
    while isinstance(current, list):
        shape.append(len(current))
        if not current:
            break
        first = current[0]
        if any(type(item) is not type(first) for item in current[1:]):
            shape.append("ragged")
            break
        current = first
    return shape


def _artifact_pointer(
    primary: dict[str, Any] | None,
    *,
    content: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "inline": False,
        "content": content,
        "note": "Complete value is stored in the primary immutable artifact.",
    }
    if primary:
        value["artifact_id"] = primary.get("artifact_id")
        value["semantic_type"] = primary.get("semantic_type")
        value["path"] = primary.get("path")
    if extra:
        value.update(extra)
    return value


def _structure_summary(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    atoms = value.get("atoms")
    summary: dict[str, Any] = {}
    if isinstance(atoms, list):
        summary["atom_count"] = len(atoms)
        symbols = [
            str(atom.get("element") or atom.get("symbol") or "")
            for atom in atoms
            if isinstance(atom, dict)
        ]
        if symbols and all(symbols):
            counts: dict[str, int] = {}
            for symbol in symbols:
                counts[symbol] = counts.get(symbol, 0) + 1
            summary["element_counts"] = counts
    for key in ("charge", "multiplicity", "pbc", "source_path"):
        if key in value:
            summary[key] = value[key]
    return summary


def _compact_payload(
    value: Any,
    *,
    primary: dict[str, Any] | None,
    key: str | None = None,
) -> Any:
    if key in _STRUCTURE_KEYS and isinstance(value, (dict, list)):
        return _artifact_pointer(
            primary,
            content="AtomicStructure",
            extra=_structure_summary(value),
        )
    if key in _DENSE_ARRAY_KEYS and isinstance(value, list):
        return _artifact_pointer(
            primary,
            content=key,
            extra={"shape": _array_shape(value)},
        )
    if isinstance(value, list):
        if len(value) > MAX_INLINE_LIST_ITEMS:
            return _artifact_pointer(
                primary,
                content=key or "array",
                extra={
                    "shape": _array_shape(value),
                    "item_count": len(value),
                    "first_items": value[:3],
                    "last_items": value[-3:],
                },
            )
        return [
            _compact_payload(item, primary=primary, key=key)
            for item in value
        ]
    if isinstance(value, dict):
        compacted = {
            item_key: _compact_payload(item, primary=primary, key=item_key)
            for item_key, item in value.items()
        }
        if len(json.dumps(compacted, ensure_ascii=False, default=str)) > MAX_INLINE_MAPPING_CHARS:
            # Preserve scalar decision variables even when an unanticipated nested
            # payload is large; the complete mapping remains in the primary artifact.
            scalars = {
                item_key: item
                for item_key, item in compacted.items()
                if isinstance(item, (str, int, float, bool)) or item is None
            }
            return _artifact_pointer(
                primary,
                content=key or "structured_result",
                extra={"inline_scalars": scalars, "field_count": len(value)},
            )
        return compacted
    return value


def _bounded_text(value: Any, limit: int = MAX_ERROR_CHARS) -> Any:
    if not isinstance(value, str) or len(value) <= limit:
        return value
    half = (limit - 80) // 2
    return value[:half] + "\n... diagnostic text compacted ...\n" + value[-half:]


def _compact_error(error: Any) -> Any:
    if not isinstance(error, dict):
        return _bounded_text(error)
    return {
        key: (
            "Omitted from the Agent view; inspect the BackendDiagnostic artifact."
            if key == "traceback" and value
            else _bounded_text(value)
        )
        for key, value in error.items()
    }


def compact_action_result(result: dict[str, Any]) -> dict[str, Any]:
    """Return the bounded Agent view of one canonical ``ActionResult`` envelope."""

    if not isinstance(result, dict) or "status" not in result:
        return result
    output_artifacts = [
        _compact_artifact(item)
        for item in (result.get("output_artifacts") or [])
        if isinstance(item, dict)
    ]
    primary = output_artifacts[0] if output_artifacts else None
    exposed_outputs = [
        item
        for index, item in enumerate(output_artifacts)
        if index == 0 or item.get("semantic_type") != "BackendFile"
    ]
    input_artifacts = [
        _compact_artifact(item)
        for item in (result.get("input_artifacts") or [])
        if isinstance(item, dict)
    ]
    value = dict(result)
    value["result"] = _compact_payload(
        result.get("result"), primary=primary, key="result"
    )
    value["input_artifacts"] = input_artifacts
    value["output_artifacts"] = exposed_outputs
    value["error"] = _compact_error(result.get("error"))
    value["warnings"] = [
        _bounded_text(item, 1_500) for item in (result.get("warnings") or [])
    ]
    value["artifact_handoff"] = {
        "primary_output": primary,
        "matching_input_artifacts": input_artifacts,
        "rule": (
            "Pass the primary artifact only to an input expecting its semantic_type. "
            "For a later Action that also needs the matching structure or another source value, "
            "reuse the separately listed matching input artifact; do not put one artifact_id into "
            "two differently typed input fields."
        ),
    }
    value["transport"] = {
        "mode": "compact_agent_view",
        "scientific_values_changed": False,
        "complete_primary_result": primary,
        "supplementary_artifact_count": max(0, len(output_artifacts) - len(exposed_outputs)),
        "supplementary_artifact_manifest": "_tool_artifacts/index.jsonl",
    }
    return value


__all__ = ["compact_action_result"]
