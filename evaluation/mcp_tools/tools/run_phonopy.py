"""MCP tool: run bounded Phonopy/Phono3py command-line workflows."""

from __future__ import annotations

import shutil

from ..adapters.runtime import run_external, safe_input_file
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="run_phonopy",
    description="Run a Phonopy or Phono3py symmetry/small-displacement workflow from a workspace structure file.",
    category="phonons",
    backend="Phonopy/Phono3py",
    dependencies=("phonopy",),
    executables=("phonopy", "phonopy-init", "phono3py", "phono3py-init"),
    tags=("phonons", "symmetry", "thermal_conductivity"),
    side_effects=("runs phonon software", "writes displacement and phonon files"),
)


def run_phonopy_core(
    structure_file: str,
    output_directory: str = "outputs/phonopy",
    backend: str = "phonopy",
    mode: str = "symmetry",
    timeout_seconds: int = 1800,
) -> dict:
    if backend not in {"phonopy", "phono3py"} or mode not in {"symmetry", "displacements"}:
        raise ValueError("backend/mode is not supported")
    source = safe_input_file(structure_file)
    arguments = ["-c", str(source), "--symmetry"] if mode == "symmetry" else ["-c", str(source), "-d"]
    # Phonopy 4 moved setup operations such as ``-c`` and ``-d`` to the
    # phonopy-init/phono3py-init entry points.  Prefer them when present while
    # retaining compatibility with older installations and administrator
    # overrides through CHEMGRAPH_*_COMMAND.
    setup_executable = f"{backend}-init" if shutil.which(f"{backend}-init") else backend
    return run_external(
        backend=backend,
        executable=setup_executable,
        arguments=arguments,
        output_directory=output_directory,
        environment_variable="CHEMGRAPH_PHONOPY_COMMAND" if backend == "phonopy" else "CHEMGRAPH_PHONO3PY_COMMAND",
        timeout_seconds=timeout_seconds,
    )


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def run_phonopy(
        structure_file: str,
        output_directory: str = "outputs/phonopy",
        backend: str = "phonopy",
        mode: str = "symmetry",
        timeout_seconds: int = 1800,
    ) -> dict:
        arguments = locals()
        return execute_traced(TOOL_SPEC.name, arguments, lambda: run_phonopy_core(**arguments))
