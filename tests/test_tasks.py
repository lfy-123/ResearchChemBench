import json
import re
from pathlib import Path

from evaluation.config import TASKS_DIR
from evaluation.run_task import TaskRunner
from evaluation.utils import list_tasks, load_ground_truth, load_task_info


def test_all_chemgraph_tasks_were_imported():
    tasks = list_tasks()
    chemgraph_tasks = [task for task in tasks if task.startswith("ChemGraph_")]
    assert len(chemgraph_tasks) == 40
    assert chemgraph_tasks[0] == "ChemGraph_001"
    assert chemgraph_tasks[-1] == "ChemGraph_040"


def test_six_heterobiaryl_tasks_use_complete_100_point_rubrics():
    tasks = [task for task in list_tasks() if task.startswith("Heterobiaryl_PV_")]
    assert tasks == [
        "Heterobiaryl_PV_01_Protonation",
        "Heterobiaryl_PV_02_CC_Selectivity",
        "Heterobiaryl_PV_03_CC_vs_CO",
        "Heterobiaryl_PV_04_Coupling_Mechanism",
        "Heterobiaryl_PV_05_Rate_Determining_Step",
        "Heterobiaryl_PV_06_End_to_End",
    ]
    forbidden_prompt_terms = {
        "gaussian",
        "orca",
        "goodvibes",
        "xtb",
        "backend",
        "action",
        "mcp",
    }
    for task_id in tasks:
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        visible_protocol = json.dumps(
            {
                "task": info["task"],
                "scientific_mode": info["scientific_mode"],
                "scientific_mode_description": info[
                    "scientific_mode_description"
                ],
                "scientific_requirements": info["scientific_requirements"],
                "required_deliverables": info["required_deliverables"],
            },
            ensure_ascii=False,
        ).casefold()
        for term in forbidden_prompt_terms:
            assert re.search(rf"\b{re.escape(term)}\b", visible_protocol) is None
        assert truth["evaluation_mode"] == "rubric_100"
        assert truth["score_max"] == 100
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        assert len(info["archive_extractions"]) == 1
        assert truth["evidence_gate_policy"]["judge_must_assess_all"] is True
        assert truth["evidence_gate_policy"]["gates"]
        expected_paths = [item["path"] for item in info["required_deliverables"]]
        assert truth["expected_structured_output"] == expected_paths

    for task_id in tasks[:5]:
        assert load_task_info(task_id)["scientific_mode"] == "focused_open_discovery"
    q6 = load_task_info(tasks[5])
    assert q6["scientific_mode"] == "independent_open_discovery"
    assert len(q6["scientific_requirements"]) >= 7
    assert {item["path"] for item in q6["required_deliverables"]} == {
        "report/research_plan.json",
        "report/stationary_points.csv",
        "report/energy_profile.csv",
        "report/mechanism_evidence.json",
        "report/failure_log.jsonl",
        "report/final_answer.json",
        "report/report.md",
    }


def test_q6_instruction_rendering_exposes_evidence_contract_without_fixed_workflow(
    tmp_path: Path,
):
    runner = TaskRunner(
        "Heterobiaryl_PV_06_End_to_End",
        agent_key="mock",
        workspace_root=tmp_path,
    )
    instructions = runner._build_instructions()
    assert "`independent_open_discovery`" in instructions
    assert "all nine unoptimized seeds" in instructions
    assert "report/stationary_points.csv" in instructions
    assert "report/final_answer.json" in instructions
    assert "not a prescribed calculation sequence" in instructions


def test_task_and_ground_truth_are_separate():
    info = load_task_info("ChemGraph_001")
    truth = load_ground_truth("ChemGraph_001")
    assert info["category"] == "smiles_lookup"
    assert truth["expected_tool_calls"][0]["molecule_name_to_smiles"]["name"] == "sulfur dioxide"
    assert (TASKS_DIR / "ChemGraph_001" / "target_study" / "ground_truth.json").is_file()
