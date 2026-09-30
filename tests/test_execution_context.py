import json

import pytest

from evaluation.execution.recovery import locate_workspace, RunRecoveryError
from chemistry_toolbox.src.execution_contract import action_execution_description


def test_locator_supports_actual_batch_layout_and_rejects_ambiguity(tmp_path):
    run_id="autonomous_research-paper_fixture-codex-example"
    workspace=tmp_path/"runs"/"cli_runs"/"batch_a"/run_id
    (workspace/"recovery").mkdir(parents=True)
    (workspace/"recovery"/"run.json").write_text("{}")
    for root in (tmp_path,tmp_path/"runs",tmp_path/"runs"/"cli_runs",workspace.parent,workspace):
        assert locate_workspace(root,run_id)==workspace
    duplicate=tmp_path/"runs"/"cli_runs"/"batch_b"/run_id
    (duplicate/"recovery").mkdir(parents=True);(duplicate/"recovery"/"run.json").write_text("{}")
    with pytest.raises(RunRecoveryError,match="ambiguous"):locate_workspace(tmp_path,run_id)


def test_description_distinguishes_persistent_and_optional_key():
    assert "recovery-enabled run" in action_execution_description(True)
    assert "when a submission_key is provided" in action_execution_description(False)
    for mode in (True,False):
        assert "structured diagnostics" in action_execution_description(mode)
