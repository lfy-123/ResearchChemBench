from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from chemistry_toolbox.mcp.execution_models import (
    AnalysisInputDeclaration,
    AnalysisInputInspectionRequest,
    AnalysisJobRequest,
    AnalysisOutputDeclaration,
    ExecutionResourceRequest,
    JobCollectRequest,
    JobStatusRequest,
    StagedInput,
)
from chemistry_toolbox.mcp.open_execution import (
    collect_execution_job,
    get_execution_job,
    get_execution_resources,
    inspect_analysis_inputs,
    submit_analysis_program,
    validate_analysis_program,
    _validate_scientific_output,
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


@pytest.mark.parametrize(
    "source",
    [
        "from pathlib import Path\nprint(Path('data/benchmark_data/input.csv').read_text())\n",
        "import pandas as pd\nprint(pd.read_csv('_tool_artifacts/objects/result.csv'))\n",
    ],
)
def test_preflight_rejects_unstaged_workspace_relative_inputs(
    workspace: Path, source: str
) -> None:
    (workspace / "code/unstaged.py").write_text(source, encoding="utf-8")
    result = validate_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/unstaged.py")
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "unstaged_workspace_relative_path"
    assert "JobContext.input" in " ".join(result["error"]["candidate_fixes"])


def test_preflight_does_not_treat_logged_path_text_as_file_access(workspace: Path) -> None:
    (workspace / "code/log_path.py").write_text(
        "print('data/benchmark_data/input.csv')\n", encoding="utf-8"
    )
    result = validate_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/log_path.py")
    )
    assert result["status"] == "success"


def test_preflight_reports_job_context_bypass_without_claiming_enforcement(
    workspace: Path,
) -> None:
    (workspace / "code/bypass.py").write_text(
        "from researchchem_job import JobContext\n"
        "ctx = JobContext.load()\n"
        "workspace = ctx.root.parents[2]\n"
        "print(workspace)\n",
        encoding="utf-8",
    )
    result = validate_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/bypass.py")
    )
    assert result["status"] == "success"
    compliance = result["job_context_compliance"]
    assert compliance["status"] == "bypassed"
    assert compliance["bypass_findings"]
    assert "not blocked" in compliance["enforcement_boundary"]


@pytest.mark.parametrize(
    "source",
    [
        "import sys\nsys.path.insert(0, '/other/python3.11/site-packages')\n",
        "import site\nsite.addsitedir('/other/environment')\n",
        "import os\nos.environ['PYTHONPATH'] = '/other/environment'\n",
    ],
)
def test_preflight_rejects_cross_runtime_path_injection(
    workspace: Path, source: str
) -> None:
    (workspace / "code/runtime_mix.py").write_text(source, encoding="utf-8")
    result = validate_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/runtime_mix.py")
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "cross_runtime_path_injection"


def test_preflight_rejects_undeclared_job_context_names(workspace: Path) -> None:
    (workspace / "code/value.json").write_text("{}\n", encoding="utf-8")
    (workspace / "code/name_mismatch.py").write_text(
        "from researchchem_job import JobContext\n"
        "ctx = JobContext.load()\n"
        "ctx.input('invented_name').read_text()\n"
        "ctx.write_json('invented_output', {})\n",
        encoding="utf-8",
    )
    result = validate_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/name_mismatch.py",
            inputs=[
                AnalysisInputDeclaration(
                    name="declared_input",
                    source_path="code/value.json",
                )
            ],
            outputs=[
                AnalysisOutputDeclaration(
                    name="declared_output",
                    path="outputs/result.json",
                    semantic_type="AnalysisResult",
                    media_type="application/json",
                )
            ],
        )
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "job_context_declaration_mismatch"
    assert "invented_name" in result["error"]["evidence"]
    assert "declared_input" in result["error"]["evidence"]
    assert "declared_output" in result["error"]["evidence"]


def test_preflight_reports_case_sensitive_job_context_repair(workspace: Path) -> None:
    (workspace / "code/value.json").write_text("{}\n", encoding="utf-8")
    (workspace / "code/name_case.py").write_text(
        "from researchchem_job import JobContext\n"
        "ctx = JobContext.load()\n"
        "ctx.input('InputData').read_text()\n",
        encoding="utf-8",
    )
    result = validate_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/name_case.py",
            inputs=[
                AnalysisInputDeclaration(
                    name="inputdata",
                    source_path="code/value.json",
                )
            ],
        )
    )

    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "job_context_declaration_mismatch"
    assert "names are case-sensitive" in result["error"]["candidate_fixes"][0]
    assert "InputData" in result["error"]["candidate_fixes"][0]
    assert "inputdata" in result["error"]["candidate_fixes"][0]


@pytest.mark.parametrize(
    ("source", "evidence"),
    [
        (
            "from researchchem_job import JobContext\n"
            "ctx = JobContext.load()\n"
            "value = ctx.input('value').path.read_text()\n",
            "JobContext.input(...).path",
        ),
        (
            "value = 'missing'\n"
            "print(f\"{value:.4f if isinstance(value, float) else value}\")\n",
            "conditional_inside_format_specifier",
        ),
        (
            "from researchchem_job import JobContext\n"
            "ctx = JobContext.load()\n"
            "ctx.output('result').register()\n",
            "JobContext.output(...).register()",
        ),
    ],
)
def test_preflight_rejects_deterministic_python_runtime_errors(
    workspace: Path, source: str, evidence: str
) -> None:
    (workspace / "code/value.txt").write_text("7\n", encoding="utf-8")
    (workspace / "code/runtime_error.py").write_text(source, encoding="utf-8")
    request = AnalysisJobRequest(
        runtime="core",
        script_path="code/runtime_error.py",
        inputs=(
            [
                AnalysisInputDeclaration(
                    name="value",
                    source_path="code/value.txt",
                )
            ]
            if "JobContext" in source
            else []
        ),
    )
    result = validate_analysis_program(request)
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "analysis_program_runtime_error"
    assert evidence in result["error"]["evidence"]


def test_execution_resource_status_is_available_before_submission(workspace: Path) -> None:
    result = get_execution_resources(ExecutionResourceRequest())
    assert result["status"] == "success"
    assert result["budget"]["cpu_cores"] >= 1
    assert result["available"]["cpu_cores"] <= result["budget"]["cpu_cores"]
    assert result["active_jobs"] == []


def test_analysis_input_inspection_reports_json_and_table_shapes(workspace: Path) -> None:
    (workspace / "code/data.json").write_text(
        json.dumps(
            {
                "records": [
                    {"id": "a", "energy": -1.0, "weight": None},
                    {"id": "b", "energy": -0.5, "weight": 0.4},
                ],
                "metadata": {"temperature": 298.15},
            }
        ),
        encoding="utf-8",
    )
    (workspace / "code/data.csv").write_text(
        "name,energy,valid\na,-1.0,true\nb,,false\n", encoding="utf-8"
    )
    declarations = [
        AnalysisInputDeclaration(name="json_data", source_path="code/data.json"),
        AnalysisInputDeclaration(name="table_data", source_path="code/data.csv"),
    ]
    result = inspect_analysis_inputs(
        AnalysisInputInspectionRequest(inputs=declarations)
    )
    assert result["status"] == "success"
    json_summary, table_summary = result["inputs"]
    assert json_summary["shape"]["fields"] == ["records", "metadata"]
    assert json_summary["shape"]["field_shapes"]["records"]["length"] == 2
    weight_profile = json_summary["shape"]["field_shapes"]["records"][
        "object_field_profiles"
    ]["weight"]
    assert weight_profile["presence_count"] == 2
    assert weight_profile["null_count"] == 1
    assert table_summary["columns"] == ["name", "energy", "valid"]
    assert table_summary["column_profiles"]["energy"]["empty_count"] == 1

    (workspace / "code/inspect.py").write_text("print('ok')\n", encoding="utf-8")
    validation = validate_analysis_program(
        AnalysisJobRequest(
            runtime="core",
            script_path="code/inspect.py",
            inputs=declarations,
        )
    )
    assert validation["input_inspection"]["inputs"][0]["format"] == "json"


def test_execution_resource_status_lists_blocking_active_jobs(workspace: Path) -> None:
    job = workspace / "outputs/execution_jobs/job_blocking"
    job.mkdir(parents=True)
    (job / "status.json").write_text(
        json.dumps(
            {
                "job_id": "job_blocking",
                "job_type": "programmable_analysis",
                "status": "running",
                "resource_limits": {
                    "cpu_cores": 2,
                    "memory_mb": 1024,
                    "gpu_count": 0,
                },
                "metadata": {"label": "blocking-analysis"},
            }
        ),
        encoding="utf-8",
    )
    result = get_execution_resources(ExecutionResourceRequest())
    assert result["active_job_count"] == 1
    assert result["active_jobs"][0]["job_id"] == "job_blocking"
    assert result["currently_reserved"]["cpu_cores"] == 2


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
        "assert ctx.input_dir() == ctx.inputs_dir == ctx.root / 'inputs'\n"
        "assert ctx.output_dir() == ctx.outputs_dir == ctx.root / 'outputs'\n"
        "assert os.environ['PYTHONNOUSERSITE'] == '1'\n"
        "assert 'site-packages' not in os.environ.get('PYTHONPATH', '')\n"
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
    assert preflight["job_context_compliance"]["status"] == "compliant"

    submitted = submit_analysis_program(request)
    assert submitted["status"] == "success"
    assert submitted["job_context_compliance"]["status"] == "compliant"
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


def test_failed_program_returns_structured_failure_diagnostic(workspace: Path) -> None:
    (workspace / "code/failing.py").write_text(
        "record = {'energy': -1.0}\nprint(record['qh_gibbs'])\n",
        encoding="utf-8",
    )
    submitted = submit_analysis_program(
        AnalysisJobRequest(runtime="core", script_path="code/failing.py")
    )
    finished = _wait(submitted["job_id"])
    assert finished["job"]["status"] == "failed"
    diagnostic = finished["failure_diagnostic"]
    assert diagnostic["classification"] == "missing_mapping_key"
    assert diagnostic["details"]["missing_key"] == "qh_gibbs"
    assert diagnostic["source_line"] == 2
    diagnostic_path = (
        workspace
        / "outputs/execution_jobs"
        / submitted["job_id"]
        / "failure_diagnostic.json"
    )
    assert diagnostic_path.is_file()


def test_scientific_output_validation_covers_hessian_and_eos(tmp_path: Path) -> None:
    hessian = tmp_path / "hessian.json"
    hessian.write_text(
        json.dumps({"matrix": [[1.0, 0.0], [0.0, 2.0]], "unit": "hartree/bohr^2"}),
        encoding="utf-8",
    )
    hessian_check = _validate_scientific_output(
        hessian,
        {"semantic_type": "Hessian", "media_type": "application/json"},
    )
    assert hessian_check["status"] == "valid"
    assert "dense_square_dimension=2" in hessian_check["checks"]

    eos = tmp_path / "eos.json"
    eos.write_text(
        json.dumps(
            {
                "points": [
                    {"volume_ang3": volume, "energy_ev": energy}
                    for volume, energy in ((10, -1.0), (11, -1.2), (12, -1.1), (13, -0.8))
                ],
                "fit": {"status": "converged", "rmse": 0.002},
            }
        ),
        encoding="utf-8",
    )
    eos_check = _validate_scientific_output(
        eos,
        {"semantic_type": "EquationOfStateResult", "media_type": "application/json"},
    )
    assert eos_check["status"] == "valid"
    assert "fit_status=converged" in eos_check["checks"]

    invalid = json.loads(eos.read_text(encoding="utf-8"))
    del invalid["fit"]["rmse"]
    eos.write_text(json.dumps(invalid), encoding="utf-8")
    failed = _validate_scientific_output(
        eos,
        {"semantic_type": "EquationOfStateResult", "media_type": "application/json"},
    )
    assert failed["status"] == "invalid"
    assert "finite residual" in failed["errors"][0]
