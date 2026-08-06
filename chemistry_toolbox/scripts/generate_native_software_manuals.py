#!/usr/bin/env python3
"""Generate detailed, structured native-software manuals and call examples."""

from __future__ import annotations

import argparse
import json
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

from chemistry_toolbox.src.catalog import backend_specs


GUIDES_PATH = TOOLBOX_ROOT / "config" / "native_software_guides.yaml"
PROFILES_PATH = TOOLBOX_ROOT / "config" / "native_software_manual_profiles.yaml"
EXAMPLE_CONTRACTS_PATH = TOOLBOX_ROOT / "config" / "native_software_example_contracts.yaml"
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
            "generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml",
            "---",
        ]
    )


def smoke_results() -> dict[str, dict[str, Any]]:
    if not SMOKE_RESULTS_PATH.is_file():
        return {}
    payload = json.loads(SMOKE_RESULTS_PATH.read_text(encoding="utf-8"))
    return {str(item["software_id"]): item for item in payload.get("software", [])}


def load_sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    guides = yaml.safe_load(GUIDES_PATH.read_text(encoding="utf-8"))["software"]
    profiles = yaml.safe_load(PROFILES_PATH.read_text(encoding="utf-8"))["software"]
    contracts = yaml.safe_load(EXAMPLE_CONTRACTS_PATH.read_text(encoding="utf-8"))["software"]
    if set(guides) != set(profiles) or set(guides) != set(contracts):
        missing = sorted(set(guides) - set(profiles))
        extra = sorted(set(profiles) - set(guides))
        contract_missing = sorted(set(guides) - set(contracts))
        contract_extra = sorted(set(contracts) - set(guides))
        raise ValueError(
            "Manual source mismatch; "
            f"profiles_missing={missing}, profiles_extra={extra}, "
            f"contracts_missing={contract_missing}, contracts_extra={contract_extra}"
        )
    validate_sources(guides, profiles, contracts)
    return guides, profiles, contracts


def _parallel_width(arguments: list[str]) -> int:
    width = 1
    index = 0
    while index < len(arguments):
        item = arguments[index]
        if item.startswith("+p") and item[2:].isdigit():
            width = max(width, int(item[2:]))
        elif item in {"--T", "-n", "-nt", "--threads", "--jobs", "-np"}:
            if index + 1 < len(arguments) and arguments[index + 1].isdigit():
                width = max(width, int(arguments[index + 1]))
                index += 1
        index += 1
    return width


def validate_sources(
    guides: dict[str, Any], profiles: dict[str, Any], contracts: dict[str, Any]
) -> None:
    errors: list[str] = []
    for software_id, guide in guides.items():
        profile = profiles[software_id]
        if not isinstance(profile.get("installed_version"), str):
            errors.append(f"{software_id}: installed_version must be a quoted string")
        for marker in profile.get("normal_markers") or []:
            if not isinstance(marker, str):
                errors.append(f"{software_id}: normal_markers must contain strings only")
        guide_commands = guide.get("commands") or {}
        contract_commands = (contracts[software_id] or {}).get("commands") or {}
        if set(guide_commands) != set(contract_commands):
            errors.append(
                f"{software_id}: command contract mismatch; "
                f"missing={sorted(set(guide_commands) - set(contract_commands))}, "
                f"extra={sorted(set(contract_commands) - set(guide_commands))}"
            )
            continue
        for executable, command in guide_commands.items():
            contract = contract_commands[executable]
            arguments = contract.get("arguments")
            inputs = contract.get("inputs")
            outputs = contract.get("outputs")
            resources = contract.get("resource_limits")
            if not isinstance(arguments, list) or not all(
                isinstance(item, str) for item in arguments
            ):
                errors.append(f"{software_id}/{executable}: arguments must be strings")
                continue
            if not isinstance(inputs, list) or not all(
                isinstance(item, str) and item for item in inputs
            ):
                errors.append(f"{software_id}/{executable}: inputs must be non-empty strings")
                continue
            if not isinstance(outputs, list) or not all(
                isinstance(item, str) and item for item in outputs
            ):
                errors.append(f"{software_id}/{executable}: outputs must be non-empty strings")
                continue
            overlap = sorted(set(inputs) & set(outputs))
            if overlap:
                errors.append(
                    f"{software_id}/{executable}: inputs and outputs overlap: {overlap}"
                )
            if not isinstance(resources, dict) or not all(
                isinstance(resources.get(name), int)
                for name in ("cpu_cores", "memory_mb", "gpu_count")
            ):
                errors.append(f"{software_id}/{executable}: invalid resource_limits")
                continue
            parallel_width = _parallel_width(arguments)
            if parallel_width > int(resources["cpu_cores"]):
                errors.append(
                    f"{software_id}/{executable}: command requests {parallel_width} workers "
                    f"but resource contract declares {resources['cpu_cores']} CPU cores"
                )
            enabled = command.get("enabled", True) is True
            if contract.get("enabled", True) is not enabled:
                errors.append(f"{software_id}/{executable}: enabled state differs from guide")
            if contract.get("example_kind") not in {
                "scientific_template",
                "interface_template",
                "disabled",
                "placeholder",
            }:
                errors.append(f"{software_id}/{executable}: invalid example_kind")
            stdin_target = contract.get("stdin_target")
            if stdin_target is not None and stdin_target not in inputs:
                errors.append(
                    f"{software_id}/{executable}: stdin_target must be a declared input"
                )
    if errors:
        raise ValueError("Invalid native software manual sources:\n" + "\n".join(errors))


def _runtime(software_id: str, guide: dict[str, Any]) -> str:
    specifications = backend_specs()
    specification = specifications.get(software_id)
    return str(guide.get("runtime") or (specification.runtime if specification else "configured-runtime"))


def _typed_actions(software_id: str) -> tuple[str, ...]:
    specification = backend_specs().get(software_id)
    if specification is None:
        return ()
    return tuple(str(action_id) for action_id in specification.capabilities)


def _command_table(guide: dict[str, Any], contracts: dict[str, Any]) -> list[str]:
    lines = [
        "| Executable | Input mode | Native invocation | Required staged inputs |",
        "|---|---|---|---|",
    ]
    for executable, command in (guide.get("commands") or {}).items():
        contract = contracts["commands"][executable]
        if contract.get("enabled", True) is not True:
            continue
        argv = " ".join([executable, *contract["arguments"]])
        required = ", ".join(f"`{item}`" for item in contract["inputs"]) or "None"
        lines.append(
            f"| `{executable}` | `{command.get('input_mode', 'arguments')}` | `{argv}` | {required} |"
        )
    return lines


def _first_command(
    guide: dict[str, Any], contracts: dict[str, Any]
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    for executable, command in (guide.get("commands") or {}).items():
        contract = contracts["commands"][executable]
        if command.get("enabled", True) is True and contract.get("enabled", True) is True:
            return executable, command, contract
    raise ValueError("No enabled native command is available for this software entry")


def _request_template(
    software_id: str, guide: dict[str, Any], contracts: dict[str, Any]
) -> dict[str, Any]:
    executable, _command, contract = _first_command(guide, contracts)
    request: dict[str, Any] = {
        "software_id": software_id,
        "executable": executable,
        "arguments": list(contract["arguments"]),
        "staged_inputs": [
            {"source_path": f"workspace_inputs/{target}", "target_path": target}
            for target in contract["inputs"]
        ],
        "resource_limits": dict(contract["resource_limits"]),
    }
    if contract.get("stdin_target"):
        request["stdin_target"] = contract["stdin_target"]
    return request


def render_index(
    software_id: str,
    guide: dict[str, Any],
    profile: dict[str, Any],
    contracts: dict[str, Any],
) -> str:
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
        *_command_table(guide, contracts),
        "",
        "## Supported task families",
        *[f"- {item}." for item in profile.get("task_types", [])],
        "",
        "## Layer 1 typed Actions",
        *(
            [f"- `{action_id}`." for action_id in _typed_actions(software_id)]
            or ["- No typed Action is registered. Use the reviewed native command layer or the documented programmable runtime."]
        ),
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


def render_quickstart(
    software_id: str,
    guide: dict[str, Any],
    profile: dict[str, Any],
    contracts: dict[str, Any],
) -> str:
    name = profile["display_name"]
    executable, command, contract = _first_command(guide, contracts)
    native = " ".join([executable, *contract["arguments"]])
    request = _request_template(software_id, guide, contracts)
    required = contract["inputs"]
    expected_outputs = contract["outputs"]
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
        "6. Call `submit_native_job`, then supervise all independent job IDs with `wait_execution_jobs`; use focused inspection or full collection only when needed.",
        "7. Check process, software, convergence, artifact, and scientific-validation axes independently.",
        "",
        "## Working directory contract",
        "The runner creates an isolated job directory and executes the resolved binary there without a shell. Relative paths in arguments and input files resolve from that directory, not from the benchmark workspace root. `source_path` is workspace-relative; `target_path` is job-relative. Stage nested dependencies explicitly. The runner captures `request.json`, `stdout.log`, `stderr.log`, status, hashes, and collected artifacts.",
        "",
        "## Input mode",
        f"The primary executable is `{executable}` and its input mode is `{command.get('input_mode', 'arguments')}`.",
        "Required inputs: " + (", ".join(f"`{item}`" for item in required) if required else "no fixed file is declared for this command") + ".",
        "Expected outputs: " + (", ".join(f"`{item}`" for item in expected_outputs) if expected_outputs else "stdout/stderr or task-dependent outputs only") + ".",
        f"Example classification: `{contract['example_kind']}`.",
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


def render_common_tasks(
    software_id: str,
    guide: dict[str, Any],
    profile: dict[str, Any],
    contracts: dict[str, Any],
) -> str:
    lines = [
        _front_matter(software_id, profile, topics=["common-tasks", "inputs", "outputs", "convergence"]),
        f"# {profile['display_name']} Common Tasks",
        "",
        "## Appropriate calculation families",
        *[f"- **{item.title()}**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation." for item in profile.get("task_types", [])],
        "",
        "## Preferred typed Action routes",
        *(
            [f"- `{action_id}`: validated structured route through backend `{software_id}`." for action_id in _typed_actions(software_id)]
            or ["- No typed Action is registered for this software. Use the reviewed native command interface when the task needs this runtime."]
        ),
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
        contract = contracts["commands"][executable]
        if contract.get("enabled", True) is not True:
            continue
        lines.extend(
            [
                f"## Command: `{executable}`",
                f"- Synopsis: `{command.get('synopsis', executable)}`.",
                f"- Input mode: `{command.get('input_mode', 'arguments')}`.",
                "- Declared example inputs: " + (", ".join(f"`{item}`" for item in contract["inputs"]) or "none declared") + ".",
                "- Declared example outputs: " + (", ".join(f"`{item}`" for item in contract["outputs"]) or "stdout/stderr or task-dependent outputs") + ".",
                f"- Example resources: `{contract['resource_limits']}`.",
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


def render_example_files(
    software_id: str,
    guide: dict[str, Any],
    profile: dict[str, Any],
    contracts: dict[str, Any],
) -> dict[Path, str]:
    root = DOCS_ROOT / software_id / "examples" / "interface_smoke"
    result = smoke_results().get(software_id, {})
    executable, _command, _contract = _first_command(guide, contracts)
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
    guides, profiles, contracts = load_sources()
    result: dict[Path, str] = {}
    for software_id in sorted(guides):
        guide = guides[software_id]
        profile = profiles[software_id]
        example_contracts = contracts[software_id]
        if profile["operational_status"] == "placeholder":
            continue
        renderers = {
            "INDEX.md": render_index(software_id, guide, profile, example_contracts),
            "QUICKSTART.md": render_quickstart(software_id, guide, profile, example_contracts),
            "COMMON_TASKS.md": render_common_tasks(software_id, guide, profile, example_contracts),
            "TROUBLESHOOTING.md": render_troubleshooting(software_id, profile),
        }
        for filename, content in renderers.items():
            path = DOCS_ROOT / software_id / filename
            result[path] = content
        result.update(
            render_example_files(software_id, guide, profile, example_contracts)
        )
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
    profiles = load_sources()[1]
    detailed = sum(
        profile["operational_status"] != "placeholder"
        for profile in profiles.values()
    )
    print(f"Detailed native manual coverage: {detailed}; generated files: {len(generated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
