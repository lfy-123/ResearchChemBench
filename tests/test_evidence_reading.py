import json

import pytest

from evaluation.provenance.evidence_archive import build_run_index
from evaluation.scoring.evidence_reading import json_projection, read_registered_evidence


def test_large_inventory_is_projected_and_array_pages_keep_provenance(tmp_path):
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    path = outputs / "result.json"
    path.write_text(json.dumps({"action_result": {"status": "success", "output_artifacts": ["irrelevant" * 100] * 3000,
        "result": {"modes": list(range(10000)), "energy": -40.2}, "error": {"message": "diagnostic retained"}}}))
    index = build_run_index(tmp_path)
    ref = "workspace/outputs/result.json"
    projection = json_projection(index, ref, action=True)
    assert projection["value"]["result"]["energy"] == -40.2
    assert projection["value"]["error"]["message"] == "diagnostic retained"
    assert len(json.dumps(projection)) < 6000
    page = read_registered_evidence(index, {"ref": ref, "selector": "/action_result/result/modes", "array_start": 9998, "array_count": 2})
    assert page["value"]["items"] == [9998, 9999]
    assert page["value"]["length"] == 10000 and page["truncated"]
    scalar = read_registered_evidence(index, {"ref": ref, "selector": "/action_result/result/energy"})
    assert scalar["value"] == -40.2 and not scalar["truncated"]
    with pytest.raises(ValueError, match="registered"):
        read_registered_evidence(index, {"ref": "workspace/../secret"})


def test_pointer_escaping_and_no_silent_jsonpath_first_match(tmp_path):
    (tmp_path / "report").mkdir()
    (tmp_path / "report/data.json").write_text(json.dumps({"a/b": {"x~y": 2}, "values": [1, 2]}))
    index = build_run_index(tmp_path)
    ref = "workspace/report/data.json"
    assert json_projection(index, ref, pointer="/a~1b/x~0y")["value"] == 2
    assert len(json.loads(read_registered_evidence(index, {"ref": ref, "selector": "$.values[*]"})["content"])) == 2
    with pytest.raises(ValueError, match="does not exist"):
        json_projection(index, ref, pointer="/missing")


@pytest.mark.parametrize("body", ["", '{"broken":', '{"number":NaN}', '{"a":1} {"b":2}'])
def test_malformed_structured_evidence_is_a_diagnostic(tmp_path, body):
    from evaluation.scoring.evidence import build_evidence_bundle
    (tmp_path / "report").mkdir()
    (tmp_path / "report/broken.json").write_text(body)
    index = build_run_index(tmp_path)
    with pytest.raises(ValueError, match="JSON"):
        json_projection(index, "workspace/report/broken.json")
    bundle = build_evidence_bundle(index)
    assert bundle["coverage"]["errors"][0]["ref"] == "workspace/report/broken.json"
    assert bundle["coverage"]["retrieval_available"]


def test_table_lines_multiframe_and_unknown_binary_keep_context(tmp_path):
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs/values.csv").write_text("time(s),energy(eV)\n0,-1\n1,-2\n2,-3\n")
    (tmp_path / "outputs/frames.xyz").write_text("1\nframe 1\nHe 0 0 0\n1\nframe 2\nHe 1 0 0\n")
    (tmp_path / "outputs/raw.bin").write_bytes(b"\x00\xff")
    index = build_run_index(tmp_path)
    page = read_registered_evidence(index, {"ref": "workspace/outputs/values.csv", "start_line": 3, "line_count": 1})
    assert page["content"] == "1,-2\n" and page["line_start"] == page["line_end"] == 3
    assert page["table_context"]["header_excerpt"] == "time(s),energy(eV)\n"
    last_frame = read_registered_evidence(index, {"ref": "workspace/outputs/frames.xyz", "start_line": 4, "line_count": 3})
    assert "frame 2" in last_frame["content"] and last_frame["truncated"]
    assert last_frame["structure_context"]["frame_identity"] == "not_parsed"
    with pytest.raises(ValueError, match="binary"):
        read_registered_evidence(index, {"ref": "workspace/outputs/raw.bin"})
