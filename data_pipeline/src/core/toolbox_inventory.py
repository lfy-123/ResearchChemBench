from __future__ import annotations

from typing import Any


_SOFTWARE_SECTIONS = ("backends", "native_software", "python_packages")
_UNAVAILABLE_STATES = {
    "absent",
    "disabled",
    "missing",
    "not_available",
    "not_installed",
    "unavailable",
    "unsupported",
}


def installed_software_inventory(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Return the Agent-facing toolbox view.

    Stage06/07 only need to know which software is installed.  Preset Actions and
    task-specific capability coverage are intentionally omitted: the absence of a
    preset Action is not evidence that an installed program is unavailable.
    """

    if snapshot.get("view_kind") == "installed_software_inventory":
        rows = snapshot.get("installed_software") or []
        return {
            key: snapshot[key]
            for key in (
                "schema_version",
                "profile_id",
                "catalog_hash",
                "runtime_profile_hash",
                "view_kind",
                "inventory_semantics",
                "installed_software",
                "audit_note",
            )
            if key in snapshot
        } | {"installed_software": rows}

    merged: dict[str, dict[str, Any]] = {}
    for section in _SOFTWARE_SECTIONS:
        source_rows = snapshot.get(section)
        if not isinstance(source_rows, dict):
            continue
        for software_id, raw in source_rows.items():
            row = raw if isinstance(raw, dict) else {}
            states = {
                str(row.get("availability") or "").strip().casefold(),
                str(row.get("local_installation_status") or "").strip().casefold(),
            }
            if states & _UNAVAILABLE_STATES:
                continue
            key = str(software_id).strip()
            if not key:
                continue
            entry = merged.setdefault(
                key.casefold(),
                {
                    "software_id": key,
                    "display_name": str(row.get("display_name") or key),
                    "aliases": [],
                },
            )
            aliases = row.get("aliases") or []
            if not isinstance(aliases, list):
                aliases = [aliases]
            entry["aliases"] = sorted(
                {
                    *entry.get("aliases", []),
                    *(str(alias) for alias in aliases if str(alias).strip()),
                },
                key=str.casefold,
            )
            version = row.get("version") or row.get("installed_version")
            if version not in (None, ""):
                entry["version"] = version

    return {
        "schema_version": snapshot.get("schema_version"),
        "profile_id": snapshot.get("profile_id"),
        "catalog_hash": snapshot.get("catalog_hash"),
        "runtime_profile_hash": snapshot.get("runtime_profile_hash"),
        "view_kind": "installed_software_inventory",
        "inventory_semantics": (
            "Every listed entry is installed and available in the read-only chemistry "
            "toolbox. Absence from this list is the only software-inventory signal; this "
            "view intentionally contains no preset Action or feature-coverage claims."
        ),
        "installed_software": sorted(
            merged.values(), key=lambda item: str(item["display_name"]).casefold()
        ),
        "audit_note": (
            "Do not infer missing software from absent preset Actions. Treat every listed "
            "software entry, including any matching alias, as installed."
        ),
    }
