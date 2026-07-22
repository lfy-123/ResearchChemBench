from __future__ import annotations

from chemistry_toolbox.mcp.execution_models import AnalysisRuntimeListRequest
from chemistry_toolbox.mcp.software_catalog import list_analysis_runtimes


def test_runtime_inventory_is_compact_until_one_runtime_is_inspected():
    compact = list_analysis_runtimes(AnalysisRuntimeListRequest(limit=500))
    assert compact["status"] == "success"
    assert compact["runtimes"]
    assert all("module_names" in item for item in compact["runtimes"])
    assert all("python" not in item and "modules" not in item for item in compact["runtimes"])
    assert "submit_analysis_program" in compact["execution_note"]

    runtime = compact["runtimes"][0]["runtime"]
    detailed = list_analysis_runtimes(
        AnalysisRuntimeListRequest(
            runtime=runtime,
            available_only=False,
            include_details=True,
        )
    )
    assert detailed["count"] == 1
    assert detailed["runtimes"][0]["runtime"] == runtime
    assert "python" in detailed["runtimes"][0]
    assert "modules" in detailed["runtimes"][0]
