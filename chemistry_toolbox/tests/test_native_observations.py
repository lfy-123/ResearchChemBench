from chemistry_toolbox.src.native_observations import parse_native_observations
from chemistry_toolbox.mcp.open_execution import _execution_status_axes, _gaussian_segment_sections, _validate_gaussian_input_deck
from chemistry_toolbox.mcp.execution_models import NativeJobRequest


def block(values, end=True):
    return "VIBRATIONAL FREQUENCIES\n" + "".join(f" {i}: {x} cm**-1\n" for i, x in enumerate(values)) + ("NORMAL MODES\n" if end else "")


def test_historical_hessians_do_not_accumulate(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_FEEDBACK_SCHEMA_VERSION", "2")
    path = tmp_path / "stdout.log"
    path.write_text(block([-200, -100, 100]) * 6 + "THE OPTIMIZATION HAS CONVERGED\n" + block([-80, 0, 200]) + "ORCA TERMINATED NORMALLY\n")
    result = parse_native_observations("orca", path)
    assert len(result["frequency_blocks"]) == 7
    assert result["final_frequency_block"] == 6
    assert result["frequency_blocks"][6]["negative_frequencies_cm_1"] == [-80]
    axes = _execution_status_axes(tmp_path, {"status": "success", "job_type": "native_software", "metadata": {"software_id": "orca", "calculation_intent": "transition_state"}})
    assert axes["scientific_validation_status"] == "not_assessed"
    assert axes["convergence_status"] == "converged"


def test_truncated_or_multiple_segments_are_explicit(tmp_path):
    path = tmp_path / "stdout.log"
    path.write_text(block([-20, 10]) + block([-30], end=False))
    result = parse_native_observations("orca", path)
    assert result["final_frequency_block"] is None
    assert result["frequency_association"] == "incomplete"
    path.write_text(block([-20, 10]) + "ORCA TERMINATED NORMALLY\nJOB NUMBER 2\n" + block([-30, 20]))
    result = parse_native_observations("orca", path)
    assert result["status"] == "ambiguous"
    assert result["normal_termination"] is False


def test_nonzero_exit_preserves_software_facts(tmp_path):
    (tmp_path / "stdout.log").write_text("SCF CONVERGED\nORCA finished by error\n")
    result = _execution_status_axes(tmp_path, {"status": "failed", "return_code": 1, "job_type": "native_software", "metadata": {"software_id": "orca"}})
    assert result["software_status"] == "failed"
    assert result["observations"]["scf_converged"] is True


def test_missing_footer_is_unknown_and_operator_stop_is_interrupted(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_FEEDBACK_SCHEMA_VERSION", "2")
    (tmp_path / "stdout.log").write_text("SCF CONVERGED\n")
    status = {"job_type":"native_software", "process_started":True, "status":"success", "return_code":0, "metadata":{"software_id":"orca"}}
    assert _execution_status_axes(tmp_path, status)["software_status"] == "unknown"
    assert _execution_status_axes(tmp_path, {**status,"status":"cancelled"})["software_status"] == "interrupted"
    assert _execution_status_axes(tmp_path, {**status,"status":"running"})["software_status"] == "running"


def test_hessian_cross_check_is_stage_specific_and_never_substitutes(tmp_path):
    log = tmp_path / "stdout.log"
    log.write_text(block([-40, 0, 100]) + block([-20, 0, 100]))
    hess = tmp_path / "arbitrary_name.hess"
    hess.write_text("$vibrational_frequencies\n3\n0 -40.0001\n1 0\n2 100\n$atoms\n1\nHe 4.0 0 0 0\n$end\n")
    record = parse_native_observations("orca", [log, hess])
    assert record["final_frequency_block"] == 1
    assert record["hessian_cross_checks"][0]["matching_blocks"] == [0]
    assert record["frequency_blocks"][1]["negative_frequencies_cm_1"] == [-20]
    hess.write_text(hess.read_text().replace("$atoms\n1", "$atoms\n2"))
    record = parse_native_observations("orca", [log, hess])
    assert record["hessian_cross_checks"][0]["complete"] is False
    assert record["hessian_cross_checks"][0]["matching_blocks"] == []


def test_qst_and_advisory_dont_edit_input(tmp_path, monkeypatch):
    import pytest
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_NATIVE_INPUT_VALIDATION_POLICY", "advisory")
    text = "%NProcShared=1\n# hf/sto-3g opt=(qst3,calcfc)\n\ntitle\n\n0 1\nHe 0 0 0\n\n"
    assert _gaussian_segment_sections(text, 1)["calculation_intent"] == "transition_state"
    path = tmp_path / "input.gjf"
    path.write_text(text.rstrip())
    request = NativeJobRequest(software_id="gaussian", executable="g16", stdin_target="input.gjf", staged_inputs=[{"source_path": "input.gjf", "target_path": "input.gjf"}])
    result = _validate_gaussian_input_deck(request)
    assert result["observations"]
    assert path.read_text() == text.rstrip()
    path.write_text(text.replace("%NProcShared=1", "%NProcShared=99999"))
    with pytest.raises(ValueError, match="cpu_mismatch"):
        _validate_gaussian_input_deck(request)


def test_gaussian_reports_requested_and_native_optimization_limits(tmp_path):
    path = tmp_path / "gaussian.log"
    path.write_text(
        "#p b3lyp/6-31g(d) opt=(maxcycles=200)\n"
        "Step number 108 out of a maximum of 108\n"
        " NStep=108\nNormal termination of Gaussian 16\n"
    )
    record = parse_native_observations("gaussian", path)
    assert record["gaussian_requested_max_cycles"] == [
        {"value": 200, "line": 1, "source": "route"}
    ]
    assert record["gaussian_optimization_progress"]["last_step"]["step"] == 108
    assert record["gaussian_optimization_progress"]["reported_maximum"] == 108
    assert record["gaussian_optimization_progress"]["nstep"]["value"] == 108
