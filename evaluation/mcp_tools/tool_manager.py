"""Manage one-file MCP tools from creation through enablement and archival."""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
from pathlib import Path

from .registry import (
    PACKAGE_ROOT,
    TOOL_CONFIG_PATH,
    TOOLS_DIR,
    configuration_errors,
    discover_tools,
    discovered_module_stems,
    load_tool_config,
)


ARCHIVED_TOOLS_DIR = PACKAGE_ROOT / "archived_tools"
DEFAULT_CATALOG_PATH = PACKAGE_ROOT / "TOOL_CATALOG.md"
_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_PLACEHOLDER_TEXT = "before enabling it"


def _validate_name(name: str) -> str:
    if not _NAME_PATTERN.fullmatch(name):
        raise ValueError(
            f"Tool name must be lower snake_case and start with a letter: {name!r}"
        )
    return name


def _save_config(config: dict) -> None:
    temporary = TOOL_CONFIG_PATH.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(TOOL_CONFIG_PATH)


def _validate_source_before_enable(name: str, path: Path) -> None:
    """Reject syntax/contract errors and generated placeholders before enabling."""

    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise ValueError(f"Cannot enable {name!r}: invalid Python syntax: {exc}") from exc
    if _PLACEHOLDER_TEXT in source:
        raise ValueError(
            f"Cannot enable {name!r}: replace the generated NotImplementedError first"
        )

    spec_names: list[str] = []
    has_register = False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "register":
            has_register = True
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "TOOL_SPEC" for target in node.targets):
            continue
        if not isinstance(node.value, ast.Call):
            continue
        for keyword in node.value.keywords:
            if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
                if isinstance(keyword.value.value, str):
                    spec_names.append(keyword.value.value)
    if spec_names != [name]:
        raise ValueError(
            f"Cannot enable {name!r}: TOOL_SPEC.name must be the literal {name!r}"
        )
    if not has_register:
        raise ValueError(f"Cannot enable {name!r}: callable register(mcp) is missing")


def set_enabled(name: str, *, enabled: bool) -> None:
    name = _validate_name(name)
    path = TOOLS_DIR / f"{name}.py"
    if name not in discovered_module_stems() or not path.is_file():
        raise FileNotFoundError(f"Active tool file does not exist: tools/{name}.py")
    if enabled:
        _validate_source_before_enable(name, path)
    config = load_tool_config()
    enabled_names = set(config.get("enabled_tools", []))
    disabled = set(config.get("disabled_tools", []))
    if enabled:
        if "*" not in enabled_names:
            enabled_names.add(name)
        disabled.discard(name)
    else:
        if "*" not in enabled_names:
            enabled_names.discard(name)
        disabled.add(name)
    config["enabled_tools"] = sorted(enabled_names)
    config["disabled_tools"] = sorted(disabled)
    _save_config(config)


def scaffold_tool(
    name: str,
    *,
    description: str,
    category: str,
    backend: str,
    dependencies: tuple[str, ...] = (),
    tags: tuple[str, ...] = (),
    requires_network: bool = False,
    executables: tuple[str, ...] = (),
    side_effects: tuple[str, ...] = (),
) -> Path:
    name = _validate_name(name)
    destination = TOOLS_DIR / f"{name}.py"
    if destination.exists():
        raise FileExistsError(f"Tool already exists: {destination}")
    description_literal = json.dumps(description or f"TODO: describe {name}")
    category_literal = json.dumps(category or "uncategorized")
    backend_literal = json.dumps(backend)
    dependencies_literal = repr(tuple(dependencies))
    tags_literal = repr(tuple(tags))
    executables_literal = repr(tuple(executables))
    side_effects_literal = repr(tuple(side_effects))
    template = f'''"""MCP tool: {name}."""

from __future__ import annotations

from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name={name!r},
    description={description_literal},
    category={category_literal},
    backend={backend_literal},
    dependencies={dependencies_literal},
    tags={tags_literal},
    requires_network={requires_network!r},
    executables={executables_literal},
    side_effects={side_effects_literal},
)


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def {name}(value: str) -> str:
        """Replace this placeholder with validation and the real software call."""

        def call() -> str:
            raise NotImplementedError("Implement {name} before enabling it")

        return execute_traced(TOOL_SPEC.name, {{"value": value}}, call)
'''
    destination.write_text(template, encoding="utf-8")
    # Scaffolds are disabled until the implementation is completed explicitly.
    config = load_tool_config()
    enabled = set(config.get("enabled_tools", []))
    if "*" not in enabled:
        enabled.discard(name)
    config["enabled_tools"] = sorted(enabled)
    disabled = set(config.get("disabled_tools", []))
    disabled.add(name)
    config["disabled_tools"] = sorted(disabled)
    try:
        _save_config(config)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return destination


def archive_tool(name: str, *, confirmed: bool) -> Path:
    name = _validate_name(name)
    if not confirmed:
        raise ValueError("Archiving requires --yes")
    source = TOOLS_DIR / f"{name}.py"
    if not source.is_file():
        raise FileNotFoundError(f"Active tool file does not exist: {source}")
    ARCHIVED_TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    destination = ARCHIVED_TOOLS_DIR / source.name
    if destination.exists():
        raise FileExistsError(f"Archived tool already exists: {destination}")
    config = load_tool_config()
    enabled = set(config.get("enabled_tools", []))
    if "*" not in enabled:
        enabled.discard(name)
    config["enabled_tools"] = sorted(enabled)
    config["disabled_tools"] = sorted(
        set(config.get("disabled_tools", [])) - {name}
    )
    shutil.move(str(source), str(destination))
    try:
        _save_config(config)
    except Exception:
        shutil.move(str(destination), str(source))
        raise
    return destination


def restore_tool(name: str) -> Path:
    name = _validate_name(name)
    source = ARCHIVED_TOOLS_DIR / f"{name}.py"
    destination = TOOLS_DIR / source.name
    if not source.is_file():
        raise FileNotFoundError(f"Archived tool does not exist: {source}")
    if destination.exists():
        raise FileExistsError(f"Active tool already exists: {destination}")
    # Restored tools start disabled until explicitly reviewed and enabled.
    config = load_tool_config()
    enabled = set(config.get("enabled_tools", []))
    if "*" not in enabled:
        enabled.discard(name)
    config["enabled_tools"] = sorted(enabled)
    disabled = set(config.get("disabled_tools", []))
    disabled.add(name)
    config["disabled_tools"] = sorted(disabled)
    shutil.move(str(source), str(destination))
    try:
        _save_config(config)
    except Exception:
        shutil.move(str(destination), str(source))
        raise
    return destination


def generate_catalog(output: Path = DEFAULT_CATALOG_PATH) -> Path:
    records = discover_tools(include_disabled=True, strict=False)
    lines = [
        "# MCP Tool Catalog",
        "",
        "This file is generated from each tool module's `TOOL_SPEC`.",
        "",
        "| Tool | Enabled | Category | Version | Backend | Dependencies | Network | Executables | Side effects | Description | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    def cell(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")

    for record in records:
        spec = record.spec
        lines.append(
            "| {name} | {enabled} | {category} | {version} | {backend} | {deps} | "
            "{network} | {executables} | {side_effects} | {description} | {status} |".format(
                name=cell(spec.name if spec else record.module_stem),
                enabled="yes" if record.enabled else "no",
                category=cell(spec.category if spec else ""),
                version=cell(spec.version if spec else ""),
                backend=cell(spec.backend if spec else ""),
                deps=cell(", ".join(spec.dependencies) if spec else ""),
                network="yes" if spec and spec.requires_network else "no",
                executables=cell(", ".join(spec.executables) if spec else ""),
                side_effects=cell(", ".join(spec.side_effects) if spec else ""),
                description=cell(spec.description if spec else ""),
                status=cell(record.error or "ok"),
            )
        )
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def _print_records(
    *,
    as_json: bool,
    include_disabled: bool,
    fail_on_disabled_errors: bool = False,
) -> int:
    records = discover_tools(include_disabled=include_disabled, strict=False)
    if as_json:
        print(json.dumps([record.as_dict() for record in records], indent=2))
    else:
        print(f"{'TOOL':34s} {'STATE':9s} {'CATEGORY':18s} STATUS")
        for record in records:
            name = record.spec.name if record.spec else record.module_stem
            category = record.spec.category if record.spec else ""
            state = "enabled" if record.enabled else "disabled"
            print(f"{name:34s} {state:9s} {category:18s} {record.error or 'ok'}")
    config_issues = configuration_errors()
    for issue in config_issues:
        print(f"CONFIG ERROR: {issue}")
    module_errors = any(
        record.error and (record.enabled or fail_on_disabled_errors)
        for record in records
    )
    return 1 if module_errors or config_issues else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List automatically discovered tools")
    list_parser.add_argument("--json", action="store_true")
    list_parser.add_argument("--enabled-only", action="store_true")

    subparsers.add_parser("validate", help="Validate metadata, imports, names, and register()")

    scaffold = subparsers.add_parser("scaffold", help="Create one disabled tool file")
    scaffold.add_argument("name")
    scaffold.add_argument("--description", default="")
    scaffold.add_argument("--category", default="uncategorized")
    scaffold.add_argument("--backend", default="")
    scaffold.add_argument(
        "--dependency",
        action="append",
        default=[],
        help="Python/runtime dependency; repeat for multiple values",
    )
    scaffold.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Search/catalog tag; repeat for multiple values",
    )
    scaffold.add_argument(
        "--network",
        action="store_true",
        help="Declare that the tool requires network access",
    )
    scaffold.add_argument(
        "--executable",
        action="append",
        default=[],
        help="Required external executable; repeat for multiple values",
    )
    scaffold.add_argument(
        "--side-effect",
        action="append",
        default=[],
        help="Declared file/process/network side effect; repeat for multiple values",
    )

    enable = subparsers.add_parser("enable", help="Enable an implemented tool")
    enable.add_argument("name")
    disable = subparsers.add_parser("disable", help="Disable a tool without deleting it")
    disable.add_argument("name")

    archive = subparsers.add_parser("archive", help="Move a tool out of auto-discovery")
    archive.add_argument("name")
    archive.add_argument("--yes", action="store_true")
    restore = subparsers.add_parser("restore", help="Restore an archived tool as disabled")
    restore.add_argument("name")

    catalog = subparsers.add_parser("catalog", help="Generate Markdown from TOOL_SPEC metadata")
    catalog.add_argument("--output", type=Path, default=DEFAULT_CATALOG_PATH)

    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            return _print_records(
                as_json=args.json,
                include_disabled=not args.enabled_only,
            )
        if args.command == "validate":
            result = _print_records(
                as_json=False,
                include_disabled=True,
                fail_on_disabled_errors=True,
            )
            if result == 0:
                print("All discovered tool modules and configuration are valid.")
            return result
        if args.command == "scaffold":
            print(
                scaffold_tool(
                    args.name,
                    description=args.description,
                    category=args.category,
                    backend=args.backend,
                    dependencies=tuple(args.dependency),
                    tags=tuple(args.tag),
                    requires_network=args.network,
                    executables=tuple(args.executable),
                    side_effects=tuple(args.side_effect),
                )
            )
            return 0
        if args.command == "enable":
            set_enabled(args.name, enabled=True)
            print(f"Enabled: {args.name}")
            return 0
        if args.command == "disable":
            set_enabled(args.name, enabled=False)
            print(f"Disabled: {args.name}")
            return 0
        if args.command == "archive":
            print(archive_tool(args.name, confirmed=args.yes))
            return 0
        if args.command == "restore":
            print(restore_tool(args.name))
            return 0
        if args.command == "catalog":
            print(generate_catalog(args.output))
            return 0
    except (FileNotFoundError, FileExistsError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
