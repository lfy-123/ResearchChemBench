"""MCP tool: inspect one registered backend without importing it."""

from __future__ import annotations

from ..adapters.runtime import backend_status
from ..adapters.toolbox_registry import software_entry
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="check_backend_availability",
    description="Check Python modules, executables, credentials, and manual actions for one backend.",
    category="toolbox_management",
    backend="ResearchChemBench registry/runtime probe",
    dependencies=("pyyaml",),
    tags=("availability", "diagnostics", "registry"),
)


ENVIRONMENT_BY_BACKEND = {
    "orca": ("CHEMGRAPH_ORCA_COMMAND",),
    "vasp": ("CHEMGRAPH_VASP_COMMAND",),
    "gaussian": ("CHEMGRAPH_GAUSSIAN_COMMAND",),
    "q-chem": ("CHEMGRAPH_QCHEM_COMMAND",),
    "molpro": ("CHEMGRAPH_MOLPRO_COMMAND",),
    "materials project api": ("MP_API_KEY",),
}


def check_backend_availability_core(name: str) -> dict:
    entry = software_entry(name)
    if entry is None:
        return {
            "status": "unknown",
            "backend": name,
            "available": False,
            "reason": "Backend is not present in config/toolbox_registry.yaml",
        }
    normalized = str(entry["name"]).lower()
    environment_variables = ENVIRONMENT_BY_BACKEND.get(normalized, ())
    install_method = str(entry.get("install_method") or "")
    if install_method.startswith("remote"):
        result = {
            "status": "available",
            "backend": str(entry["name"]),
            "available": True,
            "python_modules": {},
            "executables": {},
            "environment": {},
            "manual_action": None,
            "reason": "Remote service adapter is registered; live availability depends on the service response.",
        }
    elif not entry.get("python_module") and not entry.get("executable") and not environment_variables:
        result = {
            "status": "unavailable",
            "backend": str(entry["name"]),
            "available": False,
            "python_modules": {},
            "executables": {},
            "environment": {},
            "manual_action": entry.get("manual_action") or "Install and configure this backend before use.",
            "reason": entry.get("failure_reason") or "No runtime module, executable, or configured command is available.",
        }
    else:
        result = backend_status(
            str(entry["name"]),
            python_modules=(entry.get("python_module") or "",),
            executables=(entry.get("executable") or "",),
            environment_variables=environment_variables,
            manual_action=entry.get("manual_action")
            or "Install the backend in its configured MCP profile environment.",
        )
        if not result["available"] and entry.get("failure_reason"):
            result["reason"] = entry["failure_reason"]
    result["configured_status"] = entry.get("status")
    result["license_class"] = entry.get("license_class")
    result["official_url"] = entry.get("official_url")
    return result


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def check_backend_availability(name: str) -> dict:
        return execute_traced(
            TOOL_SPEC.name,
            {"name": name},
            lambda: check_backend_availability_core(name),
        )
