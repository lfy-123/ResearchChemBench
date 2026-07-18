from pathlib import Path

from evaluation.config import TASKS_DIR
from evaluation.utils import list_tasks, load_ground_truth, load_task_info


def test_all_chemgraph_tasks_were_imported():
    tasks = list_tasks()
    assert len(tasks) == 40
    assert tasks[0] == "ChemGraph_001"
    assert tasks[-1] == "ChemGraph_040"


def test_task_and_ground_truth_are_separate():
    info = load_task_info("ChemGraph_001")
    truth = load_ground_truth("ChemGraph_001")
    assert info["category"] == "smiles_lookup"
    assert truth["expected_tool_calls"][0]["molecule_name_to_smiles"]["name"] == "sulfur dioxide"
    assert (TASKS_DIR / "ChemGraph_001" / "target_study" / "ground_truth.json").is_file()

