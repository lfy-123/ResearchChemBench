import io
import json
import re
from pathlib import Path

from evaluation.live_progress import LiveProgressReporter
from evaluation.run_task import TaskRunner


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


def test_task_runner_writes_progress_without_terminal_spam(tmp_path: Path, capsys):
    runner = TaskRunner(
        "Electron_Isodensity_Reproduction_01_Method_Selection",
        agent_key="mock",
        workspace_root=tmp_path,
        live_progress=True,
        progress_console=False,
        progress_max_chars=120,
    )
    meta = runner.run()

    assert meta["status"] == "completed"
    assert meta["progress_console"] is False
    assert capsys.readouterr().out == ""
    progress = (runner.workspace / "_live_progress.log").read_text(encoding="utf-8")
    assert "[RUN_START]" in progress
    assert "[MODEL_INPUT]" in progress
    assert "[MODEL_OUTPUT]" in progress
    assert "[RUN_END]" in progress
    assert all(TIMESTAMPED_LINE.match(line) for line in progress.splitlines())
