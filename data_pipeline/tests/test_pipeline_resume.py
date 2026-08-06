from src.core.io import write_json, write_jsonl
from src.orchestration.pipeline import _completed_stage_records


def test_completed_stage_records_requires_summary_and_expected_count(tmp_path):
    records = [{"paper_id": "p1"}, {"paper_id": "p2"}]
    write_jsonl(tmp_path / "decisions.jsonl", records)
    write_json(tmp_path / "summary.json", {"papers": 2})

    reused = _completed_stage_records(
        {"resume_completed_stages": True}, tmp_path, "decisions.jsonl", 2
    )
    assert reused == (records, {"papers": 2})
    assert (
        _completed_stage_records(
            {"resume_completed_stages": True}, tmp_path, "decisions.jsonl", 3
        )
        is None
    )
    assert (
        _completed_stage_records({}, tmp_path, "decisions.jsonl", 2) is None
    )
