"""Software discovery and exact native invocation guidance for open execution."""

from __future__ import annotations

import html
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from researchchem_toolbox.catalog import backend_specs
from researchchem_toolbox.paths import CONFIG_ROOT, PROJECT_ROOT
from researchchem_toolbox.runtime import (
    probe_all_backends,
    resolve_executable,
    runtime_names,
    runtime_python,
    runtime_spec,
)

from .execution_models import (
    AnalysisRuntimeListRequest,
    DocumentationSearchRequest,
    SoftwareInspectRequest,
    SoftwareListRequest,
)


GUIDE_PATH = CONFIG_ROOT / "native_software_guides.yaml"
DOCUMENTATION_INDEX_PATH = PROJECT_ROOT / ".software_cache" / "documentation" / "index.json"
REQUESTED_STATUS_PATH = CONFIG_ROOT / "requested_software_status.json"
CAPABILITY_SOURCES_PATH = CONFIG_ROOT / "software_capability_sources.yaml"
REQUESTED_SOFTWARE_PATH = CONFIG_ROOT / "requested_software.yaml"
_HTML_TAG = re.compile(r"<[^>]+>")
_SPACE = re.compile(r"\s+")


@lru_cache(maxsize=1)
def load_native_guides() -> dict[str, Any]:
    value = yaml.safe_load(GUIDE_PATH.read_text(encoding="utf-8")) or {}
    if value.get("schema_version") != 1 or not isinstance(value.get("software"), dict):
        raise ValueError(f"Invalid native software guide: {GUIDE_PATH}")
    return value


@lru_cache(maxsize=1)
def load_documentation_index() -> dict[str, Any]:
    if not DOCUMENTATION_INDEX_PATH.is_file():
        return {"software": []}
    value = json.loads(DOCUMENTATION_INDEX_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("software"), list):
        raise ValueError(f"Invalid documentation index: {DOCUMENTATION_INDEX_PATH}")
    return value


@lru_cache(maxsize=1)
def load_requested_status() -> dict[str, Any]:
    if not REQUESTED_STATUS_PATH.is_file():
        return {"runtime_probes": {}, "software": []}
    value = json.loads(REQUESTED_STATUS_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Invalid requested software status: {REQUESTED_STATUS_PATH}")
    return value


@lru_cache(maxsize=1)
def load_requested_software() -> dict[str, Any]:
    value = yaml.safe_load(REQUESTED_SOFTWARE_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(value.get("requested_software"), list):
        raise ValueError(f"Invalid requested software inventory: {REQUESTED_SOFTWARE_PATH}")
    return value


@lru_cache(maxsize=1)
def _source_aliases() -> dict[str, str]:
    aliases: dict[str, str] = {}
    if not CAPABILITY_SOURCES_PATH.is_file():
        return aliases
    value = yaml.safe_load(CAPABILITY_SOURCES_PATH.read_text(encoding="utf-8")) or {}
    for software_id, item in dict(value.get("software") or {}).items():
        aliases[_normalize_id(software_id)] = str(software_id)
        for alias in item.get("aliases") or []:
            aliases[_normalize_id(str(alias))] = str(software_id)
    return aliases


def _normalize_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _documentation_by_id() -> dict[str, dict[str, Any]]:
    return {
        str(item["software_id"]): item
        for item in load_documentation_index().get("software", [])
        if isinstance(item, dict) and item.get("software_id")
    }


def _native_aliases() -> dict[str, str]:
    aliases: dict[str, str] = {}
    for software_id, item in load_native_guides()["software"].items():
        for alias in item.get("aliases") or []:
            normalized = _normalize_id(str(alias))
            if normalized in aliases and aliases[normalized] != software_id:
                raise ValueError(f"Duplicate native software alias {alias!r}")
            aliases[normalized] = software_id
    return aliases


def _documentation_for_software(software_id: str) -> dict[str, Any]:
    documents = _documentation_by_id()
    guide = load_native_guides()["software"].get(software_id) or {}
    ids = [software_id, *(guide.get("documentation_ids") or [])]
    selected = [documents[item] for item in dict.fromkeys(ids) if item in documents]
    if not selected:
        return {}
    merged = dict(selected[0])
    for key in (
        "detected_versions",
        "current_validated_actions",
        "candidate_actions",
        "official_sources",
        "local_documents",
        "downloads",
        "download_errors",
    ):
        values: list[Any] = []
        seen: set[str] = set()
        for item in selected:
            for value in item.get(key) or []:
                marker = json.dumps(value, ensure_ascii=False, sort_keys=True)
                if marker not in seen:
                    seen.add(marker)
                    values.append(value)
        merged[key] = values
    notes = [str(item["notes"]) for item in selected if item.get("notes")]
    if notes:
        merged["notes"] = " | ".join(dict.fromkeys(notes))
    return merged


def _status_software_by_id() -> dict[str, dict[str, Any]]:
    values = load_requested_status().get("software") or []
    return {
        _normalize_id(str(item.get("name") or item.get("software_id"))): item
        for item in values
        if isinstance(item, dict) and (item.get("name") or item.get("software_id"))
    }


def _requested_software_by_id() -> dict[str, dict[str, Any]]:
    return {
        _normalize_id(str(item["name"])): item
        for item in load_requested_software().get("requested_software", [])
        if isinstance(item, dict) and item.get("name")
    }


def _driver_contract(software_id: str) -> dict[str, Any]:
    guide = load_native_guides()["software"].get(software_id) or {}
    backend = backend_specs().get(software_id)
    requested = _requested_software_by_id().get(software_id)
    runtime = guide.get("runtime") or (
        backend.runtime if backend is not None else (requested or {}).get("environment")
    )
    if not runtime:
        raise ValueError(f"Native guide {software_id!r} has no declared runtime")
    backend_commands = set(backend.executables if backend is not None else ())
    requested_commands = set((requested or {}).get("commands") or [])
    return {
        "software_id": software_id,
        "backend": backend,
        "requested": requested,
        "runtime": str(runtime),
        "allowed_commands": backend_commands | requested_commands,
        "backend_commands": backend_commands,
        "requested_commands": requested_commands,
    }


def _resolve_guided_executable(
    runtime: str,
    executable: str,
    command_guide: dict[str, Any],
) -> str | None:
    configured = command_guide.get("configured_path")
    if configured:
        path = Path(str(configured)).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        resolved = path.resolve(strict=False)
        try:
            resolved.relative_to(PROJECT_ROOT.resolve())
        except ValueError as exc:
            raise ValueError(
                f"Configured native executable escapes project root: {configured}"
            ) from exc
        return str(resolved) if resolved.is_file() and resolved.stat().st_mode & 0o111 else None
    return resolve_executable(runtime, executable)


def resolve_software_id(value: str) -> str:
    normalized = _normalize_id(value)
    native_aliases = _native_aliases()
    if normalized in native_aliases:
        return native_aliases[normalized]
    known = set(_documentation_by_id()) | set(backend_specs()) | set(
        load_native_guides()["software"]
    )
    if normalized in known:
        return normalized
    aliases = _source_aliases()
    if normalized in aliases and aliases[normalized] in known:
        return aliases[normalized]
    for backend_id, backend in backend_specs().items():
        if _normalize_id(backend.display_name) == normalized:
            return backend_id
    raise KeyError(f"Unknown software_id {value!r}")


def validate_native_guides() -> None:
    """Ensure every native command is tied to BackendSpec or requested-software config."""

    specifications = backend_specs()
    covered_backend_commands: dict[str, set[str]] = {}
    for software_id, item in load_native_guides()["software"].items():
        contract = _driver_contract(software_id)
        commands = item.get("commands") or {}
        if not isinstance(commands, dict) or not commands:
            raise ValueError(f"Native guide {software_id!r} has no commands")
        declared = contract["allowed_commands"]
        unknown = set(commands) - declared
        if unknown:
            raise ValueError(
                f"Native guide {software_id!r} declares commands absent from BackendSpec and "
                f"requested_software.yaml: {sorted(unknown)}"
            )
        backend = contract["backend"]
        requested = contract["requested"] or {}
        for command in commands:
            if (
                command in contract["backend_commands"]
                and backend is not None
                and contract["runtime"] != backend.runtime
            ):
                raise ValueError(
                    f"Native guide {software_id}/{command} must use BackendSpec runtime "
                    f"{backend.runtime!r}, not {contract['runtime']!r}"
                )
            if (
                command not in contract["backend_commands"]
                and command in contract["requested_commands"]
                and contract["runtime"] != str(requested.get("environment"))
            ):
                raise ValueError(
                    f"Native guide {software_id}/{command} must use requested-software runtime "
                    f"{requested.get('environment')!r}, not {contract['runtime']!r}"
                )
        covered_backend_commands.setdefault(software_id, set()).update(
            set(commands) & contract["backend_commands"]
        )
        for command, guide in commands.items():
            if not str(guide.get("synopsis") or "").strip():
                raise ValueError(f"Native guide {software_id}/{command} lacks synopsis")
    for software_id, specification in specifications.items():
        if specification.executables:
            missing = set(specification.executables) - covered_backend_commands.get(
                software_id, set()
            )
            if missing:
                raise ValueError(
                    f"BackendSpec {software_id!r} lacks invocation guides: {sorted(missing)}"
                )


def native_command_guide(software_id: str, executable: str) -> dict[str, Any]:
    resolved_id = resolve_software_id(software_id)
    contract = _driver_contract(resolved_id)
    backend = contract["backend"]
    if executable not in contract["allowed_commands"]:
        raise ValueError(
            f"{executable!r} is not an executable declared for software_id={resolved_id!r}"
        )
    software = load_native_guides()["software"].get(resolved_id) or {}
    guide = dict((software.get("commands") or {}).get(executable) or {})
    if not guide:
        raise ValueError(
            f"No reviewed native invocation guide exists for {resolved_id}/{executable}"
        )
    if guide.get("enabled", True) is not True:
        raise ValueError(
            f"Native command {resolved_id}/{executable} is intentionally not exposed: "
            f"{guide.get('output_behavior', 'disabled by execution policy')}"
        )
    documentation = _documentation_for_software(resolved_id)
    requested = contract["requested"] or {}
    return {
        "software_id": resolved_id,
        "display_name": (
            backend.display_name
            if backend is not None
            else documentation.get("display_name") or requested.get("name") or resolved_id
        ),
        "runtime": contract["runtime"],
        "executable": executable,
        "resolved_path": _resolve_guided_executable(
            contract["runtime"], executable, guide
        ),
        **guide,
    }


def _module_runtime_index() -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    probes = load_requested_status().get("runtime_probes") or {}
    for runtime, probe in probes.items():
        for module, status in dict(probe.get("modules") or {}).items():
            result.setdefault(_normalize_id(module), []).append(
                {
                    "runtime": runtime,
                    "module": module,
                    "available": bool(status.get("available")),
                    "version": status.get("version"),
                }
            )
    return result


def _analysis_runtimes_for(
    software_id: str,
    backend: Any | None,
    documentation: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    candidates: dict[tuple[str, str], dict[str, Any]] = {}
    module_index = _module_runtime_index()
    names = {software_id}
    if backend is not None:
        names.update(_normalize_id(module) for module in backend.python_modules)
    if documentation:
        names.add(_normalize_id(str(documentation.get("display_name") or "")))
    for name in names:
        for record in module_index.get(name, []):
            candidates[(record["runtime"], record["module"])] = record
    if backend is not None and runtime_python(backend.runtime).is_file():
        for module in backend.python_modules:
            candidates.setdefault(
                (backend.runtime, module),
                {
                    "runtime": backend.runtime,
                    "module": module,
                    "available": True,
                    "version": None,
                },
            )
    guide_runtime = (
        (load_native_guides()["software"].get(software_id) or {}).get("runtime")
    )
    if guide_runtime and runtime_python(str(guide_runtime)).is_file():
        candidates.setdefault(
            (str(guide_runtime), "<Agent-authored program>"),
            {
                "runtime": str(guide_runtime),
                "module": "<Agent-authored program>",
                "available": True,
                "version": None,
            },
        )
    return sorted(candidates.values(), key=lambda item: (item["runtime"], item["module"]))


def _native_commands(software_id: str, backend: Any | None) -> list[dict[str, Any]]:
    guide = load_native_guides()["software"].get(software_id) or {}
    if not guide:
        return []
    contract = _driver_contract(software_id)
    result = []
    for executable, command in dict(guide.get("commands") or {}).items():
        enabled = command.get("enabled", True) is True
        resolved = (
            _resolve_guided_executable(contract["runtime"], executable, command)
            if enabled
            else None
        )
        result.append(
            {
                "executable": executable,
                "enabled": enabled,
                "available": bool(resolved),
                "resolved_path": resolved,
                "synopsis": command.get("synopsis"),
                "input_mode": command.get("input_mode"),
            }
        )
    return result


def _inventory_entries() -> list[dict[str, Any]]:
    docs = _documentation_by_id()
    specs = backend_specs()
    statuses = _status_software_by_id()
    aliased_documentation_ids = set(_native_aliases())
    ids = sorted(
        (set(docs) - aliased_documentation_ids)
        | set(specs)
        | set(load_native_guides()["software"])
    )
    entries: list[dict[str, Any]] = []
    for software_id in ids:
        backend = specs.get(software_id)
        documentation = _documentation_for_software(software_id)
        status = statuses.get(software_id) or {}
        native_commands = _native_commands(software_id, backend)
        analysis_runtimes = _analysis_runtimes_for(software_id, backend, documentation)
        documented_status = documentation.get("inventory_status") or status.get("status")
        available = any(item["available"] for item in native_commands) or any(
            item["available"] for item in analysis_runtimes
        )
        if backend is not None and not backend.executables and not backend.python_modules:
            health = probe_all_backends((backend,)).get(software_id, {})
            available = bool(health.get("available"))
        entries.append(
            {
                "software_id": software_id,
                "display_name": (
                    backend.display_name
                    if backend is not None
                    else documentation.get("display_name", software_id)
                ),
                "inventory_status": documented_status or ("configured" if available else "unknown"),
                "available": available,
                "backend_registered": backend is not None,
                "runtime": (
                    _driver_contract(software_id)["runtime"]
                    if software_id in load_native_guides()["software"]
                    else (backend.runtime if backend is not None else None)
                ),
                "license_class": (
                    backend.license_class
                    if backend is not None
                    else (_requested_software_by_id().get(software_id) or {}).get("license")
                    or status.get("license")
                ),
                "detected_versions": documentation.get("detected_versions") or [],
                "actions": sorted(
                    set(backend.capabilities if backend is not None else ())
                    | set(documentation.get("current_validated_actions") or [])
                ),
                "native_commands": native_commands,
                "analysis_runtimes": analysis_runtimes,
                "documentation_cached": bool(documentation.get("downloads")),
                "aliases": sorted(
                    alias
                    for alias, target in _native_aliases().items()
                    if target == software_id
                ),
            }
        )
    return entries


def list_software(request: SoftwareListRequest) -> dict[str, Any]:
    validate_native_guides()
    entries = _inventory_entries()
    if request.query:
        needle = request.query.casefold()
        entries = [
            item
            for item in entries
            if needle
            in " ".join(
                [
                    item["software_id"],
                    item["display_name"],
                    " ".join(item["actions"]),
                    " ".join(command["executable"] for command in item["native_commands"]),
                ]
            ).casefold()
        ]
    if request.native_only:
        entries = [item for item in entries if item["native_commands"]]
    if request.available_only:
        entries = [item for item in entries if item["available"]]
    selected = entries[: request.limit]
    return {
        "status": "success",
        "count": len(selected),
        "total_matching": len(entries),
        "software": selected,
        "selection_note": (
            "This is an inventory filter only. It does not recommend software, rank backends, "
            "or choose a scientific method."
        ),
    }


def inspect_software(request: SoftwareInspectRequest) -> dict[str, Any]:
    validate_native_guides()
    software_id = resolve_software_id(request.software_id)
    docs = _documentation_for_software(software_id)
    backend = backend_specs().get(software_id)
    entry = next(item for item in _inventory_entries() if item["software_id"] == software_id)
    health = probe_all_backends((backend,)).get(software_id) if backend is not None else None
    guide = load_native_guides()["software"].get(software_id) or {}
    contract = _driver_contract(software_id) if guide else None
    detailed_commands = []
    for executable, command in dict(guide.get("commands") or {}).items():
        enabled = command.get("enabled", True) is True
        resolved = (
            _resolve_guided_executable(contract["runtime"], executable, command)
            if enabled and contract is not None
            else None
        )
        detailed_commands.append(
            {
                "executable": executable,
                "enabled": enabled,
                "available": bool(resolved),
                "resolved_path": resolved,
                **command,
                "native_job_request_template": {
                    "software_id": software_id,
                    "executable": executable,
                    "arguments": command.get("example_arguments") or [],
                    "staged_inputs": [
                        {
                            "source_path": "code/<Agent-created-or-task-file>",
                            "target_path": "<exact filename referenced by the command>",
                        }
                    ],
                    "stdin_target": (
                        "<staged target filename>"
                        if "stdin" in str(command.get("input_mode") or "")
                        else None
                    ),
                    "resource_limits": {
                        "walltime_seconds": 1800,
                        "memory_mb": 4096,
                        "cpu_cores": 1,
                        "gpu_count": 0,
                    },
                },
            }
        )
    return {
        "status": "success",
        **entry,
        "purpose": guide.get("purpose") or (backend.description if backend is not None else None),
        "backend_health": health,
        "python_modules": list(backend.python_modules) if backend is not None else [],
        "native_invocation_guides": detailed_commands,
        "official_sources": docs.get("official_sources") or [],
        "cached_documents": [
            item.get("path") for item in docs.get("downloads") or [] if item.get("path")
        ],
        "local_documents": docs.get("local_documents") or [],
        "candidate_capabilities": docs.get("candidate_actions") or [],
        "notes": docs.get("notes"),
        "decision_boundary": (
            "The guide explains how to invoke this software. The Agent remains responsible for "
            "whether to use it, the scientific input content, parameters, call order, and interpretation."
        ),
    }


def _document_paths(software_id: str) -> list[Path]:
    docs = _documentation_for_software(software_id)
    paths: list[Path] = []
    for item in docs.get("downloads") or []:
        if item.get("path"):
            paths.append(PROJECT_ROOT / str(item["path"]))
    for item in docs.get("local_documents") or []:
        value = item.get("path") if isinstance(item, dict) else item
        if value:
            paths.append(PROJECT_ROOT / str(value))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.expanduser().resolve(strict=False)
        try:
            resolved.relative_to(PROJECT_ROOT.resolve())
        except ValueError:
            continue
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def _searchable_text(path: Path) -> str | None:
    if not path.is_file() or path.stat().st_size > 25 * 1024 * 1024:
        return None
    if path.suffix.lower() in {".pdf", ".gz", ".zip", ".tar", ".bz2", ".xz"}:
        return None
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".html", ".htm"}:
        text = html.unescape(_HTML_TAG.sub(" ", text))
    return _SPACE.sub(" ", text)


def search_software_documentation(request: DocumentationSearchRequest) -> dict[str, Any]:
    software_id = resolve_software_id(request.software_id)
    needle = request.query.casefold()
    results: list[dict[str, Any]] = []
    skipped: list[str] = []
    for path in _document_paths(software_id):
        text = _searchable_text(path)
        if text is None:
            skipped.append(str(path.relative_to(PROJECT_ROOT)))
            continue
        lower = text.casefold()
        cursor = 0
        while len(results) < request.max_results:
            index = lower.find(needle, cursor)
            if index < 0:
                break
            half = request.context_chars // 2
            start = max(0, index - half)
            end = min(len(text), index + len(request.query) + half)
            results.append(
                {
                    "path": str(path.relative_to(PROJECT_ROOT)),
                    "character_offset": index,
                    "excerpt": text[start:end],
                }
            )
            cursor = index + len(request.query)
        if len(results) >= request.max_results:
            break
    docs = _documentation_for_software(software_id)
    return {
        "status": "success",
        "software_id": software_id,
        "query": request.query,
        "match_count": len(results),
        "matches": results,
        "unsearchable_cached_files": skipped,
        "official_sources": docs.get("official_sources") or [],
        "note": (
            "Search results are excerpts from the locally cached documentation. PDFs and archives "
            "are listed but not parsed by this text-search tool."
        ),
    }


def list_analysis_runtimes(request: AnalysisRuntimeListRequest) -> dict[str, Any]:
    probes = load_requested_status().get("runtime_probes") or {}
    result = []
    for name in runtime_names():
        specification = runtime_spec(name)
        python = runtime_python(name)
        probe = probes.get(name) or {}
        available = python.is_file()
        if request.available_only and not available:
            continue
        if request.runtime is not None and name != request.runtime:
            continue
        modules = probe.get("modules") or {
            module: {"available": None, "version": None}
            for module in (
                (specification.get("health_checks") or {}).get("modules")
                or specification.get("modules")
                or []
            )
        }
        commands = sorted(
            set(
                (specification.get("health_checks") or {}).get("commands")
                or specification.get("commands")
                or []
            )
        )
        backends = specification.get("backends") or []
        query_haystack = " ".join(
            [
                name,
                str(specification.get("description") or ""),
                *modules,
                *commands,
                *backends,
            ]
        ).casefold()
        if request.query and request.query.casefold() not in query_haystack:
            continue
        item: dict[str, Any] = {
            "runtime": name,
            "description": specification.get("description"),
            "available": available,
            "module_names": sorted(modules),
            "configured_commands": commands,
            "backends": backends,
        }
        if request.include_details:
            item.update(
                {
                    "python": str(python),
                    "modules": modules,
                    "health_checks": specification.get("health_checks") or {},
                }
            )
        result.append(item)
    total_matches = len(result)
    result = result[: request.limit]
    return {
        "status": "success",
        "count": len(result),
        "total_matches": total_matches,
        "runtimes": result,
        "selection_note": (
            "Select one runtime explicitly according to the imports required by the Agent-authored "
            "program. No runtime or library is chosen automatically. Use runtime=<exact id> and "
            "include_details=true only after narrowing to inspect versions and the Python path."
        ),
        "submit_analysis_program_request_template": {
            "runtime": request.runtime or "<exact runtime id>",
            "script_path": "code/<agent-authored-program>.py",
            "script_target": "agent_program.py",
            "arguments": [],
            "staged_inputs": [
                {
                    "source_path": "data/<required-input>",
                    "target_path": "inputs/<required-input>",
                }
            ],
            "resource_limits": {
                "walltime_seconds": 1800,
                "memory_mb": 4096,
                "cpu_cores": 1,
                "gpu_count": 0,
            },
            "label": "<descriptive scientific operation>",
        },
        "execution_note": (
            "Execute an Agent-authored scientific program with submit_analysis_program, not a "
            "built-in shell, so its source, staged inputs, resources, logs, exit status, and "
            "outputs remain part of the benchmark trace."
        ),
    }


def open_execution_prompt(*, include_command_index: bool = True) -> str:
    """Return a neutral description of layers two and three.

    Progressive discovery omits the eager command synopsis index because the
    same exact information is available on demand through ``list_software`` and
    ``inspect_software``.
    """

    lines = [
        "",
        "### Layer 2: software-native execution",
        "When no predefined Action expresses the required operation, you may author native input "
        "files and invoke a reviewed local command. First call `inspect_software` for the exact "
        "installed executable, input mode, required filenames, synopsis, cached manuals, and request "
        "template. Then use `write_workspace_text`, `validate_native_job`, and `submit_native_job`. "
        "The runner uses no shell, supplies no scientific defaults, selects no software, and performs "
        "no fallback. Poll with `get_execution_job`, inspect logs, and collect files with "
        "`collect_execution_job`.",
        "",
    ]
    if include_command_index:
        lines.append("Reviewed native command ids and invocation synopses:")
        for software_id, item in load_native_guides()["software"].items():
            commands = []
            for executable, command in (item.get("commands") or {}).items():
                if command.get("enabled", True) is True:
                    commands.append(f"{executable}: {command.get('synopsis')}")
            if commands:
                lines.append(f"- `{software_id}` - " + " | ".join(commands))
    else:
        lines.append(
            "The complete software inventory and every reviewed command synopsis remain available "
            "on demand through `list_software` and `inspect_software`; no program is hidden or "
            "selected automatically."
        )
    lines.extend(
        [
            "",
            "### Layer 3: programmable scientific analysis",
            "For an operation that is best expressed by code, call `list_analysis_runtimes`, write a "
            "complete Python file under code/, and submit it with `submit_analysis_program` in one "
            "explicit runtime. The program and every staged input remain auditable; stdout, stderr, "
            "exit status, resources, and output hashes use the same job record as native software. "
            "Use `declare_scientific_artifact` to attach semantic type and parent lineage to important "
            "outputs. The programmable layer is resource-confined but is not a replacement for an "
            "OS/container security boundary.",
            "",
            "The three layers are peers, not a hidden workflow. A predefined Action is a convenient "
            "validated operation when it matches. Native execution and Agent-authored programs are "
            "available for capabilities that were not anticipated by the Action catalog. You decide "
            "the complete plan and may interleave all three layers.",
        ]
    )
    return "\n".join(lines)


def software_resource_snapshot() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "execution_policy": load_native_guides()["policy"],
        **list_software(SoftwareListRequest()),
    }


__all__ = [
    "inspect_software",
    "list_analysis_runtimes",
    "list_software",
    "load_native_guides",
    "native_command_guide",
    "open_execution_prompt",
    "resolve_software_id",
    "search_software_documentation",
    "software_resource_snapshot",
    "validate_native_guides",
]
