"""FastMCP bindings for the software-native and programmable execution layers."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from pydantic import BaseModel

from .execution_models import (
    AnalysisInputInspectionRequest,
    AnalysisJobRequest,
    AnalysisRuntimeListRequest,
    ArtifactDeclarationRequest,
    DocumentationReadRequest,
    DocumentationSearchRequest,
    ExecutionResourceRequest,
    ExecutionSubmissionLookupRequest,
    ExecutionResultObservationRequest,
    JobCancelRequest,
    JobCollectRequest,
    JobStatusRequest,
    JobWaitRequest,
    NativeJobRequest,
    OutputContractValidationRequest,
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
    get_execution_resources as _get_execution_resources,
    lookup_execution_submission as _lookup_execution_submission,
    list_execution_jobs as _list_execution_jobs,
    inspect_analysis_inputs as _inspect_analysis_inputs,
    read_workspace_text as _read_workspace_text,
    submit_analysis_program as _submit_analysis_program,
    submit_native_job as _submit_native_job,
    validate_native_job as _validate_native_job,
    validate_analysis_program as _validate_analysis_program,
    wait_execution_jobs_async as _wait_execution_jobs,
    write_workspace_text as _write_workspace_text,
)
from .software_catalog import (
    inspect_software as _inspect_software,
    list_analysis_runtimes as _list_analysis_runtimes,
    list_software as _list_software,
    read_software_documentation as _read_software_documentation,
    search_software_documentation as _search_software_documentation,
    software_documentation_recovery,
)
from .tracing import execute_traced, execute_traced_async


RequestT = TypeVar("RequestT", bound=BaseModel)


OPEN_EXECUTION_TOOL_NAMES = (
    "list_software",
    "inspect_software",
    "read_software_documentation",
    "search_software_documentation",
    "write_workspace_text",
    "read_workspace_text",
    "validate_native_job",
    "validate_output_contract",
    "submit_native_job",
    "list_analysis_runtimes",
    "inspect_analysis_inputs",
    "validate_analysis_program",
    "submit_analysis_program",
    "get_execution_resources",
    "lookup_execution_submission",
    "list_execution_jobs",
    "acknowledge_execution_result",
    "get_execution_job",
    "wait_execution_jobs",
    "collect_execution_job",
    "cancel_execution_job",
    "declare_scientific_artifact",
)
ARTIFACT_CAPTURING_TOOLS = {
    "write_workspace_text",
    "declare_scientific_artifact",
}


TOOL_DESCRIPTIONS = {
    "validate_output_contract": "Read-only preflight of required outputs and JSON Schema using only public submission_schema.json. Returns file/JSON paths, structured errors and the contract hash. No scientific scoring or output changes.",
    "acknowledge_execution_result": "Confirm observation of one exact collected result receipt without rerunning or re-parsing it.",
    "list_execution_jobs": "List durable job identities and states restricted to the current run.",
    "list_software": (
        "List and filter a paginated compact index of the complete local software/library inventory. "
        "Use query to narrow it, then inspect_software for one exact id; detailed versions, paths, "
        "commands, modules, and manuals are deliberately omitted here. This operation does not "
        "recommend, rank, or select a program."
    ),
    "inspect_software": (
        "Inspect one exact software id before using it. Returns installed runtime/health, current "
        "Action coverage, Python modules, reviewed native command synopses and example argv, input "
        "mode, required filenames, output behavior, cached manuals, and official sources. Use this "
        "instead of guessing a command line."
    ),
    "read_software_documentation": (
        "Read a bounded first-party Markdown topic for one exact software id, optionally narrowed "
        "to one heading. Use inspect_software to discover topic ids."
    ),
    "search_software_documentation": (
        "Search heading-level local documentation chunks for one exact software id. Exact topic and "
        "section routing is applied first, then BM25 and optional offline MiniLM semantic recall."
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
        "Search the configured Python runtimes available for an Agent-authored scientific program. "
        "The default response is a compact inventory; filter by query/runtime and request details "
        "only for the selected environment. No runtime is selected automatically."
    ),
    "inspect_analysis_inputs": (
        "Inspect bounded structural metadata for declared analysis inputs before writing or "
        "submitting a program. JSON keys/types/list lengths/nulls and CSV/TSV columns/types are "
        "reported without selecting a scientific method or interpreting the result."
    ),
    "submit_analysis_program": (
        "Submit an Agent-authored .py file asynchronously in one explicitly selected chemistry "
        "runtime. The script and inputs are staged and hashed; stdout/stderr/resources/outputs share "
        "the native job record. This process confinement is not an OS container security boundary."
    ),
    "validate_analysis_program": (
        "Preflight an Agent-authored Python analysis without executing it. Checks UTF-8 syntax, "
        "imports in the selected runtime, declared inputs and outputs, paths, and resources, then "
        "returns the exact job layout and structured repair diagnostics."
    ),
    "get_execution_resources": (
        "Read the evaluator-controlled task resource budget, resources reserved by active jobs, "
        "and capacity currently available before choosing resources or submission concurrency."
    ),
    "lookup_execution_submission": (
        "Look up the durable receipt for a submission_key after an MCP or Agent transport "
        "interruption. It never starts a replacement job."
    ),
    "get_execution_job": (
        "Inspect one native/program job by exact job_id for failure diagnosis or suspected stalls, "
        "returning persistent state plus bounded stdout and stderr tails."
    ),
    "wait_execution_jobs": (
        "Wait internally for stable state changes across 1-128 native/program jobs. Running jobs "
        "continue, distributed queues keep filling, terminal jobs are collected automatically, "
        "and one compact aggregate reports terminal, running, queued, and remaining jobs."
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
            result = {
                "status": "invalid_request",
                "error": {
                    "code": "invalid_open_execution_request",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
                "automatic_fallback": False,
            }
            if name in {"validate_native_job", "submit_native_job"} and isinstance(
                request, NativeJobRequest
            ):
                result["documentation_recovery"] = software_documentation_recovery(
                    request.software_id, failed=True
                )
            return result
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

    return execute_traced(
        name,
        arguments,
        run,
        capture_artifacts=name in ARTIFACT_CAPTURING_TOOLS,
    )


def list_software(request: SoftwareListRequest) -> dict[str, Any]:
    return _invoke("list_software", request, _list_software)


def inspect_software(request: SoftwareInspectRequest) -> dict[str, Any]:
    return _invoke("inspect_software", request, _inspect_software)


def read_software_documentation(request: DocumentationReadRequest) -> dict[str, Any]:
    return _invoke(
        "read_software_documentation", request, _read_software_documentation
    )


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


def validate_output_contract(request: OutputContractValidationRequest) -> dict[str, Any]:
    from chemistry_toolbox.src.output_contract import validate_workspace_output_contract
    from .workspace import workspace_root
    return _invoke("validate_output_contract", request,
                   lambda value: validate_workspace_output_contract(workspace_root(), max_errors=value.max_errors))


def submit_native_job(request: NativeJobRequest) -> dict[str, Any]:
    return _invoke("submit_native_job", request, _submit_native_job)


def list_analysis_runtimes(request: AnalysisRuntimeListRequest) -> dict[str, Any]:
    return _invoke("list_analysis_runtimes", request, _list_analysis_runtimes)


def inspect_analysis_inputs(request: AnalysisInputInspectionRequest) -> dict[str, Any]:
    return _invoke("inspect_analysis_inputs", request, _inspect_analysis_inputs)


def validate_analysis_program(request: AnalysisJobRequest) -> dict[str, Any]:
    return _invoke("validate_analysis_program", request, _validate_analysis_program)


def submit_analysis_program(request: AnalysisJobRequest) -> dict[str, Any]:
    return _invoke("submit_analysis_program", request, _submit_analysis_program)


def get_execution_resources(request: ExecutionResourceRequest) -> dict[str, Any]:
    return _invoke("get_execution_resources", request, _get_execution_resources)


def get_execution_job(request: JobStatusRequest) -> dict[str, Any]:
    return _invoke("get_execution_job", request, _get_execution_job)


def acknowledge_execution_result(request: ExecutionResultObservationRequest) -> dict[str, Any]:
    def acknowledge(value):
        from .execution_store import execution_store
        store = execution_store()
        result = store.get_record("result", value.job_id)
        if not result or result["result_receipt_id"] != value.result_receipt_id:
            return {"status": "invalid_request", "error": {"code": "result_receipt_mismatch"}}
        observation = {"state": "observed", "result_receipt_id": value.result_receipt_id}
        store.put_record("observation_revision", value.result_receipt_id, observation, immutable=True)
        store.put_record("observation", value.job_id, observation)
        return {"status": "success", "job_id": value.job_id, "observed": True}
    return _invoke("acknowledge_execution_result", request, acknowledge)


def list_execution_jobs(request: ExecutionResourceRequest) -> dict[str, Any]:
    return _invoke("list_execution_jobs", request, _list_execution_jobs)


def lookup_execution_submission(request: ExecutionSubmissionLookupRequest) -> dict[str, Any]:
    return _invoke(
        "lookup_execution_submission", request, _lookup_execution_submission
    )


async def wait_execution_jobs(request: JobWaitRequest) -> dict[str, Any]:
    return await execute_traced_async(
        "wait_execution_jobs", {"request": request.model_dump(mode="json")},
        lambda: _wait_execution_jobs(request),
    )


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
        if name == "validate_output_contract":
            from mcp.types import ToolAnnotations
            mcp.tool(name=name, description=TOOL_DESCRIPTIONS[name],
                     annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False))(function)
        else:
            mcp.tool(name=name, description=TOOL_DESCRIPTIONS[name])(function)
    return list(functions)


__all__ = [*OPEN_EXECUTION_TOOL_NAMES, "OPEN_EXECUTION_TOOL_NAMES", "register_open_execution_tools"]
