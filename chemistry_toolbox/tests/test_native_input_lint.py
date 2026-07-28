from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from chemistry_toolbox.mcp.execution_models import NativeJobRequest, StagedInput
from chemistry_toolbox.mcp.open_execution import validate_native_job
from researchchem_toolbox.models import ResourceLimits


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = TOOLBOX_ROOT / "examples" / "native"


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for name in ("code", "outputs", "report", "tool_logs"):
        (tmp_path / name).mkdir()
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    return tmp_path


def _copy_text(workspace: Path, source: Path, name: str) -> StagedInput:
    target = workspace / "code" / name
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return StagedInput(source_path=f"code/{name}", target_path=name)


def _write(workspace: Path, name: str, content: str) -> StagedInput:
    target = workspace / "code" / name
    target.write_text(content, encoding="utf-8")
    return StagedInput(source_path=f"code/{name}", target_path=name)


def test_native_smoke_manifest_matches_versioned_examples() -> None:
    manifest = json.loads((EXAMPLES / "smoke_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["cases"]) == 5
    assert all(case["process_status"] == "success" for case in manifest["cases"])
    for case in manifest["cases"]:
        if isinstance(case.get("source_sha256"), str):
            path = TOOLBOX_ROOT.parent / case["example_path"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == case["source_sha256"]


def test_reviewed_orca_gaussian_and_crest_examples_pass_lint(workspace: Path) -> None:
    orca = _copy_text(workspace, EXAMPLES / "orca/single_point/input.inp", "orca.inp")
    result = validate_native_job(
        NativeJobRequest(
            software_id="orca",
            executable="orca",
            arguments=["orca.inp"],
            staged_inputs=[orca],
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        )
    )
    assert result["input_deck_validation"]["lint_profile"] == "orca_high_frequency_v1"

    gaussian = _copy_text(
        workspace, EXAMPLES / "gaussian/link1/input.gjf", "gaussian.gjf"
    )
    result = validate_native_job(
        NativeJobRequest(
            software_id="gaussian",
            executable="g16",
            stdin_target="gaussian.gjf",
            staged_inputs=[gaussian],
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        )
    )
    assert result["input_deck_validation"]["link1_segment_count"] == 2

    crest = _copy_text(
        workspace, EXAMPLES / "crest/conformer_search/input.xyz", "input.xyz"
    )
    result = validate_native_job(
        NativeJobRequest(
            software_id="crest",
            executable="crest",
            arguments=["input.xyz", "--gfn2", "--T", "1"],
            staged_inputs=[crest],
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        )
    )
    assert result["input_deck_validation"]["selected_mode"] == "conformer_search"


def test_vasp_and_lobster_fixed_file_examples_pass_lint(workspace: Path) -> None:
    vasp_inputs = [
        _copy_text(workspace, EXAMPLES / f"vasp/ground_state/{name}", name)
        for name in ("INCAR", "POSCAR", "KPOINTS")
    ]
    vasp_inputs.append(
        _write(workspace, "POTCAR", "TITEL = PAW_PBE Si test\nVRHFIN =Si:\n")
    )
    result = validate_native_job(
        NativeJobRequest(
            software_id="vasp",
            executable="vasp_std",
            staged_inputs=vasp_inputs,
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        )
    )
    assert result["input_deck_validation"]["atom_count"] == 2

    lobster_inputs = [
        _copy_text(workspace, EXAMPLES / "lobster/cohp/lobsterin", "lobsterin"),
        _copy_text(workspace, EXAMPLES / "vasp/ground_state/POSCAR", "lobster_POSCAR"),
        _write(workspace, "lobster_POTCAR", "TITEL = PAW_PBE Si test\n"),
        _write(workspace, "WAVECAR", "nonempty-wavecar-fixture"),
        _write(workspace, "CONTCAR", "nonempty-contcar-fixture"),
        _write(workspace, "lobster_KPOINTS", "nonempty-kpoints-fixture"),
        _write(workspace, "OUTCAR", "nonempty-outcar-fixture"),
        _write(workspace, "vasprun.xml", "<modeling/>\n"),
    ]
    lobster_inputs[1] = StagedInput(source_path="code/lobster_POSCAR", target_path="POSCAR")
    lobster_inputs[2] = StagedInput(source_path="code/lobster_POTCAR", target_path="POTCAR")
    lobster_inputs[5] = StagedInput(source_path="code/lobster_KPOINTS", target_path="KPOINTS")
    result = validate_native_job(
        NativeJobRequest(
            software_id="lobster",
            executable="lobster-5.1.0",
            staged_inputs=lobster_inputs,
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        )
    )
    assert result["input_deck_validation"]["wavecar_size_bytes"] > 0


@pytest.mark.parametrize(
    ("software_id", "executable", "arguments", "stdin_target", "files", "message"),
    [
        (
            "orca",
            "orca",
            ["bad.inp"],
            None,
            {"bad.inp": "! HF STO-3G\n%scf\n* xyz 0 1\nH 0 0 0\n*\n"},
            "orca_unclosed_block",
        ),
        (
            "gaussian",
            "g16",
            [],
            "bad.gjf",
            {"bad.gjf": "# HF/STO-3G\nTitle without route separator\n0 1\nH 0 0 0\n"},
            "gaussian_route_separator",
        ),
        (
            "crest",
            "crest",
            ["input.xyz", "--protonate", "--deprotonate"],
            None,
            {"input.xyz": "1\nH\nH 0 0 0\n"},
            "crest_conflicting_modes",
        ),
        (
            "vasp",
            "vasp_std",
            [],
            None,
            {"INCAR": "ENCUT=300\n", "POSCAR": "x\n", "KPOINTS": "x\n"},
            "vasp_missing_fixed_files",
        ),
        (
            "lobster",
            "lobster-5.1.0",
            [],
            None,
            {
                "lobsterin": "COHPstartEnergy -10\n", "POSCAR": "x\n", "POTCAR": "x\n",
                "WAVECAR": "", "CONTCAR": "x\n", "KPOINTS": "x\n", "OUTCAR": "x\n",
                "vasprun.xml": "<modeling/>\n",
            },
            "lobster_empty_fixed_files",
        ),
    ],
)
def test_high_frequency_lints_reject_known_immediate_failures(
    workspace: Path,
    software_id: str,
    executable: str,
    arguments: list[str],
    stdin_target: str | None,
    files: dict[str, str],
    message: str,
) -> None:
    staged = [_write(workspace, target, content) for target, content in files.items()]
    with pytest.raises(ValueError, match=message):
        validate_native_job(
            NativeJobRequest(
                software_id=software_id,
                executable=executable,
                arguments=arguments,
                stdin_target=stdin_target,
                staged_inputs=staged,
                resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
            )
        )
