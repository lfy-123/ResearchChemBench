from __future__ import annotations

import json

from chemistry_toolbox.mcp.execution_models import (
    AnalysisRuntimeListRequest,
    SoftwareListRequest,
)
from chemistry_toolbox.mcp.software_catalog import list_analysis_runtimes, list_software


def test_runtime_inventory_is_compact_until_one_runtime_is_inspected():
    compact = list_analysis_runtimes(AnalysisRuntimeListRequest(limit=500))
    assert compact["status"] == "success"
    assert compact["runtimes"]
    assert all("module_count" in item for item in compact["runtimes"])
    assert all(
        "python" not in item and "modules" not in item and "module_names" not in item
        for item in compact["runtimes"]
    )
    assert "submit_analysis_program" in compact["execution_note"]
    assert "get_execution_resources" in compact["execution_note"]
    assert compact["managed_program_contract"]["job_context_required_for_compliance"]
    assert "JobContext.load" in compact["managed_program_contract"]["minimal_python_template"]
    assert list(compact).index("managed_program_contract") < list(compact).index("runtimes")
    template = compact["submit_analysis_program_request_template"]
    assert template["inputs"][0]["name"] == "<logical_input_name>"
    assert template["outputs"][0]["path"].startswith("outputs/")
    assert template["staged_inputs"] == []

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


def test_software_inventory_is_a_paginated_compact_index():
    first = list_software(SoftwareListRequest())
    assert first["status"] == "success"
    assert first["count"] <= 50
    assert first["next_offset"] is not None
    assert all("resolved_path" not in json.dumps(item) for item in first["software"])

    complete = list_software(SoftwareListRequest(limit=200))
    assert complete["count"] == complete["total_matching"]
    assert len(json.dumps(complete)) < 40_000
