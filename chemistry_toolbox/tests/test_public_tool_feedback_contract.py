import asyncio
import json

import pytest

from chemistry_toolbox.src.execution_feedback import execution_feedback, normalize_tool_feedback
from chemistry_toolbox.src.native_diagnostics import native_diagnostic


@pytest.fixture
def v2(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_FEEDBACK_SCHEMA_VERSION", "2")
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    return tmp_path


def test_native_root_cause_beats_secondary_crash(v2):
    log = v2 / "stdout.log"
    log.write_text("banner\nEnd of file in ZSymb\nsegmentation fault\n")
    error = native_diagnostic([log], root=v2, software_id="gaussian")
    assert error["code"] == "input_read_error"
    assert error["evidence"][0]["line_start"] == 2
    assert error["evidence"][0]["path"] == "stdout.log"


def test_ready_job_does_not_request_redundant_collect(v2):
    view = execution_feedback(status={"job_id": "j", "status": "failed", "return_code": 1},
        record={"result_state": "ready"}, program_diagnostic={"code": "native", "message": "one cause"})
    assert view["next_tool_calls"] == []
    assert view["process"]["started"] is True
    shown = normalize_tool_feedback({"execution_feedback": view, "failure_diagnostic": view["diagnostic"],
        "stdout_tail": "one cause", "error": "one cause"}, tool="wait_execution_jobs")
    assert json.dumps(shown).count("one cause") == 1


def test_registration_surfaces_use_common_trace_boundary(v2):
    from chemistry_toolbox.mcp.registry import register_public_tools
    class Registry:
        def __init__(self): self.tools = {}
        def tool(self, **kwargs):
            def add(fn): self.tools[kwargs["name"]] = fn; return fn
            return add
    for mode in ("full", "progressive"):
        registry = Registry()
        names = register_public_tools(registry, mode)
        assert set(names) == set(registry.tools)
        for name in names:
            value = normalize_tool_feedback({"status": "invalid_request", "error": {"message": "bad request"}}, tool=name)
            assert value["execution_feedback"]["diagnostic"]["origin"] == "tool_boundary"
            assert "process" not in value["execution_feedback"]


def test_mcp_schema_errors_are_persisted(v2):
    from chemistry_toolbox.mcp.feedback_server import FeedbackFastMCP
    server = FeedbackFastMCP("fixture")
    @server.tool()
    def number(value: int) -> dict:
        return {"value": value}
    response = asyncio.run(server.call_tool("number", {"value": "not-an-int"}))
    result = json.loads(response[0].text)
    assert result["status"] == "invalid_request"
    assert result["execution_feedback"]["diagnostic"]["stage"] == "dispatch"
    assert (v2 / "_tool_trace.jsonl").is_file()


def test_mcp_does_not_duplicate_text_and_structured_results(v2):
    from chemistry_toolbox.mcp.feedback_server import FeedbackFastMCP
    server = FeedbackFastMCP("fixture")
    @server.tool()
    def value() -> dict:
        return {"observations": "unique-native-evidence"}
    response = asyncio.run(server.call_tool("value", {}))
    assert isinstance(response, list)
    assert len(response) == 1 and response[0].text.count("unique-native-evidence") == 1


def test_cancel_is_not_converted_to_tool_error(v2):
    from chemistry_toolbox.mcp.feedback_server import FeedbackFastMCP
    server = FeedbackFastMCP("fixture")
    @server.tool()
    async def cancel() -> dict:
        raise asyncio.CancelledError()
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(server.call_tool("cancel", {}))
