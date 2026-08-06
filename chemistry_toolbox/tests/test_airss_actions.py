from __future__ import annotations

import shutil
from pathlib import Path

from chemistry_toolbox.src.backends import periodic
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
AIRSS = ROOT / ".software_cache" / "installations" / "airss" / "0.9.3"
SEED = ROOT / "chemistry_toolbox" / "examples" / "integration" / "airss" / "al8_seed.cell"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)


def _request(seed_file: Path) -> dict:
    return {
        "inputs": {"seed_file": str(seed_file)},
        "method_spec": {},
        "action_settings": {"candidate_count": 2},
        "resource_limits": {"cpu_cores": 1, "walltime_seconds": 30},
    }


def _stage_seed(tmp_path: Path) -> Path:
    return Path(shutil.copy2(SEED, tmp_path / "seed.cell"))


def test_airss_generates_real_crystal_candidates(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv(
        "CHEMGRAPH_AIRSS_BUILDCELL_COMMAND", str(AIRSS / "bin" / "buildcell")
    )
    monkeypatch.setenv("LD_LIBRARY_PATH", str(AIRSS / "lib"))
    result = _execute(
        "generate_crystal_structure_candidates", "airss", _request(_stage_seed(tmp_path))
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "0.9.3"
    assert result["result"]["candidate_count"] == 2
    assert result["result"]["relaxed"] is False
    assert result["result"]["ranked"] is False
    for candidate in result["result"]["candidates"]:
        assert len(candidate["structure"]["atoms"]) == 8
        assert candidate["structure"]["pbc"] == [True, True, True]


def test_airss_converts_generated_cell_to_xyz(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv(
        "CHEMGRAPH_AIRSS_BUILDCELL_COMMAND", str(AIRSS / "bin" / "buildcell")
    )
    monkeypatch.setenv("CHEMGRAPH_AIRSS_CABAL_COMMAND", str(AIRSS / "bin" / "cabal"))
    monkeypatch.setenv("LD_LIBRARY_PATH", str(AIRSS / "lib"))
    generated = _execute(
        "generate_crystal_structure_candidates", "airss", _request(_stage_seed(tmp_path))
    )
    candidate_path = tmp_path / generated["result"]["candidates"][0]["structure_file"]
    converted = _execute(
        "convert_crystal_structure_format",
        "airss",
        {
            "inputs": {"structure_file": str(candidate_path)},
            "method_spec": {},
            "action_settings": {"input_format": "cell", "output_format": "xyz"},
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 30},
        },
    )
    assert converted["status"] == "success"
    output_path = tmp_path / converted["result"]["structure_file"]
    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert lines[0].strip() == "8"
    assert len(lines) >= 10
