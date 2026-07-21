from pathlib import Path

from evaluation.config import TASKS_DIR
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
        "backend",
        "action",
        "mcp",
    }
    for task_id in tasks:
        info = load_task_info(task_id)
        truth = load_ground_truth(task_id)
        words = {word.casefold().strip(".,:;()[]") for word in info["task"].split()}
        assert words.isdisjoint(forbidden_prompt_terms)
        assert truth["evaluation_mode"] == "rubric_100"
        assert truth["score_max"] == 100
        assert sum(item["max_score"] for item in truth["scoring_rubric"]) == 100
        assert len(info["archive_extractions"]) == 1


def test_task_and_ground_truth_are_separate():
    info = load_task_info("ChemGraph_001")
    truth = load_ground_truth("ChemGraph_001")
    assert info["category"] == "smiles_lookup"
    assert truth["expected_tool_calls"][0]["molecule_name_to_smiles"]["name"] == "sulfur dioxide"
    assert (TASKS_DIR / "ChemGraph_001" / "target_study" / "ground_truth.json").is_file()
