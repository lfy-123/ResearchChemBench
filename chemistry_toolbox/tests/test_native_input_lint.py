from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from chemistry_toolbox.mcp.execution_models import NativeJobRequest, StagedInput
from chemistry_toolbox.mcp.open_execution import (
    _validate_goodvibes_invocation,
    validate_native_job,
)
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
        elif isinstance(case.get("source_sha256"), dict):
            paths = {Path(item).name: TOOLBOX_ROOT.parent / item for item in case["example_paths"]}
            for name, expected in case["source_sha256"].items():
                assert hashlib.sha256(paths[name].read_bytes()).hexdigest() == expected


def test_archived_native_smoke_evidence_is_independently_verifiable() -> None:
    script = TOOLBOX_ROOT / "scripts" / "run_native_smokes.py"
    spec = importlib.util.spec_from_file_location("run_native_smokes", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    evidence = TOOLBOX_ROOT / "evidence/native_smoke/20260728_reliability_fix_v3"
    result = module.verify(evidence)
    assert result == {"valid": True, "errors": [], "case_count": 5}
    manifest = json.loads((evidence / "manifest.json").read_text(encoding="utf-8"))
    assert all(case["calculation_intent"] for case in manifest["cases"])


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
    assert result["calculation_intent"] == "single_point"

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
    assert result["calculation_intent"] == "optimization_frequency"

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
    assert result["calculation_intent"] == "conformer_search"


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
    assert result["calculation_intent"] == "single_point"

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
    assert result["calculation_intent"] == "projection"


def test_vasp_geometry_optimization_aliases_ionic_relaxation(workspace: Path) -> None:
    vasp_inputs = [
        _write(
            workspace,
            "INCAR",
            "ENCUT = 300\nIBRION = 2\nNSW = 20\nEDIFF = 1E-5\nEDIFFG = -0.02\n",
        ),
        _copy_text(workspace, EXAMPLES / "vasp/ground_state/POSCAR", "POSCAR"),
        _copy_text(workspace, EXAMPLES / "vasp/ground_state/KPOINTS", "KPOINTS"),
        _write(workspace, "POTCAR", "TITEL = PAW_PBE Si test\nVRHFIN =Si:\n"),
    ]
    result = validate_native_job(
        NativeJobRequest(
            software_id="vasp",
            executable="vasp_std",
            staged_inputs=vasp_inputs,
            calculation_intent="geometry_optimization",
            resource_limits=ResourceLimits(memory_mb=1024, cpu_cores=1),
        )
    )
    assert result["status"] == "success"
    assert result["calculation_intent"] == "ionic_relaxation"


def test_goodvibes_native_lint_rejects_glob_sensitive_staged_names(
    workspace: Path,
) -> None:
    staged = _write(workspace, "frequency.log", "fixture\n")
    request = NativeJobRequest(
        software_id="goodvibes",
        executable="goodvibes",
        arguments=["[Int-I]/frequency.log"],
        staged_inputs=[
            StagedInput(
                source_path=staged.source_path,
                target_path="[Int-I]/frequency.log",
            )
        ],
    )
    with pytest.raises(ValueError, match="goodvibes_unsafe_staged_target"):
        _validate_goodvibes_invocation(request)


def test_goodvibes_native_lint_validates_spc_suffix_pairing(workspace: Path) -> None:
    frequency = _write(workspace, "species.log", "frequency fixture\n")
    single_point = _write(workspace, "species_DLPNO.out", "single point fixture\n")
    staged = [frequency, single_point]

    with pytest.raises(
        ValueError, match="goodvibes_spc_suffix_leading_underscore"
    ):
        _validate_goodvibes_invocation(
            NativeJobRequest(
                software_id="goodvibes",
                executable="goodvibes",
                arguments=["species.log", "--spc", "_DLPNO"],
                staged_inputs=staged,
            )
        )

    valid = _validate_goodvibes_invocation(
        NativeJobRequest(
            software_id="goodvibes",
            executable="goodvibes",
            arguments=["species.log", "--spc", "DLPNO"],
            staged_inputs=staged,
        )
    )
    assert "spc_suffix_pairing" in valid["checks"]

    with pytest.raises(ValueError, match="goodvibes_spc_pair_missing"):
        _validate_goodvibes_invocation(
            NativeJobRequest(
                software_id="goodvibes",
                executable="goodvibes",
                arguments=["species.log", "--spc", "OTHER"],
                staged_inputs=staged,
            )
        )


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
