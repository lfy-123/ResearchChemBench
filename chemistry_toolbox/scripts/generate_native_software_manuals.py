#!/usr/bin/env python3
"""Generate structured first-party manuals for every native software guide."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
for path in (TOOLBOX_ROOT / "src", PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.catalog import backend_specs


GUIDES_PATH = TOOLBOX_ROOT / "config" / "native_software_guides.yaml"
STATUS_PATH = TOOLBOX_ROOT / "config" / "requested_software_status.json"
DOCS_ROOT = TOOLBOX_ROOT / "native_software_docs"
HAND_WRITTEN_SOFTWARE = {"orca", "gaussian", "crest", "vasp", "lobster"}


def normalize_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")


def detected_versions() -> dict[str, list[str]]:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    result: dict[str, list[str]] = {}
    for item in status.get("software", []):
        software_id = normalize_id(str(item.get("name") or ""))
        versions: list[str] = []
        verification = item.get("verification") or {}
        for module in (verification.get("modules") or {}).values():
            if module.get("version"):
                versions.append(str(module["version"]))
        for smoke in (verification.get("runtime_smokes") or {}).values():
            if isinstance(smoke, dict) and smoke.get("version"):
                versions.append(str(smoke["version"]))
        result[software_id] = list(dict.fromkeys(versions))
    return result


def render_manual(
    software_id: str,
    guide: dict,
    *,
    runtime: str,
    versions: list[str],
) -> str:
    commands = dict(guide.get("commands") or {})
    aliases = [software_id.replace("_", " "), *(guide.get("aliases") or [])]
    required_files = list(
        dict.fromkeys(
            str(item)
            for command in commands.values()
            for item in command.get("required_files") or []
        )
    )
    lines = [
        "---",
        f"software_id: {software_id}",
        f"versions: {json.dumps(versions)}",
        "topics: [index, quickstart, native-execution, resources, convergence, troubleshooting]",
        f"aliases: {json.dumps(aliases)}",
        f"inputs: {json.dumps(required_files)}",
        'outputs: ["stdout.log", "stderr.log", "software-declared output files"]',
        "last_smoke_tested: null",
        "generated_from: chemistry_toolbox/config/native_software_guides.yaml",
        "---",
        f"# {software_id.replace('_', ' ').title()} Native Execution",
        "",
        "## Purpose and supported version",
        str(guide.get("purpose") or "Use the configured native executable for an Agent-authored task."),
        "",
        f"Configured runtime: `{runtime}`. Detected versions: "
        + (", ".join(f"`{item}`" for item in versions) if versions else "not recorded; inspect the executable before relying on version-specific syntax."),
        "",
        "## Working directory and staging",
        "The execution layer creates an isolated job directory and runs the exact argv vector there without a shell. Stage every referenced input with the exact filename used by the command or input deck. Relative paths resolve from the job directory, not from the task workspace root. Use `stdin_target` only when the command input mode below requires stdin.",
        "",
        "## Commands",
    ]
    for executable, command in commands.items():
        lines.extend(
            [
                "",
                f"### `{executable}`",
                f"Synopsis: `{command.get('synopsis') or executable}`",
                "",
                f"Input mode: `{command.get('input_mode') or 'arguments'}`.",
                "",
                "Required staged files: "
                + (", ".join(f"`{item}`" for item in command.get("required_files") or []) or "none declared by the mechanical guide."),
                "",
                f"Output behavior: {command.get('output_behavior') or 'Inspect stdout, stderr, and files created in the job directory.'}",
                "",
                "Example argv: `"
                + " ".join([executable, *(str(item) for item in command.get("example_arguments") or [])])
                + "`.",
            ]
        )
        notes = command.get("notes") or []
        if notes:
            lines.extend(["", "Command-specific cautions:"])
            lines.extend(f"- {item}" for item in notes)
    guide_notes = guide.get("notes") or []
    if guide_notes:
        lines.extend(["", "## Software-specific cautions"])
        lines.extend(f"- {item}" for item in guide_notes)
    lines.extend(
        [
            "",
            "## Resource mapping",
            "Set `resource_limits.cpu_cores`, `memory_mb`, `gpu_count`, and `walltime_seconds` explicitly. Keep software thread, MPI, memory, and GPU settings within those requested limits. The Supervisor enforces the per-job memory limit, CPU affinity, evaluator-wide concurrent reservations, walltime, cancellation, and process-group cleanup.",
            "",
            "## Normal termination and scientific convergence",
            "Exit code zero only establishes process completion. Inspect stdout, stderr, and the software's primary output for fatal errors and its documented normal-termination marker. Scientific convergence is task-specific: verify the requested optimization, electronic, ionic, frequency, dynamics, fitting, or projection criteria and confirm that every required result file is present and parseable. If the toolbox has no software-specific parser for this task, the status remains `not_checked` rather than inferring convergence from the exit code.",
            "",
            "## Common immediate failures",
            "- A referenced file was not staged with the exact target name.",
            "- The command was authored for a different software version.",
            "- An input deck contains an invalid keyword, section delimiter, or path.",
            "- Internal thread, MPI, memory, or GPU settings exceed the declared resource limits.",
            "- The process exits successfully but the main output reports a scientific or parsing failure.",
            "",
            "## Preflight checklist",
            "- Confirm the installed version and executable returned by `inspect_software`.",
            "- Read this manual and any referenced official version documentation.",
            "- Stage every input and nested dependency using the exact job-local filename.",
            "- Declare a calculation intent when the task has a convergence contract.",
            "- Match software parallelism and memory settings to `resource_limits`.",
            "- Run `validate_native_job` before submission.",
            "- After execution, inspect all status axes and the required output artifacts.",
            "",
        ]
    )
    return "\n".join(lines)


def generated_manuals() -> dict[Path, str]:
    guides = yaml.safe_load(GUIDES_PATH.read_text(encoding="utf-8"))["software"]
    specifications = backend_specs()
    versions = detected_versions()
    result: dict[Path, str] = {}
    for software_id, guide in sorted(guides.items()):
        if software_id in HAND_WRITTEN_SOFTWARE:
            continue
        runtime = str(
            guide.get("runtime")
            or (specifications.get(software_id).runtime if specifications.get(software_id) else "configured-runtime")
        )
        path = DOCS_ROOT / software_id / "INDEX.md"
        result[path] = render_manual(
            software_id,
            guide,
            runtime=runtime,
            versions=versions.get(software_id, []),
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale: list[str] = []
    for path, content in generated_manuals().items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(PROJECT_ROOT)))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    if stale:
        print("Generated native manuals are missing or stale:")
        print("\n".join(stale))
        return 1
    print(f"Native manual coverage: {len(generated_manuals()) + len(HAND_WRITTEN_SOFTWARE)} software entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
