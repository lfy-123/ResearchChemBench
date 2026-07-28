#!/usr/bin/env python3
"""Generate detailed, structured native-software manuals and call examples."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from pathlib import Path
from typing import Any

import yaml


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
for path in (TOOLBOX_ROOT / "src", PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.catalog import backend_specs


GUIDES_PATH = TOOLBOX_ROOT / "config" / "native_software_guides.yaml"
PROFILES_PATH = TOOLBOX_ROOT / "config" / "native_software_manual_profiles.yaml"
SMOKE_RESULTS_PATH = TOOLBOX_ROOT / "evidence" / "native_interface_smoke" / "latest.json"
DOCS_ROOT = TOOLBOX_ROOT / "native_software_docs"
HAND_WRITTEN_SOFTWARE = {"orca", "gaussian", "crest", "vasp", "lobster"}
STANDARD_FILES = ("INDEX.md", "QUICKSTART.md", "COMMON_TASKS.md", "TROUBLESHOOTING.md")
EXAMPLE_INPUT_CONTENTS = {
    "multiwfn": {"interface_smoke.stdin": "\n"},
    "packmol": {"interface_smoke.stdin": "\n"},
    "siesta": {"interface_smoke.stdin": "\n"},
    "nequip": {"interface_smoke.yaml": "{}\n"},
    "pysisyphus": {
        "interface_smoke.yaml": (
            "geom:\n  type: cart\n  fn: interface_smoke.xyz\n"
            "calc:\n  type: xtb\n  charge: 0\n  mult: 1\n  gfn: 2\n  pal: 1\n"
            "opt:\n  type: rfo\n  max_cycles: 5\n"
        ),
        "interface_smoke.xyz": "2\nH2 interface smoke\nH 0.0 0.0 0.0\nH 0.0 0.0 0.75\n",
    },
}


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True)


def _front_matter(
    software_id: str,
    profile: dict[str, Any],
    *,
    topics: list[str],
    inputs: list[str] | None = None,
    outputs: list[str] | None = None,
) -> str:
    smoke = smoke_results().get(software_id, {})
    tested = smoke.get("tested_at", "null")
    if tested != "null":
        tested = json.dumps(str(tested)[:10])
    return "\n".join(
        [
            "---",
            f"software_id: {software_id}",
            f"versions: {_json([str(profile['installed_version'])])}",
            f"topics: {_json(topics)}",
            f"aliases: {_json([profile['display_name'], software_id.replace('_', ' ')])}",
            f"inputs: {_json(inputs if inputs is not None else profile.get('inputs', []))}",
            f"outputs: {_json(outputs if outputs is not None else profile.get('outputs', []))}",
            f"last_smoke_tested: {tested}",
            "generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml",
            "---",
        ]
    )


def smoke_results() -> dict[str, dict[str, Any]]:
    if not SMOKE_RESULTS_PATH.is_file():
        return {}
    payload = json.loads(SMOKE_RESULTS_PATH.read_text(encoding="utf-8"))
    return {str(item["software_id"]): item for item in payload.get("software", [])}


def load_sources() -> tuple[dict[str, Any], dict[str, Any]]:
    guides = yaml.safe_load(GUIDES_PATH.read_text(encoding="utf-8"))["software"]
    profiles = yaml.safe_load(PROFILES_PATH.read_text(encoding="utf-8"))["software"]
    if set(guides) != set(profiles):
        missing = sorted(set(guides) - set(profiles))
        extra = sorted(set(profiles) - set(guides))
        raise ValueError(f"Manual profile mismatch; missing={missing}, extra={extra}")
    return guides, profiles


def _runtime(software_id: str, guide: dict[str, Any]) -> str:
    specifications = backend_specs()
    specification = specifications.get(software_id)
    return str(guide.get("runtime") or (specification.runtime if specification else "configured-runtime"))


def _command_table(guide: dict[str, Any]) -> list[str]:
    lines = [
        "| Executable | Input mode | Native invocation | Required staged inputs |",
        "|---|---|---|---|",
    ]
    for executable, command in (guide.get("commands") or {}).items():
        argv = " ".join([executable, *(str(item) for item in command.get("example_arguments") or [])])
        required = ", ".join(f"`{item}`" for item in command.get("required_files") or []) or "None"
        lines.append(
            f"| `{executable}` | `{command.get('input_mode', 'arguments')}` | `{argv}` | {required} |"
        )
    return lines


def _first_command(guide: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    return next(iter((guide.get("commands") or {}).items()))


def _specific_targets(command: dict[str, Any]) -> list[str]:
    arguments = [str(item) for item in command.get("example_arguments") or []]
    candidates: list[str] = []
    for item in command.get("required_files") or []:
        text = str(item)
        if " " not in text and not any(char in text for char in "<>[]"):
            candidates.append(text)
    for item in arguments:
        if item.startswith("-") or item.replace(".", "", 1).isdigit() or item.startswith("<"):
            continue
        if "." in Path(item).name and item not in candidates:
            candidates.append(item)
    return candidates


def _request_template(software_id: str, guide: dict[str, Any]) -> dict[str, Any]:
    executable, command = _first_command(guide)
    targets = _specific_targets(command)
    request: dict[str, Any] = {
        "software_id": software_id,
        "executable": executable,
        "arguments": [str(item) for item in command.get("example_arguments") or []],
        "staged_inputs": [
            {"source_path": f"workspace_inputs/{target}", "target_path": target}
            for target in targets
        ],
        "resource_limits": {
            "cpu_cores": 1,
            "memory_mb": 2048,
            "gpu_count": 0,
        },
    }
    mode = command.get("input_mode")
    if mode in {"stdin_file", "arguments_and_stdin_file"}:
        request["stdin_target"] = targets[-1] if targets else "input.in"
    return request


def render_index(software_id: str, guide: dict[str, Any], profile: dict[str, Any]) -> str:
    name = profile["display_name"]
    status = profile["operational_status"]
    lines = [
        _front_matter(software_id, profile, topics=["index", "navigation", "capabilities"]),
        f"# {name} Native Software Guide",
        "",
        "## Installed software",
        f"- Installed version: `{profile['installed_version']}`.",
        f"- Operational status: `{status}`.",
        f"- Configured runtime: `{_runtime(software_id, guide)}`.",
        f"- Primary use: {profile['primary_task']}.",
        "",
        "## When to use this interface",
        str(guide.get("purpose") or profile["primary_task"]) + " The native layer is appropriate when the Agent must author the software input or select version-specific options that are not represented by a preset Action.",
        "",
        "## Documentation map",
        "- `QUICKSTART.md`: complete staging, command, resource, submission, and collection flow.",
        "- `COMMON_TASKS.md`: supported calculation families, input responsibilities, outputs, and validation states.",
        "- `TROUBLESHOOTING.md`: high-frequency failure signatures, causes, fixes, and a pre-submission checklist.",
        "- `examples/interface_smoke/`: the exact native command, toolbox request, and latest interface-smoke result.",
        "- Additional topic files in this directory contain software-specific scientific mechanics where available.",
        "",
        "## Supported command entries",
        *_command_table(guide),
        "",
        "## Supported task families",
        *[f"- {item}." for item in profile.get("task_types", [])],
        "",
        "## Required knowledge before submission",
        "The toolbox does not select a scientific method, force field, pseudopotential, basis, database, training set, convergence threshold, or workflow ordering. The Agent must obtain those choices from the task, a paper, or an authoritative source and then author a complete input.",
        "",
        "## Official references",
        *[f"- {url}" for url in profile.get("official_docs", [])],
        "",
        "## Test interpretation",
        "An interface smoke proves that the configured executable can be resolved and started through `submit_native_job`. A scientific smoke additionally requires a valid input, normal software termination, task-specific convergence, and parseable expected artifacts. The two levels are recorded separately and must not be conflated.",
        "",
    ]
    if status == "placeholder":
        lines.extend(
            [
                "## Availability restriction",
                "This entry is a placeholder in the current environment. Do not submit it until the missing licensed host or executable is installed and inspected.",
                "",
            ]
        )
    return "\n".join(lines)


def render_quickstart(software_id: str, guide: dict[str, Any], profile: dict[str, Any]) -> str:
    name = profile["display_name"]
    executable, command = _first_command(guide)
    native = " ".join([executable, *(str(item) for item in command.get("example_arguments") or [])])
    request = _request_template(software_id, guide)
    required = command.get("required_files") or []
    lines = [
        _front_matter(software_id, profile, topics=["quickstart", "staging", "submission", "resources"]),
        f"# {name} Quickstart",
        "",
        "## Complete invocation flow",
        "1. Call `inspect_software` and confirm the executable, installed version, runtime, and documentation topics.",
        "2. Author the smallest scientifically meaningful input for the selected task and installed version.",
        "3. Put every source file under the evaluation workspace and map it to the exact job-local target expected by the input deck.",
        "4. Set explicit CPU, total memory, GPU, and walltime limits. Keep all software-internal parallel settings within those limits.",
        "5. Call `validate_native_job`; repair every error before submitting.",
        "6. Call `submit_native_job`, poll `get_execution_job`, and finally call `collect_execution_job`.",
        "7. Check process, software, convergence, artifact, and scientific-validation axes independently.",
        "",
        "## Working directory contract",
        "The runner creates an isolated job directory and executes the resolved binary there without a shell. Relative paths in arguments and input files resolve from that directory, not from the benchmark workspace root. `source_path` is workspace-relative; `target_path` is job-relative. Stage nested dependencies explicitly. The runner captures `request.json`, `stdout.log`, `stderr.log`, status, hashes, and collected artifacts.",
        "",
        "## Input mode",
        f"The primary executable is `{executable}` and its input mode is `{command.get('input_mode', 'arguments')}`.",
        "Required inputs: " + (", ".join(f"`{item}`" for item in required) if required else "no fixed file is declared for this command") + ".",
        f"Output behavior: {command.get('output_behavior', 'Inspect captured logs and files created in the job directory.')}",
        "",
        "## Native command template",
        "```bash",
        native,
        "```",
        "Run that command only inside a directory containing the exact referenced files. The toolbox resolves the executable itself; do not embed shell redirection, pipes, `cd`, or environment activation in `arguments`.",
        "",
        "## Toolbox submission template",
        "```json",
        json.dumps(request, indent=2),
        "```",
        "The paths under `workspace_inputs/` are illustrative workspace-relative sources. Replace them with real files and keep the target names synchronized with the input deck.",
        "",
        "## stdin, arguments, and fixed files",
        "- For `arguments`, put each token in `arguments`; never pass one shell command string.",
        "- For `stdin_file`, stage the input and set `stdin_target`; do not put `< input` in `arguments`.",
        "- For `arguments_and_stdin_file`, provide both the positional file arguments and `stdin_target`.",
        "- For `fixed_files`, stage every required filename exactly and normally leave `arguments` empty.",
        "",
        "## Resource mapping",
        profile["resource_notes"],
        "`resource_limits.memory_mb` is total memory for the entire process group, not memory per MPI rank. `cpu_cores` is the allocation ceiling. Software thread or rank controls must not exceed it. Walltime is enforced by the Supervisor; a timeout is distinct from software non-convergence.",
        "",
        "## Collection checklist",
        "- `request_status=accepted` confirms only that the interface accepted the request.",
        "- `process_status=completed` confirms only process exit code zero.",
        "- `software_status=normal` requires a recognized normal end and no fatal message when a parser exists.",
        "- `convergence_status` must match the requested task type; an SCF marker alone cannot validate an optimization or frequency job.",
        "- `artifact_status=valid` requires all declared results to exist and parse.",
        "- The Judger, not the execution layer, evaluates whether the results support the requested scientific conclusion.",
        "",
    ]
    if software_id == "gaussian":
        lines.extend(
            [
                "## Required sections",
                "Place Link 0 commands first, followed by one route section beginning with `#`. A blank line must separate the route from a non-empty title, another blank line must separate the title from charge and multiplicity, coordinates follow, and the input must end with a final blank line. Each Link1 segment repeats the required structure unless it explicitly and validly reads the checkpoint.",
                "",
            ]
        )
    return "\n".join(lines)


def render_common_tasks(software_id: str, guide: dict[str, Any], profile: dict[str, Any]) -> str:
    lines = [
        _front_matter(software_id, profile, topics=["common-tasks", "inputs", "outputs", "convergence"]),
        f"# {profile['display_name']} Common Tasks",
        "",
        "## Appropriate calculation families",
        *[f"- **{item.title()}**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation." for item in profile.get("task_types", [])],
        "",
        "## Minimum input responsibilities",
        *[f"- `{item}`" for item in profile.get("inputs", [])],
        "",
        "A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.",
        "",
        "## Expected output families",
        *[f"- `{item}`" for item in profile.get("outputs", [])],
        "",
        "Only collect outputs produced by the same job or by explicitly linked parent jobs. Do not combine checkpoints, force constants, trajectories, pseudopotentials, wavefunctions, or databases from unrelated calculations.",
        "",
        "## State-specific validation",
        "| State | Required evidence | Not sufficient |",
        "|---|---|---|",
        "| Process completed | Exit code zero and Supervisor did not cancel or time out | A submitted job ID |",
        "| Software normal | Program-specific normal marker and absence of fatal diagnostics | Exit code zero alone |",
        "| Electronic convergence | Requested SCF or electronic tolerance reached | A printed energy from an unconverged cycle |",
        "| Geometry convergence | Optimization stopping criteria reached for the requested degrees of freedom | SCF convergence at the last geometry |",
        "| Frequency completion | Hessian/frequencies finished and modes were parsed | Optimization completion alone |",
        "| Transition-state candidate | Optimization converged and exactly the intended imaginary mode was verified | One negative number without mode inspection |",
        "| Dynamics completion | Requested steps completed with acceptable stability diagnostics | Creation of a partial trajectory |",
        "| Artifact validity | Required files exist, are non-empty, and can be parsed | Files with expected names only |",
        "",
        "## Software-specific end markers",
        *[f"- `{marker}`" for marker in profile.get("normal_markers", [])],
        "",
        "## Scientific convergence notes",
        profile["convergence_notes"],
        "",
        "## Version-specific caution",
        f"These mechanics target the installed `{profile['installed_version']}` environment. Verify keywords and file formats against the official references before reusing an input written for another release.",
        "",
        "## Minimal-example policy",
        "The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.",
        "",
    ]
    for executable, command in (guide.get("commands") or {}).items():
        lines.extend(
            [
                f"## Command: `{executable}`",
                f"- Synopsis: `{command.get('synopsis', executable)}`.",
                f"- Input mode: `{command.get('input_mode', 'arguments')}`.",
                "- Required files: " + (", ".join(f"`{item}`" for item in command.get("required_files") or []) or "none declared") + ".",
                f"- Output behavior: {command.get('output_behavior', 'Inspect stdout, stderr, and generated files.')}",
                *[f"- Caution: {note}" for note in command.get("notes") or []],
                "",
            ]
        )
    return "\n".join(lines)


def render_troubleshooting(software_id: str, profile: dict[str, Any]) -> str:
    lines = [
        _front_matter(software_id, profile, topics=["troubleshooting", "errors", "preflight"]),
        f"# {profile['display_name']} Troubleshooting",
        "",
        "## Diagnose in this order",
        "1. Confirm that `inspect_software` resolves the expected executable and version.",
        "2. Read the first fatal message in `stderr.log` or the primary software output; later messages are often consequences.",
        "3. Verify staged target names, input-relative paths, file encodings, line endings, and required blank sections.",
        "4. Verify task syntax against the installed version, then check method and data compatibility.",
        "5. Compare internal MPI, thread, memory, scratch, and GPU settings with the declared job resources.",
        "6. Only after syntax and staging pass, investigate numerical convergence or increase resources.",
        "",
        "## Known failures and repairs",
        "| Symptom | Likely cause | Corrective action |",
        "|---|---|---|",
    ]
    for symptom, cause, fix in profile.get("known_errors", []):
        lines.append(f"| {symptom} | {cause} | {fix} |")
    if software_id == "lobster":
        lines.extend(
            [
                "",
                "## Projection quality",
                "High charge spilling or high total spilling is a scientific validation problem even when LOBSTER terminates normally. Check basis selection, band coverage, PAW compatibility, and upstream VASP settings before interpreting COHP, COOP, COBI, DOS, or charge results. Record the spilling value and any threshold chosen for the task.",
            ]
        )
    lines.extend(
        [
            "",
            "## Path and staging failures",
            "A source file existing in the benchmark workspace does not make it visible to the native process. Every dependency must be declared in `staged_inputs`. The content of an input deck must reference the staged `target_path`, not its original workspace path. Fixed-name programs are case-sensitive. Never assume the process starts in the task workspace.",
            "",
            "## Resource failures",
            profile["resource_notes"],
            "If the Supervisor reports `memory_limit_exceeded`, reduce software parallelism or request a justified larger total allocation. If it reports timeout, inspect whether the software was progressing and whether the requested task can finish within the remaining evaluation lifetime. Resource increases do not repair malformed input.",
            "",
            "## False-success prevention",
            "Do not accept a zero exit code when the main output contains `ERROR`, `FATAL`, an abort marker, non-convergence, or missing-result diagnostics. Likewise, do not promote an electronic convergence marker to geometry, frequency, transition-state, dynamics, or projection success. Preserve the independent status axes in the final report.",
            "",
            "## Pre-submission checklist",
            "- Installed executable and version inspected.",
            "- Official syntax checked for the intended calculation family.",
            "- Input is complete and uses English/ASCII-safe filenames where possible.",
            "- Every referenced file is staged to the exact target name.",
            "- stdin and argument modes match the Catalog contract.",
            "- Charge, multiplicity, periodicity, units, atom ordering, and upstream provenance are consistent.",
            "- CPU, total memory, per-rank/per-core memory, GPU, scratch, and walltime agree.",
            "- `validate_native_job` returns no errors.",
            "- Required outputs and task-specific success criteria are declared before execution.",
            "",
        ]
    )
    return "\n".join(lines)


def render_example_files(software_id: str, guide: dict[str, Any], profile: dict[str, Any]) -> dict[Path, str]:
    root = DOCS_ROOT / software_id / "examples" / "interface_smoke"
    result = smoke_results().get(software_id, {})
    executable, command = _first_command(guide)
    smoke_request = json.loads(json.dumps(result.get("request") or {
        "software_id": software_id,
        "executable": executable,
        "arguments": ["--help"],
        "staged_inputs": [],
        "resource_limits": {"cpu_cores": 1, "memory_mb": 1024, "gpu_count": 0},
    }))
    local_inputs = EXAMPLE_INPUT_CONTENTS.get(software_id, {})
    for staged in smoke_request.get("staged_inputs") or []:
        target = staged.get("target_path")
        if target in local_inputs:
            staged["source_path"] = str(
                (root / target).relative_to(PROJECT_ROOT)
            )
    native_argv = [smoke_request["executable"], *(smoke_request.get("arguments") or [])]
    native_line = shlex.join(native_argv)
    if smoke_request.get("stdin_target"):
        native_line += f" < {shlex.quote(smoke_request['stdin_target'])}"
    files = {
        root / "native_command.sh": "#!/usr/bin/env bash\nset -euo pipefail\n" + native_line + "\n",
        root / "submit_request.json": json.dumps(smoke_request, indent=2, sort_keys=True) + "\n",
        root / "smoke_result.json": json.dumps(
            result
            or {
                "software_id": software_id,
                "test_level": "not_run",
                "status": "pending",
                "reason": "Run chemistry_toolbox/scripts/run_native_interface_smokes.py before relying on this example.",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    }
    for target, content in local_inputs.items():
        files[root / target] = content
    return files


def generated_manuals() -> dict[Path, str]:
    guides, profiles = load_sources()
    result: dict[Path, str] = {}
    for software_id in sorted(guides):
        guide = guides[software_id]
        profile = profiles[software_id]
        if profile["operational_status"] == "placeholder":
            continue
        renderers = {
            "INDEX.md": render_index(software_id, guide, profile),
            "QUICKSTART.md": render_quickstart(software_id, guide, profile),
            "COMMON_TASKS.md": render_common_tasks(software_id, guide, profile),
            "TROUBLESHOOTING.md": render_troubleshooting(software_id, profile),
        }
        for filename, content in renderers.items():
            path = DOCS_ROOT / software_id / filename
            result[path] = content
        result.update(render_example_files(software_id, guide, profile))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = generated_manuals()
    stale: list[str] = []
    for path, content in generated.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(PROJECT_ROOT)))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if path.name == "native_command.sh":
            path.chmod(0o755)
    if stale:
        print("Generated native manuals or examples are missing or stale:")
        print("\n".join(stale))
        return 1
    detailed = len(load_sources()[0]) - 2
    print(f"Detailed native manual coverage: {detailed}; generated files: {len(generated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
