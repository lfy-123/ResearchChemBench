from __future__ import annotations

import time
from pathlib import Path

import pytest

from chemistry_toolbox.mcp.execution_models import (
    AnalysisInputDeclaration,
    AnalysisJobRequest,
    AnalysisOutputDeclaration,
    JobCollectRequest,
    JobStatusRequest,
    StagedInput,
)
from chemistry_toolbox.mcp.open_execution import (
    collect_execution_job,
    get_execution_job,
    submit_analysis_program,
    validate_analysis_program,
)
from researchchem_toolbox.models import ResourceLimits


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for name in ("code", "outputs", "report", "tool_logs"):
        (tmp_path / name).mkdir()
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    return tmp_path


def _wait(job_id: str) -> dict:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        result = get_execution_job(JobStatusRequest(job_id=job_id, tail_chars=3000))
        if result["terminal"]:
            return result
        time.sleep(0.05)
    raise AssertionError(f"job did not finish: {job_id}")


def test_programmable_analysis_templates_are_versioned_and_compile() -> None:
    templates = sorted((TOOLBOX_ROOT / "examples/analysis").glob("*.py"))
    assert len(templates) == 8
    for template in templates:
        compile(template.read_text(encoding="utf-8"), str(template), "exec")


def test_preflight_rejects_syntax_and_missing_runtime_modules(workspace: Path) -> None:
    (workspace / "code/bad.py").write_text("if True print('bad')\n", encoding="utf-8")
    syntax = validate_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/bad.py")
    )
    assert syntax["status"] == "invalid_request"
    assert syntax["error"]["code"] == "python_syntax_error"
    assert syntax["error"]["line"] == 1

    (workspace / "code/import.py").write_text(
        "import module_that_cannot_exist_12345\n", encoding="utf-8"
    )
    missing = validate_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/import.py")
    )
    assert missing["status"] == "invalid_request"
    assert missing["error"]["code"] == "runtime_modules_missing"

    (workspace / "code/main.py").write_text("import broken_local\n", encoding="utf-8")
    (workspace / "code/broken_local.py").write_text("def broken(:\n", encoding="utf-8")
    broken_local = validate_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/main.py",
            staged_inputs=[
                StagedInput(
                    source_path="code/broken_local.py",
                    target_path="broken_local.py",
                )
            ],
        )
    )
    assert broken_local["status"] == "invalid_request"
    assert broken_local["error"]["code"] == "staged_python_syntax_error"


def test_preflight_imports_modules_and_checks_versions_and_symbols(workspace: Path) -> None:
    (workspace / "code/imports.py").write_text(
        "import json\nimport packaging\n", encoding="utf-8"
    )
    valid = validate_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/imports.py",
            required_module_versions={"packaging": ">=20"},
            required_symbols={"json": ["loads", "JSONDecoder"]},
        )
    )
    assert valid["status"] == "success"
    assert valid["module_details"]["json"]["source"] == "runtime_import"
    assert valid["module_details"]["packaging"]["version"]

    missing_symbol = validate_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/imports.py",
            required_symbols={"json": ["symbol_that_does_not_exist"]},
        )
    )
    assert missing_symbol["status"] == "invalid_request"
    assert missing_symbol["error"]["code"] == "runtime_symbols_missing"


@pytest.mark.parametrize(
    "source",
    [
        "import subprocess\nsubprocess.run(['orca', 'input.inp'])\n",
        "from ase.calculators.vasp import Vasp\ncalculator = Vasp()\n",
    ],
)
def test_preflight_routes_external_executables_to_native_jobs(
    workspace: Path, source: str
) -> None:
    (workspace / "code/external.py").write_text(source, encoding="utf-8")
    result = validate_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/external.py")
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "external_execution_not_audited"
    assert "submit_native_job" in " ".join(result["error"]["candidate_fixes"])


def test_declared_job_context_and_artifact_manifest(workspace: Path) -> None:
    (workspace / "code/value.txt").write_text("7\n", encoding="utf-8")
    (workspace / "code/program.py").write_text(
        "from researchchem_job import JobContext\n"
        "import os\n"
        "ctx = JobContext.load()\n"
        "assert os.environ['RESEARCHCHEM_JOB_ROOT'] == str(ctx.root)\n"
        "assert os.environ['RESEARCHCHEM_JOB_INPUTS'] == str(ctx.root / 'inputs')\n"
        "assert os.environ['RESEARCHCHEM_JOB_OUTPUTS'] == str(ctx.root / 'outputs')\n"
        "assert os.environ['RESEARCHCHEM_JOB_REPORT'] == str(ctx.root / 'report')\n"
        "value = int(ctx.input('value').read_text())\n"
        "ctx.write_json('result', {'value': value, 'square': value * value})\n"
        "ctx.output('table').write_text('value,square\\n7,49\\n')\n"
        "ctx.register_output('table')\n",
        encoding="utf-8",
    )
    request = AnalysisJobRequest(
        runtime="core",
        script_path="code/program.py",
        required_modules=["json"],
        inputs=[
            AnalysisInputDeclaration(
                name="value",
                source_path="code/value.txt",
                semantic_type="IntegerInput",
            )
        ],
        outputs=[
            AnalysisOutputDeclaration(
                name="result",
                path="outputs/result.json",
                semantic_type="AnalysisResult",
                media_type="application/json",
                json_schema={
                    "type": "object",
                    "required": ["value", "square"],
                    "properties": {
                        "value": {"type": "integer"},
                        "square": {"type": "integer"},
                    },
                },
            ),
            AnalysisOutputDeclaration(
                name="table",
                path="outputs/result.csv",
                semantic_type="NumericTable",
                media_type="text/csv",
            ),
        ],
        resource_limits=ResourceLimits(memory_mb=512, cpu_cores=1),
    )
    preflight = validate_analysis_program(request)
    assert preflight["status"] == "success"
    assert preflight["analysis_contract"]["layout"]["inputs"] == "inputs/"
    assert "researchchem_job" in preflight["module_status"]

    submitted = submit_analysis_program(request)
    assert submitted["status"] == "success"
    finished = _wait(submitted["job_id"])
    assert finished["job"]["status"] == "success"
    collected = collect_execution_job(JobCollectRequest(job_id=submitted["job_id"]))
    assert collected["artifact_status"] == "valid"
    assert collected["request_status"] == "accepted"
    assert collected["process_status"] == "completed"
    assert collected["software_status"] == "not_applicable"
    assert collected["scientific_validation_status"] == "mechanically_valid"
    assert {item["name"] for item in collected["declared_artifacts"]} == {
        "result",
        "table",
    }
    assert all(
        item["validation_status"] == "valid"
        for item in collected["declared_artifacts"]
    )
    assert all(item["runtime_registration"] for item in collected["declared_artifacts"])
    assert collected["artifact_manifest"].endswith("artifact_manifest.json")


def test_process_success_does_not_hide_invalid_declared_json(workspace: Path) -> None:
    (workspace / "code/nonfinite.py").write_text(
        "from pathlib import Path\n"
        "Path('outputs/result.json').write_text('{\"energy\": NaN}\\n')\n",
        encoding="utf-8",
    )
    request = AnalysisJobRequest(
        runtime="core",
        script_path="code/nonfinite.py",
        outputs=[
            AnalysisOutputDeclaration(
                name="result",
                path="outputs/result.json",
                semantic_type="EnergyResult",
                media_type="application/json",
            )
        ],
    )
    submitted = submit_analysis_program(request)
    finished = _wait(submitted["job_id"])
    assert finished["job"]["status"] == "success"
    collected = collect_execution_job(JobCollectRequest(job_id=submitted["job_id"]))
    assert collected["artifact_status"] == "invalid"
    artifact = collected["declared_artifacts"][0]
    assert artifact["validation_status"] == "invalid"
    assert "non-standard JSON constant" in artifact["validation_errors"][0]
