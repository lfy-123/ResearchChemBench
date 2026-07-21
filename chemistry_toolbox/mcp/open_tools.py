"""FastMCP bindings for the software-native and programmable execution layers."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from pydantic import BaseModel

from .execution_models import (
    AnalysisJobRequest,
    AnalysisRuntimeListRequest,
    ArtifactDeclarationRequest,
    DocumentationSearchRequest,
    JobCancelRequest,
    JobCollectRequest,
    JobStatusRequest,
    NativeJobRequest,
    SoftwareInspectRequest,
    SoftwareListRequest,
    WorkspaceTextReadRequest,
    WorkspaceTextWriteRequest,
)
from .open_execution import (
    cancel_execution_job as _cancel_execution_job,
    collect_execution_job as _collect_execution_job,
    declare_scientific_artifact as _declare_scientific_artifact,
    get_execution_job as _get_execution_job,
    read_workspace_text as _read_workspace_text,
    submit_analysis_program as _submit_analysis_program,
    submit_native_job as _submit_native_job,
    validate_native_job as _validate_native_job,
    write_workspace_text as _write_workspace_text,
)
from .software_catalog import (
    inspect_software as _inspect_software,
    list_analysis_runtimes as _list_analysis_runtimes,
    list_software as _list_software,
    search_software_documentation as _search_software_documentation,
)
from .tracing import execute_traced


RequestT = TypeVar("RequestT", bound=BaseModel)


OPEN_EXECUTION_TOOL_NAMES = (
    "list_software",
    "inspect_software",
    "search_software_documentation",
    "write_workspace_text",
    "read_workspace_text",
    "validate_native_job",
    "submit_native_job",
    "list_analysis_runtimes",
    "submit_analysis_program",
    "get_execution_job",
    "collect_execution_job",
    "cancel_execution_job",
    "declare_scientific_artifact",
)


TOOL_DESCRIPTIONS = {
    "list_software": (
        "List and filter the complete local software/library/documentation inventory. This is a "
        "neutral inventory operation: it does not recommend, rank, or select a program."
    ),
    "inspect_software": (
        "Inspect one exact software id before using it. Returns installed runtime/health, current "
        "Action coverage, Python modules, reviewed native command synopses and example argv, input "
        "mode, required filenames, output behavior, cached manuals, and official sources. Use this "
        "instead of guessing a command line."
    ),
    "search_software_documentation": (
        "Search locally cached text/HTML documentation for one exact software id and term. Returns "
        "bounded excerpts and source paths; PDFs/archives are listed when they cannot be text-searched."
    ),
    "write_workspace_text": (
        "Write an Agent-authored UTF-8 input deck, configuration, or Python program under code/ or "
        "outputs/. Existing files are protected unless overwrite=true is explicit."
    ),
    "read_workspace_text": (
        "Read an exact UTF-8 workspace file with a bounded character count and content hash."
    ),
    "validate_native_job": (
        "Validate one exact Agent-authored native invocation without executing it. Checks the "
        "software/executable allowlist, installed path, argv/path safety, staging/stdin contract, "
        "and mechanical resources. It never adds scientific parameters or judges the method."
    ),
    "submit_native_job": (
        "Submit one exact reviewed software command asynchronously with shell=false. All input files "
        "must be mapped explicitly into an isolated job directory. Returns a persistent job_id; no "
        "software choice, scientific default, callback, retry, or fallback is performed."
    ),
    "list_analysis_runtimes": (
        "List configured Python runtimes, installed modules, commands, and paths available for an "
        "Agent-authored scientific program. No runtime is selected automatically."
    ),
    "submit_analysis_program": (
        "Submit an Agent-authored .py file asynchronously in one explicitly selected chemistry "
        "runtime. The script and inputs are staged and hashed; stdout/stderr/resources/outputs share "
        "the native job record. This process confinement is not an OS container security boundary."
    ),
    "get_execution_job": (
        "Poll one native/program job by exact job_id and return persistent state plus bounded stdout "
        "and stderr tails."
    ),
    "collect_execution_job": (
        "After a job is terminal, enumerate output files and logs with paths, byte sizes, and SHA-256 "
        "hashes. This does not interpret scientific results."
    ),
    "cancel_execution_job": (
        "Send a cancellation request to one exact running job. It never starts a replacement or "
        "changes scientific parameters."
    ),
    "declare_scientific_artifact": (
        "Register an existing workspace file as an immutable ArtifactRef with Agent-supplied semantic "
        "type, producer layer/id, media type, and parent lineage. No semantics are inferred."
    ),
}


def _invoke(
    name: str,
    request: RequestT,
    function: Callable[[RequestT], dict[str, Any]],
) -> dict[str, Any]:
    arguments = {"request": request.model_dump(mode="json")}

    def run() -> dict[str, Any]:
        try:
            return function(request)
        except (FileNotFoundError, FileExistsError, KeyError, UnicodeError, ValueError) as exc:
            return {
                "status": "invalid_request",
                "error": {
                    "code": "invalid_open_execution_request",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
                "automatic_fallback": False,
            }
        except OSError as exc:
            return {
                "status": "failed",
                "error": {
                    "code": "open_execution_os_error",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
                "automatic_fallback": False,
            }
        except Exception as exc:
            return {
                "status": "failed",
                "error": {
                    "code": "open_execution_internal_error",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
                "automatic_fallback": False,
            }

    return execute_traced(name, arguments, run)


def list_software(request: SoftwareListRequest) -> dict[str, Any]:
    return _invoke("list_software", request, _list_software)


def inspect_software(request: SoftwareInspectRequest) -> dict[str, Any]:
    return _invoke("inspect_software", request, _inspect_software)


def search_software_documentation(request: DocumentationSearchRequest) -> dict[str, Any]:
    return _invoke(
        "search_software_documentation", request, _search_software_documentation
    )


def write_workspace_text(request: WorkspaceTextWriteRequest) -> dict[str, Any]:
    return _invoke("write_workspace_text", request, _write_workspace_text)


def read_workspace_text(request: WorkspaceTextReadRequest) -> dict[str, Any]:
    return _invoke("read_workspace_text", request, _read_workspace_text)


def validate_native_job(request: NativeJobRequest) -> dict[str, Any]:
    return _invoke("validate_native_job", request, _validate_native_job)


def submit_native_job(request: NativeJobRequest) -> dict[str, Any]:
    return _invoke("submit_native_job", request, _submit_native_job)


def list_analysis_runtimes(request: AnalysisRuntimeListRequest) -> dict[str, Any]:
    return _invoke("list_analysis_runtimes", request, _list_analysis_runtimes)


def submit_analysis_program(request: AnalysisJobRequest) -> dict[str, Any]:
    return _invoke("submit_analysis_program", request, _submit_analysis_program)


def get_execution_job(request: JobStatusRequest) -> dict[str, Any]:
    return _invoke("get_execution_job", request, _get_execution_job)


def collect_execution_job(request: JobCollectRequest) -> dict[str, Any]:
    return _invoke("collect_execution_job", request, _collect_execution_job)


def cancel_execution_job(request: JobCancelRequest) -> dict[str, Any]:
    return _invoke("cancel_execution_job", request, _cancel_execution_job)


def declare_scientific_artifact(request: ArtifactDeclarationRequest) -> dict[str, Any]:
    return _invoke(
        "declare_scientific_artifact", request, _declare_scientific_artifact
    )


def register_open_execution_tools(mcp) -> list[str]:
    functions = {
        name: globals()[name]
        for name in OPEN_EXECUTION_TOOL_NAMES
    }
    for name, function in functions.items():
        mcp.tool(name=name, description=TOOL_DESCRIPTIONS[name])(function)
    return list(functions)


__all__ = [*OPEN_EXECUTION_TOOL_NAMES, "OPEN_EXECUTION_TOOL_NAMES", "register_open_execution_tools"]
