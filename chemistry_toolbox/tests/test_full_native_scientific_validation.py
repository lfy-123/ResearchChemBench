from __future__ import annotations

import re
from pathlib import Path

from chemistry_toolbox.scripts import run_full_native_scientific_validation as native


def test_repaired_native_recipes_preserve_strict_execution_contracts() -> None:
    plans, disabled = native.build_plans()
    assert len(plans) == native.EXPECTED_ENABLED
    assert len(disabled) == native.EXPECTED_DISABLED
    by_case = {plan["case_id"]: plan for plan in plans}

    amber = by_case["amber_pmemd::pmemd.MPI"]
    assert amber["launcher"] == "mpirun"
    assert amber["launcher_arguments"] == ["-np", "2"]
    assert amber["execution_command"] == "pmemd.MPI"

    gamess = by_case["gamess::rungms"]["recipe"]
    assert gamess.environment == {
        "GMS_SCRATCH": "{workdir}/scratch",
        "GMS_RESTART": "{workdir}/scratch",
    }

    wannier = by_case["wannier90::wannier90.x"]["recipe"]
    win = next(item for item in wannier.inputs if item.target == "seedname.win")
    assert win.append_text == "\nselect_projections : 1-4\n"
    assert wannier.normal_markers == ("All done: wannier90 exiting",)

    kinbot = by_case["kinbot::kinbot"]["recipe"]
    kinbot_input = next(item for item in kinbot.inputs if item.target == "input.json")
    assert '"reaction_search": 0' in (kinbot_input.text or "")
    assert '"barrier_threshold": 200.0' in (kinbot_input.text or "")
    assert '"qc": "nwchem"' in (kinbot_input.text or "")
    assert kinbot.normal_markers == ("KinBot finished.",)
    assert "*_well*.out" in kinbot.artifacts
    assert kinbot.timeout_seconds == 1200

    wfoverlap = by_case["sharc::wfoverlap.x"]
    assert wfoverlap["arguments"] == ["-f", "ciovl.in"]
    assert wfoverlap["stdin_target"] == ""


def test_native_text_corpus_keeps_sparse_fortran_nuls_and_skips_binary(
    tmp_path: Path,
) -> None:
    text_log = tmp_path / "fortran.log"
    text_log.write_bytes(
        b"Info: scientific validation log\n"
        + b"\x00" * 200
        + b"normal exit after 1.0 seconds\n"
    )
    binary = tmp_path / "binary.dat"
    binary.write_bytes(b"binary" + b"\x00" * 128)

    corpus = native._corpus([text_log, binary])

    assert "normal exit after" in corpus
    assert "binary" not in corpus


def test_native_fatal_signature_does_not_match_documented_crash_warning() -> None:
    warning = "random crashes (e.g. segmentation faults)"
    actual = "Segmentation fault (core dumped)"
    assert not any(
        re.search(pattern, warning, flags=re.I) for pattern in native.FATAL_PATTERNS
    )
    assert any(
        re.search(pattern, actual, flags=re.I) for pattern in native.FATAL_PATTERNS
    )


def test_native_staged_source_append_is_recorded_and_materialized(
    tmp_path: Path, monkeypatch
) -> None:
    source = tmp_path / "fixture.win"
    source.write_text("num_wann = 4\n", encoding="utf-8")
    workdir = tmp_path / "work"
    workdir.mkdir()
    monkeypatch.setattr(native, "PROJECT_ROOT", tmp_path)
    item = native.src(
        "seedname.win",
        "fixture.win",
        append_text="select_projections : 1-4\n",
    )

    records = native._copy_input(item, workdir)

    assert records[0]["target"] == "seedname.win"
    assert (workdir / "seedname.win").read_text(encoding="utf-8") == (
        "num_wann = 4\nselect_projections : 1-4\n"
    )
