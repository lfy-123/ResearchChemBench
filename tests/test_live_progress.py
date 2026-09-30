import io
import json
import re
from pathlib import Path

from evaluation.execution.progress import LiveProgressReporter


TIMESTAMPED_LINE = re.compile(
    r"^\[RCB\]\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\]"
    r"\[[A-Z_]+\]"
)


def test_progress_is_timestamped_redacted_truncated_and_file_only(tmp_path: Path):
    console = io.StringIO()
    reporter = LiveProgressReporter(
        tmp_path,
        "test-run",
        console=False,
        max_chars=100,
        stream=console,
    )
    reporter.emit(
        "MODEL_INPUT",
        request={"api_key": "secret-value", "prompt": "x" * 500},
    )
    reporter.handle_agent_line(
        json.dumps(
            {
                "type": "text",
                "part": {"text": "A model answer " + "y" * 500},
            }
        )
    )
    reporter.handle_agent_line(
        json.dumps(
            {
                "type": "tool_use",
                "part": {
                    "tool": "bash",
                    "state": {
                        "status": "completed",
                        "input": {"command": "python analysis.py"},
                        "output": "analysis complete",
                    },
                },
            }
        )
    )
    reporter.handle_agent_line(
        json.dumps(
            {
                "type": "step_finish",
                "part": {
                    "reason": "tool-calls",
                    "tokens": {"input": 120, "output": 30, "total": 150},
                },
            }
        )
    )
    reporter.handle_tool_trace_line(
        json.dumps(
            {
                "sequence": 4,
                "tool": "researchchem_toolbox_run_action",
                "arguments": {
                    "request": {
                        "action_id": "calculate_energy",
                        "backend_id": "orca",
                    }
                },
                "status": "success",
                "duration_seconds": 1.25,
                "result_preview": {"energy_hartree": -40.1},
            }
        )
    )
    reporter.close()

    assert console.getvalue() == ""
    lines = (tmp_path / "_live_progress.log").read_text(encoding="utf-8").splitlines()
    assert lines
    assert all(TIMESTAMPED_LINE.match(line) for line in lines)
    combined = "\n".join(lines)
    assert "test-run" not in combined
    assert "secret-value" not in combined
    assert "<redacted>" in combined
    assert "<truncated " in combined
    assert "[MODEL_OUTPUT]" in combined
    assert "[NATIVE_TOOL]" in combined
    assert "[MODEL_STEP]" in combined
    assert "[MCP_CALL]" in combined
    assert "[MCP_RESULT]" in combined


def test_progress_can_be_explicitly_mirrored_to_console(tmp_path: Path):
    console = io.StringIO()
    reporter = LiveProgressReporter(
        tmp_path,
        "test-run",
        console=True,
        max_chars=100,
        stream=console,
    )
    reporter.emit("RUN_START", task="Electron_Isodensity_Reproduction_01_Method_Selection")
    reporter.close()

    assert TIMESTAMPED_LINE.match(console.getvalue().strip())
    assert console.getvalue() == (tmp_path / "_live_progress.log").read_text(
        encoding="utf-8"
    )


def test_codex_stream_reports_tool_denials_and_outputs(tmp_path: Path):
    reporter = LiveProgressReporter(tmp_path, "codex-run", max_chars=160)
    events = [
        {"type": "thread.started", "thread_id": "original-session"},
        {"type": "turn.started"},
        {"type": "item.completed", "item": {"id": "item_0", "type": "agent_message", "text": "Inspecting inputs."}},
        {"type": "item.started", "item": {
            "id": "item_1", "type": "mcp_tool_call", "server": "researchchem_toolbox",
            "tool": "list_execution_jobs", "arguments": {"request": {"api_key": "do-not-log"}},
            "status": "in_progress",
        }},
        {"type": "item.completed", "item": {
            "id": "item_1", "type": "mcp_tool_call", "server": "researchchem_toolbox",
            "tool": "list_execution_jobs", "status": "failed",
            "error": {"message": "MCP tool call requires approval, but approval policy is never"},
        }},
        {"type": "item.completed", "item": {
            "id": "item_2", "type": "command_execution", "command": "cat task.md",
            "aggregated_output": "output " * 100, "exit_code": 0, "status": "completed",
        }},
        {"type": "turn.completed", "usage": {"input_tokens": 12, "output_tokens": 3}},
        {"type": "turn.failed", "error": {"message": "provider disconnected"}},
    ]
    for event in events:
        reporter.handle_agent_line(json.dumps(event))
    reporter.close()
    text = (tmp_path / "_live_progress.log").read_text()
    assert all(TIMESTAMPED_LINE.match(line) for line in text.splitlines())
    assert "[AGENT_SESSION] session_id=original-session" in text
    assert "[MODEL_STEP_START]" in text
    assert "[MODEL_OUTPUT] text=Inspecting inputs." in text
    assert text.count("[MCP_AGENT_EVENT]") == 2
    assert "status=in_progress" in text and "status=failed" in text
    assert "MCP tool call requires approval" in text
    assert "[NATIVE_TOOL]" in text and "exit_code=0" in text
    assert "<truncated " in text
    assert "[MODEL_STEP]" in text and '"input_tokens": 12' in text
    assert "[AGENT_ERROR]" in text and "provider disconnected" in text
    assert "do-not-log" not in text and "<redacted>" in text
