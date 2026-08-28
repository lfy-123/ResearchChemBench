#!/usr/bin/env python3
"""Run real native-command science checks; never count interface probes as pass.

The command inventory is derived from the three authoritative native software
registries. Every enabled command receives either a real input recipe or an
explicit blocked result. The JSON report is checkpointed after every command.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
for _path in (TOOLBOX_ROOT / "src", PROJECT_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from chemistry_toolbox.src.catalog import backend_specs
from chemistry_toolbox.src.runtime import resolve_executable, runtime_environment, runtime_spec


GUIDES_PATH = TOOLBOX_ROOT / "config" / "native_software_guides.yaml"
EXAMPLES_PATH = TOOLBOX_ROOT / "config" / "native_software_example_contracts.yaml"
MANUALS_PATH = TOOLBOX_ROOT / "config" / "native_software_manual_profiles.yaml"
REQUESTED_PATH = TOOLBOX_ROOT / "config" / "requested_software.yaml"
DEFAULT_OUTPUT = TOOLBOX_ROOT / "evidence/status/full_native_scientific_validation.json"
EXPECTED_SOFTWARE = 63
EXPECTED_ENABLED = 79
EXPECTED_DISABLED = 1

FATAL_PATTERNS = (
    r"error while loading shared libraries",
    r"\bGLIBCXX_[0-9.]+.*not found",
    r"\bCXXABI_[0-9.]+.*not found",
    r"segmentation fault\b",
    r"fortran runtime error",
    r"traceback \(most recent call last\)",
    r"cannot find primary config",
    r"module import timed out",
)


@dataclass(frozen=True)
class Input:
    target: str
    source: str | None = None
    text: str | None = None
    tree: bool = False
    includes: tuple[str, ...] = ("*",)
    sensitive: bool = False
    append_text: str | None = None

    def __post_init__(self) -> None:
        if (self.source is None) == (self.text is None):
            raise ValueError("Input requires exactly one of source or text")
        if self.append_text is not None and (self.text is not None or self.tree):
            raise ValueError("append_text is supported only for staged source files")
        target = PurePosixPath(self.target)
        if target.is_absolute() or ".." in target.parts:
            raise ValueError(f"unsafe input target: {self.target}")


@dataclass(frozen=True)
class Step:
    executable: str
    arguments: tuple[str, ...]
    label: str


@dataclass(frozen=True)
class Recipe:
    execution_command: str | None = None
    arguments: tuple[str, ...] | None = None
    inputs: tuple[Input, ...] = ()
    stdin_target: str | None = None
    artifacts: tuple[str, ...] = ("stdout.log",)
    science_patterns: tuple[str, ...] = ()
    science_descriptions: tuple[str, ...] = ()
    normal_markers: tuple[str, ...] = ()
    setup_steps: tuple[Step, ...] = ()
    launcher: str | None = None
    launcher_arguments: tuple[str, ...] = ()
    environment: dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 900
    blocked_reason: str | None = None


def src(
    target: str,
    source: str,
    *,
    sensitive: bool = False,
    append_text: str | None = None,
) -> Input:
    return Input(
        target=target,
        source=source,
        sensitive=sensitive,
        append_text=append_text,
    )


def txt(target: str, text: str) -> Input:
    return Input(target=target, text=text)


def subtree(target: str, source: str, *includes: str) -> Input:
    return Input(
        target=target,
        source=source,
        tree=True,
        includes=tuple(includes) or ("*",),
    )


WATER_XYZ = """3
water scientific validation
O  0.000000  0.000000  0.000000
H  0.758602  0.000000  0.504284
H -0.758602  0.000000  0.504284
"""

H2_XYZ = """2
H2 scientific validation
H 0.000000 0.000000 0.000000
H 0.000000 0.000000 0.740000
"""

SI_POSCAR = """Si scientific validation
1.0
5.430000 0.000000 0.000000
0.000000 5.430000 0.000000
0.000000 0.000000 5.430000
Si
2
Direct
0.000000 0.000000 0.000000
0.250000 0.250000 0.250000
"""

TWO_CHAIN_PDB = """ATOM      1  O   HOH A   5       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   5       0.957   0.000   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   5      -0.239   0.927   0.000  1.00  0.00           H
TER       4      HOH A   5
ATOM      4  O   HOH B  12       3.000   0.000   0.000  1.00  0.00           O
ATOM      5  H1  HOH B  12       3.957   0.000   0.000  1.00  0.00           H
ATOM      6  H2  HOH B  12       2.761   0.927   0.000  1.00  0.00           H
TER       8      HOH B  12
END
"""


# These are deliberate corrections at the runner boundary. The authoritative
# example contract is left unchanged so this audit can expose the drift.
CONTRACT_OVERRIDES: dict[tuple[str, str], dict[str, Any]] = {
    ("multiwfn", "Multiwfn_noGUI"): {
        "stdin_target": "commands.txt",
        "note": "commands.txt, not the wavefunction, is the stdin stream",
    },
    ("gaussian", "formchk"): {
        "inputs": ["input.chk"],
        "outputs": ["output.fchk"],
        "note": "output.fchk is an output, not an input",
    },
    ("gnina", "gnina"): {
        "inputs": ["receptor.pdbqt", "ligand.sdf"],
        "outputs": ["poses.sdf"],
        "note": "receptor.pdbqt is an input, not an output",
    },
    ("phonopy", "phonopy"): {
        "inputs": ["POSCAR"],
        "outputs": ["phonopy_disp.yaml", "POSCAR-*"],
        "note": "Phonopy v4 moved displacement generation from phonopy to phonopy-init",
    },
    ("phono3py", "phono3py"): {
        "inputs": ["POSCAR"],
        "outputs": ["phono3py_disp.yaml", "POSCAR-*"],
        "note": "Phono3py v4 moved displacement generation from phono3py to phono3py-init",
    },
    ("wannier90", "wannier90.x"): {
        "inputs": ["seedname.win"],
        "outputs": ["seedname.nnkp", "seedname.wout", "seedname.chk"],
        "note": "-pp requires seedname.win",
    },
}


# A blocked result is intentional only when a portable scientific calculation
# would require state that this repository cannot safely or honestly synthesize.
BLOCKED_REASONS: dict[tuple[str, str], str] = {
    ("aiida", "verdi"): (
        "A real AiiDA calculation needs an isolated configured profile and database; "
        "status/help output is not scientific validation."
    ),
    ("automekin", "amk.sh"): (
        "The full AutoMeKin workflow needs a reviewed control/start structure and QM "
        "configuration and spawns child jobs; only its portable MOPAC component has a fixture."
    ),
    ("automekin", "bbfs.exe"): (
        "This internal AutoMeKin component has no standalone scientific input contract and "
        "requires files generated by the parent workflow."
    ),
    ("censo", "censo"): (
        "A real CENSO calculation needs a conformer ensemble plus portable external-QM "
        "configuration; the cached configuration contains host-specific ORCA/xTB paths."
    ),
    ("charmm", "charmm"): (
        "CHARMM requires academic registration and a matched topology, parameter, coordinate, "
        "and command set; the cache contains output evidence but no redistributable staged input."
    ),
    ("critic2", "critic2"): (
        "A scientific Critic2 run needs a compatible real density or wavefunction and reviewed "
        "analysis input; no matching field fixture is registered."
    ),
    ("deepmd", "dp"): (
        "DeepMD validation needs an exact registered DPA model, its task head/branch, and a "
        "matching one-frame DeePMD dataset; a generic model.pb fixture is invalid for the "
        "registered multi-task PyTorch checkpoints."
    ),
    ("geometric", "geometric-optimize"): (
        "A geomeTRIC optimization needs a reviewed engine-specific molecular input and child "
        "engine; the documented <engine> placeholder is not executable."
    ),
    ("gnina", "gnina"): (
        "Scientific docking needs a prepared receptor/ligand pair and justified search box; no "
        "curated pair is registered, and arbitrary synthetic docking would not validate utility."
    ),
    ("lobster", "lobster-5.1.0"): (
        "LOBSTER requires its academic license plus a same-lineage upstream VASP, QE, or ABINIT "
        "wavefunction set; licensed POTCAR/WAVECAR data cannot be fabricated or redistributed."
    ),
    ("nequip", "nequip-train"): (
        "A real NequIP training run needs a labeled training/validation dataset and matching "
        "configuration; registered checkpoints are inference resources, not a training fixture."
    ),
    ("newton_x", "nx_geninp"): (
        "The interactive generator needs reviewed answers, molecular data, and interface files; "
        "a help or startup probe is not equivalent to generating a usable trajectory input."
    ),
    ("newton_x", "nx_moldyn"): (
        "Newton-X dynamics needs a complete control, initial-condition, and electronic-structure "
        "interface tree; nx_test is a separate installation test."
    ),
    ("pmx", "pmx"): (
        "A real pmx mutation/topology operation needs hydrogen-complete biomolecular input and a "
        "reviewed mutation and force-field mapping fixture."
    ),
    ("rmg", "rmg.py"): (
        "RMG model generation needs a bounded reactor/species input and an installed matching "
        "RMG database; no reviewed generation fixture is registered, while Arkane is separate."
    ),
    ("theodore", "theodore"): (
        "TheoDORE needs same-lineage excited-state orbital/density output and dens_ana.in; no "
        "compatible electronic-structure result bundle is registered."
    ),
    ("vasp", "vasp_std"): (
        "VASP requires a commercial license and locally licensed POTCAR data; POTCAR must not be "
        "embedded in or archived by this validation runner."
    ),
    ("vesta", "VESTA"): (
        "A real VESTA workflow is GUI-driven and needs Xvfb/display plus the matching graphics "
        "stack and an automated export assertion; -h or -nogui startup cannot pass."
    ),
    ("vina", "vina"): (
        "Scientific docking needs a prepared receptor/ligand PDBQT pair and justified search box; "
        "no curated pair is registered, and arbitrary synthetic docking is not a valid test."
    ),
    ("yambo", "p2y"): (
        "p2y must consume a compatible upstream Quantum ESPRESSO save database with exact "
        "directory semantics; the portable Yambo recipe starts from an already converted SAVE."
    ),
}


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if value.get("schema_version") != 1:
        raise ValueError(f"unsupported schema: {path}")
    return value


def _requested() -> dict[str, dict[str, Any]]:
    value = yaml.safe_load(REQUESTED_PATH.read_text(encoding="utf-8")) or {}
    return {
        str(item["name"]).lower().replace("-", "_"): item
        for item in value.get("requested_software", [])
        if isinstance(item, dict) and item.get("name")
    }


def _runtime(software_id: str, guide: dict[str, Any]) -> str:
    backend = backend_specs().get(software_id)
    requested = _requested().get(software_id, {})
    value = guide.get("runtime") or (
        backend.runtime if backend is not None else requested.get("environment")
    )
    if not value:
        raise ValueError(f"no runtime for {software_id}")
    return str(value)


def _license(software_id: str) -> str:
    backend = backend_specs().get(software_id)
    requested = _requested().get(software_id, {})
    return str(
        (getattr(backend, "license_class", None) if backend else None)
        or requested.get("license")
        or requested.get("license_class")
        or "unknown"
    )


def _recipes() -> dict[tuple[str, str], Recipe]:
    """Return reviewed real-input recipes; absent commands become blocked."""

    amber = ".software_cache/validation/amber/26/smoke/gb7_trx_serial"
    sisso = ".software_cache/validation/sisso/3.5/smoke/regression"
    namd = ".software_cache/validation/namd/3.0.2/smoke"
    amber_mdin = """PMEMD scientific minimization
&cntrl
 imin=1, maxcyc=5, cut=99.0, igb=7, saltcon=0.2, gbsa=1,
 ntpr=1, ntx=1, ntb=0, ig=71277,
/
"""
    kinbot_initial_well = """{
  "title": "formaldehyde_initial_well_validation",
  "smiles": "C=O",
  "charge": 0,
  "mult": 1,
  "reaction_search": 0,
  "families": ["h2_elim"],
  "skip_families": ["none"],
  "barrier_threshold": 200.0,
  "pes": 0,
  "conformer_search": 0,
  "rotor_scan": 0,
  "high_level": 0,
  "me": 0,
  "qc": "nwchem",
  "qc_command": "nwchem",
  "use_sella": true,
  "method": "b3lyp",
  "basis": "sto-3g",
  "scan_method": "b3lyp",
  "scan_basis": "sto-3g",
  "imagfreq_threshold": 100.0,
  "ppn": 1,
  "queuing": "local",
  "error_missing_local": true,
  "delete_intermediate_files": 0,
  "verbose": 1
}
"""
    pysis_config = """geom:
  type: cart
  fn: h2.xyz
calc:
  type: xtb
  charge: 0
  mult: 1
  gfn: 2
  pal: 1
opt:
  type: rfo
  max_cycles: 20
"""

    result: dict[tuple[str, str], Recipe] = {
        ("bagel", "BAGEL"): Recipe(
            arguments=("input.json",),
            inputs=(src("input.json", ".software_cache/validation/bagel/1.2.2/smoke/hf-fci/input.json"),),
            artifacts=("stdout.log",),
            normal_markers=("METHOD: FCI",),
            science_patterns=(
                r"SCF iteration converged",
                r"METHOD:\s+FCI",
                r"(?m)^\s*\d+\s+0\s+\*\s+-?\d+\.\d+",
            ),
            science_descriptions=("The requested HF/FCI method runs and reports finite state energy data.",),
            timeout_seconds=1200,
        ),
        ("vaspkit", "vaspkit"): Recipe(
            arguments=("-task", "601", "-file", "POSCAR", "-symprec", "1e-5"),
            inputs=(src("POSCAR", ".software_cache/validation/vaspkit/1.5.1/smoke/symmetry/POSCAR"),),
            artifacts=("stdout.log",),
            normal_markers=("VASPKIT Standard Edition 1.5.1", "Summary"),
            science_patterns=(r"(?i)(symmetr|space group|summary)",),
            science_descriptions=("The supplied Si structure yields a parseable symmetry summary.",),
        ),
        ("pyfrag", "pyfrag-orca"): Recipe(
            arguments=("input.inp", "scratch"),
            inputs=(
                src("input.inp", ".software_cache/validation/pyfrag/2019/smoke/orca-final/input.inp"),
                src("irc.amv", ".software_cache/validation/pyfrag/2019/smoke/orca-final/irc.amv"),
            ),
            artifacts=("fragment_energies.txt", "fragmentfiles/*.out", "stdout.log"),
            normal_markers=("ORCA TERMINATED NORMALLY",),
            science_patterns=(r"ORCA TERMINATED NORMALLY", r"[-+]?\d+\.\d+"),
            science_descriptions=("Every path frame produces complex/fragment energies and a finite activation-strain table.",),
            timeout_seconds=1800,
        ),
        ("sisso", "SISSO"): Recipe(
            arguments=(),
            inputs=(src("SISSO.in", f"{sisso}/SISSO.in"), src("train.dat", f"{sisso}/train.dat")),
            artifacts=("SISSO.out", "Models/**/*", "SIS_subspaces/**/*", "stdout.log"),
            normal_markers=("SISSO done successfully", "Have a nice day"),
            science_patterns=(r"(?i)(descriptor|model|expression)",),
            science_descriptions=("SISSO emits at least one sparse descriptor model from the regression fixture.",),
            timeout_seconds=1200,
        ),
        ("sisso", "SISSO_predict"): Recipe(
            arguments=(),
            inputs=(
                src("SISSO.out", f"{sisso}/SISSO.out"),
                src("predict.dat", f"{sisso}/predict.dat"),
                src("SISSO_predict_para", f"{sisso}/SISSO_predict_para"),
            ),
            artifacts=("predict_X.out", "predict_Y.out", "stdout.log"),
            normal_markers=("Prediction RMSE and MaxAE", "RMSE"),
            science_patterns=(r"(?i)(RMSE|prediction)", r"[-+]?\d+\.\d+"),
            science_descriptions=("The official predictor writes finite held-out coordinates and predictions.",),
        ),
        ("gmx_mmpbsa", "gmx_MMPBSA"): Recipe(
            arguments=(
                "-O", "-i", "mmpbsa.in", "-cs", "com.tpr", "-ct", "com_traj.xtc",
                "-ci", "index.ndx", "-cg", "3", "4", "-cp", "topol.top",
                "-o", "FINAL_RESULTS_MMPBSA.dat", "-eo", "FINAL_RESULTS_MMPBSA.csv", "-nogui",
            ),
            inputs=(subtree(
                "",
                ".software_cache/validation/gmx_mmpbsa/1.6.5/smoke/gmx_MMPBSA_test/examples/Protein_ligand/ST",
                "mmpbsa.in", "com.tpr", "com_traj.xtc", "index.ndx", "topol.top", "toppar/*",
            ),),
            artifacts=("FINAL_RESULTS_MMPBSA.dat", "FINAL_RESULTS_MMPBSA.csv", "gmx_MMPBSA.log", "stdout.log"),
            normal_markers=("Finalizing gmx_MMPBSA: [ERROR  ] = 0", "Finalized..."),
            science_patterns=(r"(?i)(DELTA\s+TOTAL|Delta Total|.TOTAL)", r"[-+]?\d+\.\d+"),
            science_descriptions=("The matched topology/trajectory fixture yields finite Delta TOTAL binding terms.",),
            timeout_seconds=1800,
        ),
        ("crest", "crest"): Recipe(
            arguments=("input.xyz", "--gfn2", "--T", "1", "--quick"),
            inputs=(src("input.xyz", "chemistry_toolbox/examples/native/crest/conformer_search/input.xyz"),),
            artifacts=("crest_conformers.xyz", "crest.energies", "stdout.log"),
            normal_markers=("CREST terminated normally",),
            science_patterns=(r"(?i)conformer", r"[-+]?\d+\.\d+"),
            science_descriptions=("CREST produces a finite-energy conformer ensemble with fixed atom order.",),
            timeout_seconds=1800,
        ),
        ("multiwfn", "Multiwfn_noGUI"): Recipe(
            arguments=("H2O.fch",),
            inputs=(
                src("H2O.fch", ".software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/examples/H2O.fch"),
                txt("commands.txt", "7\n5\n1\nn\n0\n0\nq\n"),
            ),
            stdin_target="commands.txt",
            artifacts=("stdout.log",),
            normal_markers=("Loaded H2O.fch successfully",),
            science_patterns=(r"Loaded H2O\.fch successfully", r"Atom\s+\d+\([^)]*\).*Net charge:"),
            science_descriptions=("Mulliken populations are printed for all water atoms and their charges can be summed.",),
        ),
        ("orca", "orca"): Recipe(
            arguments=("input.inp",),
            inputs=(src("input.inp", "chemistry_toolbox/examples/native/orca/single_point/input.inp"),),
            artifacts=("stdout.log", "input.gbw"),
            normal_markers=("ORCA TERMINATED NORMALLY",),
            science_patterns=(r"FINAL SINGLE POINT ENERGY\s+[-+0-9.DEd]+",),
            science_descriptions=("The water single point converges and returns a finite final energy.",),
            timeout_seconds=1200,
        ),
        ("gaussian", "g16"): Recipe(
            arguments=(),
            inputs=(src("input.gjf", "chemistry_toolbox/examples/native/gaussian/optimization/input.gjf"),),
            stdin_target="input.gjf",
            artifacts=("stdout.log", "*.chk"),
            normal_markers=("Normal termination of Gaussian",),
            science_patterns=(r"Optimization completed", r"SCF Done:.*[-+0-9.DEd]+"),
            science_descriptions=("The optimization completes with finite SCF energies and a checkpoint.",),
            environment={"GAUSS_SCRDIR": "{workdir}/scratch"},
            timeout_seconds=1800,
        ),
        ("gaussian", "formchk"): Recipe(
            arguments=("input.chk", "output.fchk"),
            inputs=(src("input.chk", ".software_cache/validation/gaussian/g16/smoke/freq/water_freq.chk"),),
            artifacts=("output.fchk", "stdout.log", "stderr.log"),
            normal_markers=("Atomic numbers", "Number of atoms"),
            science_patterns=(r"Atomic numbers\s+I\s+N=",),
            science_descriptions=("The formatted checkpoint is non-empty and contains the water atomic-number array.",),
        ),
        ("gamess", "rungms"): Recipe(
            arguments=("exam01", "00", "1"),
            inputs=(src("exam01.inp", ".software_cache/validation/gamess/2024-r2-p1/smoke/exam01.inp"),),
            artifacts=("stdout.log",),
            normal_markers=("EXECUTION OF GAMESS TERMINATED NORMALLY",),
            science_patterns=(r"(?i)(SCF IS CONVERGED|FINAL.*ENERGY IS)",),
            science_descriptions=("GAMESS reaches SCF convergence without a legacy server path in its launcher output.",),
            environment={
                "GMS_SCRATCH": "{workdir}/scratch",
                "GMS_RESTART": "{workdir}/scratch",
            },
            timeout_seconds=1200,
        ),
        ("goodvibes", "goodvibes"): Recipe(
            arguments=(
                "output.log", "--temp", "298.15", "--conc", "1.0", "--qs", "grimme",
                "--qh", "--fs", "100", "--fh", "100", "-v", "0.99",
                "--zpe-vscal", "0.98", "--json", "result.json",
            ),
            inputs=(src("output.log", ".software_cache/validation/gaussian/g16/smoke/freq/water_freq.log"),),
            artifacts=("result.json", "stdout.log"),
            normal_markers=("GoodVibes", "qh-G"),
            science_patterns=(r"(?i)(qh-G|quasi-harmonic|Gibbs)", r"[-+]?\d+\.\d+"),
            science_descriptions=("GoodVibes parses the completed frequency job and reports finite 298.15 K thermochemistry.",),
        ),
        ("pysisyphus", "pysis"): Recipe(
            arguments=("config.yaml",),
            inputs=(txt("config.yaml", pysis_config), txt("h2.xyz", H2_XYZ)),
            artifacts=("stdout.log", "*.xyz"),
            normal_markers=("Converged!",),
            science_patterns=(r"(?i)converged!", r"[-+]?\d+\.\d+"),
            science_descriptions=("The H2 xTB geometry optimization reaches its force convergence criterion.",),
            timeout_seconds=1200,
        ),
        ("mess", "mess"): Recipe(
            arguments=("input.inp",),
            inputs=(src("input.inp", ".software_cache/validation/mess/smoke/hco/hco.inp"),),
            artifacts=("input.out", "input.log", "ke.out", "stdout.log"),
            normal_markers=("rate calculation done",),
            science_patterns=(
                r"(?i)Temperature-Pressure Rate Tables",
                r"[-+]?\d+\.\d+(?:[Ee][-+]?\d+)?",
            ),
            science_descriptions=("The HCO master-equation fixture produces finite non-negative rate tables.",),
            timeout_seconds=1200,
        ),
        ("mesmer", "mesmer"): Recipe(
            arguments=("input.xml", "-o", "output.xml"),
            inputs=(src("input.xml", ".software_cache/validation/mesmer/smoke/examples/H2Ominimal/H2Ominimal.xml"),),
            artifacts=("output.xml", "stdout.log"),
            normal_markers=("MESMER", "calculation"),
            science_patterns=(r"(?i)(reaction|rate|population|calculation)",),
            science_descriptions=("The minimal H2O master-equation XML is solved and a parseable result XML is written.",),
        ),
        ("namd", "namd3"): Recipe(
            arguments=("+p1", "input.conf"),
            inputs=(
                src("input.conf", f"{namd}/minimal.namd"),
                src("CH_final.pdb", f"{namd}/CH_final.pdb"),
                src("CH_final.psf", f"{namd}/CH_final.psf"),
                src("CH_cgenff.prm", f"{namd}/CH_cgenff.prm"),
            ),
            artifacts=("namd_smoke.coor", "namd_smoke.vel", "namd_smoke.xsc", "stdout.log"),
            normal_markers=("End of program",),
            science_patterns=(r"(?m)^ENERGY:\s+0\s+[-+0-9.eE]+",),
            science_descriptions=("NAMD reports finite energy for the prepared PSF/PDB/parameter set and writes restart state.",),
        ),
        ("amber_pmemd", "pmemd"): Recipe(
            arguments=("-O", "-i", "mdin", "-o", "mdout", "-p", "topology.prmtop", "-c", "input.rst7", "-r", "output.rst7", "-x", "trajectory.nc"),
            inputs=(txt("mdin", amber_mdin), src("topology.prmtop", f"{amber}/prmtop"), src("input.rst7", f"{amber}/trxox.2.4ns.x")),
            artifacts=("mdout", "output.rst7", "stdout.log"),
            normal_markers=("Final Performance Info", "5.  TIMINGS"),
            science_patterns=(r"(?m)^\s*NSTEP\s+ENERGY", r"[-+]?\d+\.\d+"),
            science_descriptions=("Serial PMEMD completes five minimization cycles with finite energies and restart output.",),
        ),
        ("amber_pmemd", "pmemd.MPI"): Recipe(
            arguments=("-O", "-i", "mdin", "-o", "mdout", "-p", "topology.prmtop", "-c", "input.rst7", "-r", "output.rst7", "-x", "trajectory.nc"),
            inputs=(txt("mdin", amber_mdin), src("topology.prmtop", f"{amber}/prmtop"), src("input.rst7", f"{amber}/trxox.2.4ns.x")),
            artifacts=("mdout", "output.rst7", "stdout.log"),
            normal_markers=("Final Performance Info", "5.  TIMINGS"),
            science_patterns=(r"(?m)^\s*NSTEP\s+ENERGY", r"[-+]?\d+\.\d+"),
            science_descriptions=("MPI PMEMD initializes and completes the same finite-energy minimization workload.",),
            launcher="mpirun",
            launcher_arguments=("-np", "2"),
        ),
    }
    airss_cell = """#VARVOL=80
#NFORM=1
#SYMMOPS=1
#MINSEP=2.0
%BLOCK LATTICE_CART
5.43 0.00 0.00
0.00 5.43 0.00
0.00 0.00 5.43
%ENDBLOCK LATTICE_CART
%BLOCK POSITIONS_ABS
Si 0.0 0.0 0.0 # Si1 % NUM=1
Si 1.35 1.35 1.35 # Si2 % NUM=1
%ENDBLOCK POSITIONS_ABS
"""
    packmol_input = """tolerance 2.0
filetype xyz
output packed.xyz
structure water.xyz
 number 10
 inside box 0. 0. 0. 15. 15. 15.
end structure
"""
    lammps_input = """units lj
atom_style atomic
lattice fcc 0.8442
region box block 0 2 0 2 0 2
create_box 1 box
create_atoms 1 box
mass 1 1.0
pair_style lj/cut 2.5
pair_coeff 1 1 1.0 1.0 2.5
velocity all create 0.5 12345 mom yes rot no
fix integrator all nve
thermo 1
run 10
write_data final.data
"""
    psi4_input = """memory 500 mb
molecule water {
0 1
O  0.000000  0.000000  0.000000
H  0.758602  0.000000  0.504284
H -0.758602  0.000000  0.504284
}
set basis sto-3g
set e_convergence 1e-8
energy('scf')
"""
    nwchem_input = """start water_smoke
geometry units angstrom
 O  0.000000  0.000000  0.000000
 H  0.758602  0.000000  0.504284
 H -0.758602  0.000000  0.504284
end
basis
 * library sto-3g
end
scf
 thresh 1e-8
end
task scf energy
"""
    vmd_script = """mol new input.pdb type pdb waitfor all
set all [atomselect top all]
set n [$all num]
set center [measure center $all weight mass]
set rg [measure rgyr $all]
set out [open result.txt w]
puts $out "ATOMS=$n"
puts $out "CENTER=$center"
puts $out "RGYR=$rg"
close $out
$all writepdb selected.pdb
quit
"""

    result.update(
        {
            ("airss", "buildcell"): Recipe(
                arguments=(),
                inputs=(txt("seed.cell", airss_cell),),
                stdin_target="seed.cell",
                artifacts=("stdout.log",),
                normal_markers=("Generated by Buildcell", "%BLOCK LATTICE"),
                science_patterns=(r"(?is)LATTICE.*POSITIONS", r"(?m)^\s*Si\b"),
                science_descriptions=("AIRSS emits a two-Si CELL candidate with a positive explicit lattice.",),
                timeout_seconds=120,
            ),
            ("airss", "cabal"): Recipe(
                arguments=("cell", "xyz"),
                inputs=(txt("input.cell", airss_cell),),
                stdin_target="input.cell",
                artifacts=("stdout.log",),
                normal_markers=("Si",),
                science_patterns=(r"(?m)^\s*2\s*$", r"(?m)^\s*Si\s+[-+0-9.]"),
                science_descriptions=("cabal preserves the two-atom composition during CELL-to-XYZ conversion.",),
            ),
            ("openbabel", "obabel"): Recipe(
                arguments=("-ixyz", "input.xyz", "-osdf", "-O", "output.sdf"),
                inputs=(txt("input.xyz", WATER_XYZ),),
                artifacts=("output.sdf", "stdout.log", "stderr.log"),
                normal_markers=("1 molecule converted",),
                science_patterns=(r"\$\$\$\$",),
                science_descriptions=("The converted SDF is complete and retains one three-atom molecule.",),
            ),
            ("packmol", "packmol"): Recipe(
                arguments=(),
                inputs=(txt("packmol.inp", packmol_input), txt("water.xyz", WATER_XYZ)),
                stdin_target="packmol.inp",
                artifacts=("packed.xyz", "stdout.log"),
                normal_markers=("Success!", "Success"),
                science_patterns=(r"(?i)success",),
                science_descriptions=("Packmol places ten complete water molecules in the requested box.",),
            ),
            ("pdb_tools", "pdb_selchain"): Recipe(
                arguments=("-A",),
                inputs=(txt("input.pdb", TWO_CHAIN_PDB),),
                stdin_target="input.pdb",
                artifacts=("stdout.log",),
                normal_markers=("ATOM",),
                science_patterns=(r"(?m)^ATOM.{17}A", r"\A(?!.*^ATOM.{17}B).*\Z"),
                science_descriptions=("The output contains chain A atom records and excludes chain B.",),
            ),
            ("pdb_tools", "pdb_reres"): Recipe(
                arguments=("-1",),
                inputs=(txt("input.pdb", TWO_CHAIN_PDB),),
                stdin_target="input.pdb",
                artifacts=("stdout.log",),
                normal_markers=("ATOM",),
                science_patterns=(r"(?m)^ATOM.{18}\s*1\s", r"(?m)^ATOM.{18}\s*2\s"),
                science_descriptions=("Two residues are renumbered consecutively from one while atom records remain parseable.",),
            ),
            ("pdb_tools", "pdb_tidy"): Recipe(
                arguments=(),
                inputs=(txt("input.pdb", TWO_CHAIN_PDB),),
                stdin_target="input.pdb",
                artifacts=("stdout.log",),
                normal_markers=("ATOM", "END"),
                science_patterns=(r"(?m)^END\s*$",),
                science_descriptions=("The tidied PDB retains atom records and terminates with END.",),
            ),
            ("xtb", "xtb"): Recipe(
                arguments=("structure.xyz", "--gfn", "2", "--opt", "tight", "--chrg", "0", "--uhf", "0"),
                inputs=(txt("structure.xyz", WATER_XYZ),),
                artifacts=("xtbopt.xyz", "stdout.log"),
                normal_markers=("normal termination of xtb",),
                science_patterns=(r"(?i)geometry optimization converged", r"(?i)(?:version\s*)?6\.7\.1"),
                science_descriptions=("xTB 6.7.1, not 6.6.1, converges a real GFN2 water optimization.",),
                timeout_seconds=900,
            ),
            ("lammps", "lmp"): Recipe(
                arguments=("-in", "input.lammps"),
                inputs=(txt("input.lammps", lammps_input),),
                artifacts=("log.lammps", "final.data", "stdout.log"),
                normal_markers=("Loop time",),
                science_patterns=(r"(?m)^\s*10\s+[-+0-9.eE]+",),
                science_descriptions=("The finite LJ trajectory reaches step 10 and writes final atom data.",),
            ),
            ("psi4", "psi4"): Recipe(
                arguments=("input.dat", "output.dat", "-n", "1"),
                inputs=(txt("input.dat", psi4_input),),
                artifacts=("output.dat", "stdout.log"),
                normal_markers=("Psi4 exiting successfully",),
                science_patterns=(r"(?i)(Final Energy:|@RHF Final Energy:)\s*[-+0-9.DEd]+",),
                science_descriptions=("The water RHF/STO-3G calculation reaches SCF convergence with finite energy.",),
            ),
            ("nwchem", "nwchem"): Recipe(
                arguments=("input.nw",),
                inputs=(txt("input.nw", nwchem_input),),
                artifacts=("stdout.log",),
                normal_markers=("Total SCF energy", "Task  times"),
                science_patterns=(r"Total SCF energy\s*=\s*[-+0-9.DEd]+",),
                science_descriptions=("The water RHF/STO-3G task converges and reports finite total energy.",),
            ),
            ("phonopy", "phonopy"): Recipe(
                execution_command="phonopy-init",
                arguments=("POSCAR", "-d", "--dim", "2", "2", "2"),
                inputs=(txt("POSCAR", SI_POSCAR),),
                artifacts=("phonopy_disp.yaml", "POSCAR-*", "stdout.log"),
                normal_markers=("Summary of calculation was written in \"phonopy_disp.yaml\"",),
                science_patterns=(r"Generated number of supercells:\s*[1-9]\d*", r"Spacegroup:\s*\S+"),
                science_descriptions=("Phonopy writes a schema-valid displacement set and Si supercells.",),
            ),
            ("phono3py", "phono3py"): Recipe(
                execution_command="phono3py-init",
                arguments=("POSCAR", "-d", "--dim", "2", "2", "2", "--pa", "auto"),
                inputs=(txt("POSCAR", SI_POSCAR),),
                artifacts=("phono3py_disp.yaml", "POSCAR-*", "stdout.log"),
                normal_markers=("Displacement dataset was written", "phono3py_disp.yaml"),
                science_patterns=(r"Number of displacements:\s*[1-9]\d*", r"Spacegroup:\s*\S+"),
                science_descriptions=("Phono3py writes third-order displacement metadata and Si supercells.",),
            ),
            ("vmd", "vmd"): Recipe(
                arguments=("-dispdev", "text", "-e", "analysis.tcl"),
                inputs=(txt("analysis.tcl", vmd_script), txt("input.pdb", TWO_CHAIN_PDB)),
                artifacts=("result.txt", "selected.pdb", "stdout.log"),
                normal_markers=("Exiting normally.",),
                science_patterns=(r"ATOMS=6", r"RGYR=[-+0-9.eE]+"),
                science_descriptions=("Headless VMD loads six atoms, computes finite center/radius, and exports PDB.",),
            ),
        }
    )

    qe_input = """&CONTROL
 calculation='scf', prefix='si', pseudo_dir='./pseudo', outdir='./tmp'
/
&SYSTEM
 ibrav=2, celldm(1)=10.26, nat=2, ntyp=1, ecutwfc=20.0
/
&ELECTRONS
 conv_thr=1.0d-7, electron_maxstep=80
/
ATOMIC_SPECIES
Si 28.0855 Si.UPF
ATOMIC_POSITIONS crystal
Si 0.00 0.00 0.00
Si 0.25 0.25 0.25
K_POINTS gamma
"""
    abinit_input = """acell 3*10.26
rprim 0.0 0.5 0.5  0.5 0.0 0.5  0.5 0.5 0.0
natom 2
ntypat 1
typat 1 1
znucl 14
xred 0.0 0.0 0.0  0.25 0.25 0.25
ecut 8.0
ngkpt 1 1 1
nshiftk 1
shiftk 0.0 0.0 0.0
toldfe 1.0d-7
nstep 80
pseudos "Si.psp8"
"""
    siesta_input = """SystemName Si smoke
SystemLabel si
NumberOfAtoms 2
NumberOfSpecies 1
%block ChemicalSpeciesLabel
 1 14 Si
%endblock ChemicalSpeciesLabel
LatticeConstant 5.43 Ang
%block LatticeVectors
 1.0 0.0 0.0
 0.0 1.0 0.0
 0.0 0.0 1.0
%endblock LatticeVectors
AtomicCoordinatesFormat Fractional
%block AtomicCoordinatesAndAtomicSpecies
 0.00 0.00 0.00 1
 0.25 0.25 0.25 1
%endblock AtomicCoordinatesAndAtomicSpecies
MeshCutoff 60 Ry
PAO.BasisSize SZ
MaxSCFIterations 80
DM.Tolerance 1.d-4
%block kgrid_Monkhorst_Pack
 1 0 0 0.0
 0 1 0 0.0
 0 0 1 0.0
%endblock kgrid_Monkhorst_Pack
"""
    dftb_input = """Geometry = GenFormat {
 <<< "geometry.gen"
}
Hamiltonian = DFTB {
 SCC = Yes
 SCCTolerance = 1e-7
 MaxSCCIterations = 100
 SlaterKosterFiles = Type2FileNames {
  Prefix = "sk/"
  Separator = "-"
  Suffix = ".skf"
 }
 MaxAngularMomentum { Si = "d" }
 KPointsAndWeights = SupercellFolding {
  1 0 0
  0 1 0
  0 0 1
  0.0 0.0 0.0
 }
}
Options { WriteResultsTag = Yes }
"""
    dftb_geometry = """2 S
Si
1 1 0.0 0.0 0.0
2 1 1.3575 1.3575 1.3575
0.0 0.0 0.0
5.43 0.0 0.0
0.0 5.43 0.0
0.0 0.0 5.43
"""
    plumed_input = """d: DISTANCE ATOMS=1,2 NOPBC
PRINT ARG=d FILE=COLVAR STRIDE=1
"""
    trajectory_xyz = """2
frame 0
H 0.000 0.000 0.000
H 0.740 0.000 0.000
2
frame 1
H 0.000 0.000 0.000
H 0.760 0.000 0.000
"""
    qce_input = json.dumps(
        {
            "schema_name": "qcschema_input",
            "schema_version": 1,
            "molecule": {
                "symbols": ["O", "H", "H"],
                "geometry": [0.0, 0.0, 0.0, 0.0, 1.4323, 1.111, 0.0, -1.4323, 1.111],
                "molecular_charge": 0,
                "molecular_multiplicity": 1,
            },
            "driver": "energy",
            "model": {"method": "hf", "basis": "sto-3g"},
            "keywords": {"e_convergence": 8},
        },
        indent=2,
    ) + "\n"

    result.update(
        {
            ("quantum_espresso", "pw.x"): Recipe(
                arguments=("-in", "input.in"),
                inputs=(
                    txt("input.in", qe_input),
                    src("pseudo/Si.UPF", ".software_cache/shared/scientific-data/qe_pseudos/efficiency/Si.pbe-n-rrkjus_psl.1.0.0.UPF"),
                ),
                artifacts=("stdout.log", "tmp/si.save/**/*"),
                normal_markers=("JOB DONE.",),
                science_patterns=(r"convergence has been achieved", r"!\s+total energy\s+=\s+[-+0-9.DEd]+"),
                science_descriptions=("The Si SCF reaches the requested threshold and reports finite total energy.",),
                timeout_seconds=1200,
            ),
            ("abinit", "abinit"): Recipe(
                arguments=("input.abi",),
                inputs=(
                    txt("input.abi", abinit_input),
                    src("Si.psp8", ".software_cache/shared/scientific-data/abinit_pseudos/pseudo_dojo_psp8/pbe_s_sr/Si.psp8"),
                ),
                artifacts=("stdout.log",),
                normal_markers=("Calculation completed", "delivered 0"),
                science_patterns=(r"(?i)(converged|toldfe)", r"etotal\s+[-+0-9.DEd]+"),
                science_descriptions=("The Si SCF reaches toldfe and emits a finite total energy.",),
                timeout_seconds=1200,
            ),
            ("siesta", "siesta"): Recipe(
                arguments=(),
                inputs=(
                    txt("input.fdf", siesta_input),
                    src("Si.psml", ".software_cache/shared/scientific-data/siesta_pseudos/nc-sr-05_pbe_standard_psml/Si.psml"),
                ),
                stdin_target="input.fdf",
                artifacts=("stdout.log", "si.DM", "si.XV"),
                normal_markers=("Job completed", "siesta: Final energy"),
                science_patterns=(r"siesta:\s+Final energy", r"[-+]?\d+\.\d+"),
                science_descriptions=("The Si SCF completes with finite energy and density-matrix/coordinate outputs.",),
                timeout_seconds=1200,
            ),
            ("dftbplus", "dftb+"): Recipe(
                arguments=(),
                inputs=(
                    txt("dftb_in.hsd", dftb_input),
                    txt("geometry.gen", dftb_geometry),
                    src("sk/Si-Si.skf", ".software_cache/shared/scientific-data/dftb_params/matsci-0.3.0/skfiles/Si-Si.skf"),
                ),
                artifacts=("detailed.out", "results.tag", "stdout.log"),
                normal_markers=("DFTB+ running times",),
                science_patterns=(r"(?i)(SCC converged|Total Energy)", r"[-+]?\d+\.\d+"),
                science_descriptions=("The Si SCC calculation converges and writes finite tagged results.",),
            ),
            ("plumed", "plumed"): Recipe(
                arguments=(
                    "driver", "--plumed", "plumed.dat", "--ixyz", "trajectory.xyz",
                    "--length-units", "A", "--box", "10,10,10",
                ),
                inputs=(txt("plumed.dat", plumed_input), txt("trajectory.xyz", trajectory_xyz)),
                artifacts=("COLVAR", "stdout.log"),
                normal_markers=("PLUMED",),
                science_patterns=(r"#!\s+FIELDS\s+time\s+d", r"[-+]?\d+\.\d+"),
                science_descriptions=("PLUMED evaluates a finite H-H distance for each staged trajectory frame.",),
            ),
            ("qcengine", "qcengine"): Recipe(
                arguments=("run", "psi4", "input.json"),
                inputs=(txt("input.json", qce_input),),
                artifacts=("stdout.log",),
                normal_markers=('"success": true',),
                science_patterns=(r'"success"\s*:\s*true', r'"return_result"\s*:\s*[-+0-9.eE]+'),
                science_descriptions=("QCEngine returns a successful QCSchema water energy with finite return_result.",),
            ),
        }
    )

    tdep = ".software_cache/installations/tdep/25.03/source/examples/example_1_fcc_al"
    sharc = ".software_cache/validation/sharc/smoke/lvc_ensemble/TRAJ_00001"
    wannier = ".software_cache/validation/wannier90/smoke/qe_si"
    gpaw_program = """from ase import Atoms
from gpaw import GPAW
atoms = Atoms('H2', positions=[(0, 0, 0), (0, 0, 0.74)], cell=(8, 8, 8), pbc=False)
atoms.center()
atoms.calc = GPAW(mode='lcao', basis='sz(dzp)', xc='LDA', txt='gpaw.out')
energy = atoms.get_potential_energy()
forces = atoms.get_forces()
print(f'GPAW_SCIENTIFIC_ENERGY_EV={energy:.12f}')
print('GPAW_SCIENTIFIC_FORCE_NORM=', float((forces ** 2).sum() ** 0.5))
"""
    cp2k_input = """&GLOBAL
 PROJECT ar_smoke
 RUN_TYPE ENERGY
 PRINT_LEVEL LOW
&END GLOBAL
&FORCE_EVAL
 METHOD FIST
 &MM
  &FORCEFIELD
   &CHARGE
    ATOM Ar
    CHARGE 0.0
   &END CHARGE
   &NONBONDED
    &LENNARD-JONES
     ATOMS Ar Ar
     EPSILON [kcalmol] 0.238
     SIGMA [angstrom] 3.405
     RCUT [angstrom] 8.0
    &END LENNARD-JONES
   &END NONBONDED
  &END FORCEFIELD
  &POISSON
   PERIODIC XYZ
   &EWALD
    EWALD_TYPE EWALD
    GMAX 21 21 21
   &END EWALD
  &END POISSON
 &END MM
 &SUBSYS
  &CELL
   ABC 20.0 20.0 20.0
   PERIODIC XYZ
  &END CELL
  &COORD
   Ar 0.0 0.0 0.0
   Ar 4.0 0.0 0.0
  &END COORD
 &END SUBSYS
&END FORCE_EVAL
"""

    result.update(
        {
            ("gpaw", "gpaw"): Recipe(
                arguments=("python", "program.py"),
                inputs=(txt("program.py", gpaw_program),),
                artifacts=("gpaw.out", "stdout.log"),
                normal_markers=("GPAW_SCIENTIFIC_ENERGY_EV",),
                science_patterns=(r"GPAW_SCIENTIFIC_ENERGY_EV=[-+0-9.eE]+", r"GPAW_SCIENTIFIC_FORCE_NORM=\s*[-+0-9.eE]+"),
                science_descriptions=("GPAW converges an H2 LCAO calculation and returns finite energy/forces.",),
                timeout_seconds=1200,
            ),
            ("cp2k", "cp2k"): Recipe(
                arguments=("-i", "input.inp", "-o", "output.out"),
                inputs=(txt("input.inp", cp2k_input),),
                artifacts=("output.out", "stdout.log"),
                normal_markers=("PROGRAM ENDED AT",),
                science_patterns=(r"ENERGY\| Total FORCE_EVAL.*[-+0-9.DEd]+",),
                science_descriptions=("CP2K/FIST returns a finite Lennard-Jones energy for two argon atoms.",),
            ),
            ("tdep", "extract_forceconstants"): Recipe(
                blocked_reason="The bundled example lacks the validated infile.sim.hdf5 required by this registered extraction command.",
            ),
            ("tdep", "canonical_configuration"): Recipe(
                arguments=("--nconf", "2", "--temperature", "300", "--quantum"),
                inputs=(
                    src("infile.ucposcar", f"{tdep}/infile.ucposcar"),
                    src("infile.ssposcar", f"{tdep}/infile.ssposcar"),
                    src("infile.forceconstant", f"{tdep}/infile.forceconstant"),
                ),
                artifacts=("contcar_conf0001", "contcar_conf0002", "stdout.log"),
                normal_markers=("    2     +",),
                science_patterns=(
                    r"(?m)^\s*1\s+\+\s+(?:[-+]?\d+\.\d+\s+){5}[-+]?\d+\.\d+",
                    r"(?m)^\s*2\s+\+\s+(?:[-+]?\d+\.\d+\s+){5}[-+]?\d+\.\d+",
                ),
                science_descriptions=("TDEP generates two finite-temperature canonical configurations.",),
            ),
            ("tdep", "phonon_dispersion_relations"): Recipe(
                arguments=("--unit", "thz", "-nq", "20"),
                inputs=(
                    src("infile.ucposcar", f"{tdep}/infile.ucposcar"),
                    src("infile.forceconstant", f"{tdep}/infile.forceconstant"),
                ),
                artifacts=("outfile.dispersion_relations", "outfile.dispersion_relations.hdf5", "stdout.log"),
                normal_markers=("All done in", "Done in"),
                science_patterns=(r"(?i)(dispersion|q-point|frequency)", r"[-+]?\d+\.\d+"),
                science_descriptions=("TDEP writes finite phonon branches for the supplied force constants.",),
            ),
            ("shengbte", "ShengBTE"): Recipe(
                arguments=(),
                inputs=(
                    src("CONTROL", ".software_cache/installations/shengbte/source/Test-RTA/CONTROL"),
                    src("FORCE_CONSTANTS_2ND", ".software_cache/installations/shengbte/source/Test-RTA/FORCE_CONSTANTS_2ND"),
                    src("FORCE_CONSTANTS_3RD", ".software_cache/installations/shengbte/source/Test-RTA/FORCE_CONSTANTS_3RD"),
                ),
                artifacts=("BTE.KappaTensorVsT_RTA", "stdout.log"),
                normal_markers=("normal exit after",),
                science_patterns=(
                    r"(?m)^\s*300(?:\.0+)?\s+(?:[-+]?\d+\.\d+(?:[Ee][-+]?\d+)?\s+){8}[-+]?\d+\.\d+(?:[Ee][-+]?\d+)?\s*$",
                ),
                science_descriptions=("The official Test-RTA fixture yields a finite thermal-conductivity tensor.",),
                timeout_seconds=1800,
            ),
            ("arkane", "Arkane.py"): Recipe(
                arguments=("input.py",),
                inputs=(
                    src("input.py", ".software_cache/validation/rmg/smoke/H/input.py"),
                    src("H.py", ".software_cache/validation/rmg/smoke/H/H.py"),
                    src("H_cbsqb3.log", ".software_cache/validation/rmg/smoke/H/H_cbsqb3.log"),
                ),
                artifacts=("output.py", "stdout.log"),
                normal_markers=("Arkane execution terminated", "execution terminated"),
                science_patterns=(r"(?i)(thermo|wilhoit|heat capacity)",),
                science_descriptions=("Arkane derives finite H-atom thermochemistry from the staged quantum log.",),
                environment={"MPLCONFIGDIR": "{workdir}/scratch"},
                timeout_seconds=1200,
            ),
            ("automekin", "mopac"): Recipe(
                arguments=("water.mop",),
                inputs=(src("water.mop", ".software_cache/validation/automekin/smoke/water.mop"),),
                artifacts=("water.out", "water.arc", "stdout.log"),
                normal_markers=("JOB ENDED NORMALLY", "normal termination", "ended normally"),
                science_patterns=(r"(?i)(FINAL HEAT OF FORMATION|TOTAL ENERGY)\s*=\s*[-+0-9.DEd]+",),
                science_descriptions=("The bundled MOPAC component returns a finite PM7 water energy.",),
            ),
            ("kinbot", "kinbot"): Recipe(
                arguments=("input.json",),
                inputs=(txt("input.json", kinbot_initial_well),),
                artifacts=("kinbot.db", "kinbot.log", "*_well*.out", "stdout.log"),
                normal_markers=("KinBot finished.",),
                science_patterns=(
                    r"Total\s+(?:DFT|SCF)\s+energy\s*=\s*[-+]?\d+\.\d+",
                    r"Starting optimization of initial well",
                ),
                science_descriptions=(
                    "KinBot completes a bounded formaldehyde initial-well optimization and frequency workflow with a finite NWChem energy.",
                ),
                timeout_seconds=1200,
            ),
            ("kinbot", "pes"): Recipe(
                arguments=("input.json",),
                inputs=(src("input.json", ".software_cache/validation/kinbot/smoke/formaldehyde_pes_complete/input.json"),),
                artifacts=("pes.log", "chemids", "stdout.log"),
                normal_markers=("PES", "KinBot"),
                science_patterns=(r"(?i)(chemids|PES|reaction)",),
                science_descriptions=("The bounded PES workflow emits at least one validated chemid.",),
                timeout_seconds=3600,
            ),
            ("sharc", "sharc.x"): Recipe(
                arguments=("input",),
                inputs=(subtree(
                    "", sharc, "input", "geom", "veloc", "QM/LVC.resources",
                    "QM/LVC.template", "QM/runQM.sh", "QM/V.txt",
                ),),
                artifacts=("output.dat", "output.lis", "output.log", "restart.ctrl", "stdout.log"),
                normal_markers=("Total wallclock time:",),
                science_patterns=(r"(?m)^\s*60\s+30\.0000\b",),
                science_descriptions=("The LVC trajectory reaches its configured final time with finite state data.",),
                timeout_seconds=1800,
            ),
            ("sharc", "wfoverlap.x"): Recipe(
                arguments=("-f", "ciovl.in"),
                inputs=(subtree(
                    "", ".software_cache/installations/sharc/source/wfoverlap/test_jobs/CH2S_ricc2/IN_FILES",
                    "ciovl.in", "dets.1.old", "dets.1", "ao_ovl", "mos.old", "mos",
                ),),
                stdin_target="",
                artifacts=("stdout.log",),
                normal_markers=("Overlap matrix", "walltime: total"),
                science_patterns=(r"Overlap matrix <PsiA_i\|PsiB_j>", r"<PsiA\s+\d+\|\s+[-+0-9.eE]+"),
                science_descriptions=("wfoverlap produces a finite 3x3 electronic-state overlap matrix.",),
            ),
            ("newton_x", "nx_test"): Recipe(
                arguments=("-p", "1d-models", "-t", "01"),
                artifacts=("stdout.log", "stderr.log"),
                normal_markers=("Normal termination of testsuite",),
                science_patterns=(r"(?m)^\s*IERR\s*=\s*0\s*$",),
                science_descriptions=("Newton-X analytical test 1 must pass without a Fortran runtime error.",),
                timeout_seconds=1800,
            ),
            ("wannier90", "wannier90.x"): Recipe(
                arguments=("seedname",),
                inputs=(
                    src(
                        "seedname.win",
                        f"{wannier}/si.win",
                        append_text="\nselect_projections : 1-4\n",
                    ),
                    src("seedname.amn", f"{wannier}/si.amn"),
                    src("seedname.mmn", f"{wannier}/si.mmn"),
                    src("seedname.eig", f"{wannier}/si.eig"),
                ),
                setup_steps=(Step("wannier90.x", ("-pp", "seedname"), "preprocess"),),
                artifacts=("seedname.nnkp", "seedname.wout", "seedname.chk", "stdout.log"),
                normal_markers=("All done: wannier90 exiting",),
                science_patterns=(r"Final State", r"[-+]?\d+\.\d+"),
                science_descriptions=("Preprocessing and full Wannierization complete with finite final spreads.",),
                timeout_seconds=1200,
            ),
            ("yambo", "yambo"): Recipe(
                arguments=("-F", "input.in", "-J", "job"),
                inputs=(
                    src("input.in", ".software_cache/validation/yambo/smoke/qe_si_gw_bse/gw.in"),
                    subtree("SAVE", ".software_cache/validation/yambo/smoke/qe_si_gw_bse/SAVE"),
                ),
                artifacts=("o-*", "r-*", "stdout.log"),
                normal_markers=("Game Over & Game summary", "Timing Overview"),
                science_patterns=(r"(?i)(quasiparticle|QP|GW)", r"[-+]?\d+\.\d+"),
                science_descriptions=("The staged Si SAVE database yields finite GW quasiparticle data.",),
                timeout_seconds=1800,
            ),
        }
    )

    water_mol2 = """@<TRIPOS>MOLECULE
WATER
3 2 1 0 0
SMALL
USER_CHARGES

@<TRIPOS>ATOM
1 O1  0.0000  0.0000 0.0000 O.3 1 HOH -0.8340
2 H1  0.9572  0.0000 0.0000 H   1 HOH  0.4170
3 H2 -0.2390  0.9270 0.0000 H   1 HOH  0.4170
@<TRIPOS>BOND
1 1 2 1
2 1 3 1
@<TRIPOS>SUBSTRUCTURE
1 HOH 1 TEMP 0 **** **** 0 ROOT
"""
    sqm_input = """Run semi-empirical minimization
 &qmmm
    qm_theory='AM1', grms_tol=0.0005,
 scfconv=1.d-10, ndiis_attempts=700,   qmcharge=0,
 /
   8    O1        0.0000        0.0000        0.0000 
   1    H1        0.9570        0.0000        0.0000 
   1    H2       -0.2390        0.9270        0.0000 

"""
    gromacs_gro = """Argon scientific validation
1
    1AR      AR    1   1.500   1.500   1.500
   3.00000   3.00000   3.00000
"""
    gromacs_top = """[ defaults ]
1 2 yes 0.5 0.5
[ atomtypes ]
Ar 39.948 0.0 A 0.3405 0.997
[ moleculetype ]
AR 1
[ atoms ]
1 Ar 1 AR AR 1 0.0 39.948
[ system ]
Argon scientific validation
[ molecules ]
AR 1
"""
    gromacs_mdp = """integrator = md
dt = 0.001
nsteps = 10
nstlog = 1
nstenergy = 1
nstxout-compressed = 1
cutoff-scheme = Verlet
nstlist = 1
rlist = 1.0
rvdw = 1.0
rcoulomb = 1.0
coulombtype = Cut-off
vdwtype = Cut-off
pbc = xyz
gen-vel = yes
gen-temp = 100
gen-seed = 12345
constraints = none
"""
    openmolcas_input = """&GATEWAY
Coord
2
angstrom
H 0.000000 0.000000 0.000000
H 0.000000 0.000000 0.740000
Basis=STO-3G
Group=Nosym
&SEWARD
&SCF
Charge=0
Spin=1
"""
    result.update(
        {
            ("acpype", "acpype"): Recipe(
                arguments=("-i", "input.mol2", "-b", "molecule", "-n", "0", "-m", "1", "-c", "user", "-a", "gaff2", "-q", "sqm", "-o", "gmx"),
                inputs=(txt("input.mol2", water_mol2),),
                artifacts=("molecule.acpype/*prmtop", "molecule.acpype/*GMX.top", "stdout.log"),
                normal_markers=("Total time of execution", "ACPYPE"),
                science_patterns=(r"(?i)(topology|prmtop|gromacs)",),
                science_descriptions=("ACPYPE preserves the water atom/charge model and emits parseable AMBER/GROMACS topologies.",),
            ),
            ("openff_am1bcc", "antechamber"): Recipe(
                arguments=("-i", "input.mol2", "-fi", "mol2", "-o", "charged.mol2", "-fo", "mol2", "-c", "bcc", "-nc", "0"),
                inputs=(txt("input.mol2", water_mol2),),
                artifacts=("charged.mol2", "stdout.log", "stderr.log"),
                normal_markers=("Calculation completed", "sqm"),
                science_patterns=(r"@<TRIPOS>ATOM", r"[-+]?0\.\d+"),
                science_descriptions=("Antechamber writes a three-atom MOL2 whose AM1-BCC charges sum to zero.",),
            ),
            ("openff_am1bcc", "sqm"): Recipe(
                arguments=("-O", "-i", "sqm.in", "-o", "sqm.out"),
                inputs=(txt("sqm.in", sqm_input),),
                artifacts=("sqm.out", "stdout.log", "stderr.log"),
                normal_markers=("Calculation Completed", "Total SCF energy"),
                science_patterns=(r"(?i)(Total SCF energy|heat of formation).*[-+0-9.DEd]+",),
                science_descriptions=("SQM reaches AM1 SCF convergence and reports finite water energy/charges.",),
            ),
            ("gromacs", "gmx"): Recipe(
                arguments=("mdrun", "-deffnm", "production", "-nt", "1", "-nsteps", "10"),
                inputs=(
                    txt("start.gro", gromacs_gro),
                    txt("topol.top", gromacs_top),
                    txt("md.mdp", gromacs_mdp),
                ),
                setup_steps=(Step("gmx", ("grompp", "-f", "md.mdp", "-c", "start.gro", "-p", "topol.top", "-o", "production.tpr", "-maxwarn", "1"), "grompp"),),
                artifacts=("production.tpr", "production.log", "production.edr", "production.gro", "stdout.log"),
                normal_markers=("Finished mdrun", "Writing final coordinates"),
                science_patterns=(r"(?i)(Finished mdrun|Writing final coordinates)", r"(?m)^\s*10\s+[-+0-9.eE]+"),
                science_descriptions=("grompp builds a valid TPR and mdrun completes ten finite-energy argon steps.",),
            ),
            ("openmolcas", "pymolcas"): Recipe(
                arguments=("input.inp",),
                inputs=(txt("input.inp", openmolcas_input),),
                artifacts=("stdout.log", "input.ScfOrb", "input.scf.molden", "xmldump"),
                normal_markers=("Happy landing!",),
                science_patterns=(r"(?i)(total SCF energy|final energy).*[-+0-9.DEd]+",),
                science_descriptions=("OpenMolcas converges an H2 SCF calculation and reports finite energy.",),
                environment={"MOLCAS_WORKDIR": "{workdir}/scratch"},
                timeout_seconds=1200,
            ),
        }
    )
    return result


def _input_plan(item: Input) -> dict[str, Any]:
    record: dict[str, Any] = {
        "target": item.target,
        "kind": "tree" if item.tree else ("inline" if item.text is not None else "file"),
        "sensitive": item.sensitive,
    }
    if item.source:
        path = PROJECT_ROOT / item.source
        record.update(
            source=item.source,
            source_exists=path.is_dir() if item.tree else path.is_file(),
            includes=list(item.includes) if item.tree else None,
        )
        if item.append_text is not None:
            payload = item.append_text.encode("utf-8")
            record["append_text"] = {
                "size_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
    else:
        payload = (item.text or "").encode()
        record.update(
            size_bytes=len(payload),
            sha256=hashlib.sha256(payload).hexdigest(),
        )
    return record


def build_plans() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    guides = _load(GUIDES_PATH)["software"]
    examples = _load(EXAMPLES_PATH)["software"]
    manuals = _load(MANUALS_PATH)["software"]
    recipes = _recipes()
    if set(guides) != set(examples) or set(guides) != set(manuals):
        raise ValueError("native guide/manual/example software IDs differ")
    if len(guides) != EXPECTED_SOFTWARE:
        raise ValueError(f"expected {EXPECTED_SOFTWARE} software, found {len(guides)}")

    enabled: list[dict[str, Any]] = []
    disabled: list[dict[str, Any]] = []
    for software_id in sorted(guides):
        guide = guides[software_id]
        manual = manuals[software_id]
        runtime = _runtime(software_id, guide)
        for command, contract in examples[software_id]["commands"].items():
            command_guide = (guide.get("commands") or {}).get(command)
            if command_guide is None:
                raise ValueError(f"missing guide command: {software_id}/{command}")
            override = CONTRACT_OVERRIDES.get((software_id, command), {})
            common = {
                "case_id": f"{software_id}::{command}",
                "software_id": software_id,
                "command": command,
                "runtime": runtime,
                "environment": runtime_spec(runtime).get("environment"),
                "declared_version": manual.get("installed_version"),
                "license": _license(software_id),
                "guide_synopsis": command_guide.get("synopsis"),
                "contract_override": override.get("note"),
            }
            if not contract.get("enabled"):
                disabled.append(
                    {
                        **common,
                        "enabled": False,
                        "policy_status": "policy_validated"
                        if contract.get("example_kind") == "disabled"
                        else "policy_invalid",
                        "reason": "Standalone mpirun is disabled; pmemd.MPI owns the MPI scientific invocation.",
                    }
                )
                continue

            recipe = recipes.get((software_id, command))
            required = [str(value) for value in command_guide.get("required_files") or []]
            if recipe is None:
                recipe = Recipe(
                    blocked_reason=BLOCKED_REASONS.get((software_id, command))
                    or (
                        "No reviewed self-contained, license-compliant fixture is registered for "
                        + (", ".join(required) or "the command-specific scientific inputs")
                        + "; an interface probe is not a substitute."
                    )
                )
            inputs = [_input_plan(item) for item in recipe.inputs]
            missing = [item["source"] for item in inputs if item.get("source") and not item["source_exists"]]
            blocked = recipe.blocked_reason or (
                f"Registered validation sources are missing: {missing}" if missing else None
            )
            arguments = list(
                recipe.arguments
                if recipe.arguments is not None
                else tuple(str(value) for value in contract.get("arguments") or [])
            )
            input_names = list(override.get("inputs", contract.get("inputs") or []))
            output_names = list(override.get("outputs", contract.get("outputs") or []))
            stdin_target = override.get(
                "stdin_target",
                recipe.stdin_target if recipe.stdin_target is not None else contract.get("stdin_target"),
            )
            markers = list(recipe.normal_markers or tuple(manual.get("normal_markers") or []))
            enabled.append(
                {
                    **common,
                    "enabled": True,
                    "execution_command": recipe.execution_command or command,
                    "launcher": recipe.launcher,
                    "launcher_arguments": list(recipe.launcher_arguments),
                    "arguments": arguments,
                    "real_inputs": inputs,
                    "input_roles": input_names,
                    "stdin_target": stdin_target,
                    "expected_artifacts": list(recipe.artifacts or tuple(output_names)),
                    "normal_markers": markers,
                    "scientific_criteria": [
                        str(manual.get("convergence_notes") or ""),
                        *recipe.science_descriptions,
                    ],
                    "availability": "blocked" if blocked else "runnable",
                    "blocked_reason": blocked,
                    "timeout_seconds": recipe.timeout_seconds,
                    "recipe": recipe,
                }
            )

    if len(enabled) != EXPECTED_ENABLED:
        raise ValueError(f"expected {EXPECTED_ENABLED} enabled commands, found {len(enabled)}")
    if len(disabled) != EXPECTED_DISABLED:
        raise ValueError(f"expected {EXPECTED_DISABLED} disabled command, found {len(disabled)}")
    if disabled[0]["case_id"] != "amber_pmemd::mpirun":
        raise ValueError(f"unexpected disabled command: {disabled[0]['case_id']}")
    return enabled, disabled


def _public(plan: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in plan.items() if key != "recipe"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _copy_input(item: Input, workdir: Path) -> list[dict[str, Any]]:
    target = workdir.joinpath(*PurePosixPath(item.target).parts)
    if item.text is not None:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item.text, encoding="utf-8")
        return [
            {
                "target": item.target,
                "source": "inline",
                "size_bytes": target.stat().st_size,
                "sha256": _sha256(target),
            }
        ]

    source_path = PROJECT_ROOT / str(item.source)
    if item.tree:
        if not source_path.is_dir():
            raise FileNotFoundError(source_path)
        records = []
        for candidate in sorted(source_path.rglob("*")):
            if not candidate.is_file() or candidate.is_symlink():
                continue
            relative = candidate.relative_to(source_path).as_posix()
            if not any(fnmatch.fnmatch(relative, pattern) for pattern in item.includes):
                continue
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, destination)
            records.append(
                {
                    "target": destination.relative_to(workdir).as_posix(),
                    "source": candidate.relative_to(PROJECT_ROOT).as_posix(),
                    "size_bytes": destination.stat().st_size,
                    "sha256": None if item.sensitive else _sha256(destination),
                }
            )
        if not records:
            raise FileNotFoundError(
                f"no files matched {item.source} includes={item.includes}"
            )
        return records

    if not source_path.is_file() or source_path.is_symlink():
        raise FileNotFoundError(source_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target)
    if item.append_text is not None:
        with target.open("a", encoding="utf-8") as handle:
            handle.write(item.append_text)
    return [
        {
            "target": item.target,
            "source": item.source,
            "size_bytes": target.stat().st_size,
            "sha256": None if item.sensitive else _sha256(target),
        }
    ]


def _run(
    executable: str,
    arguments: tuple[str, ...] | list[str],
    *,
    workdir: Path,
    environment: dict[str, str],
    stdin_target: str | None,
    timeout_seconds: int,
    label: str,
) -> dict[str, Any]:
    stdin_handle = None
    if stdin_target:
        # Some Fortran programs rewind stdin. A pipe created by input= is not seekable.
        stdin_handle = (workdir / stdin_target).open("r", encoding="utf-8")
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [executable, *arguments],
            cwd=workdir,
            env=environment,
            stdin=stdin_handle,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
        result = {
            "returncode": completed.returncode,
            "timed_out": False,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired as exc:
        result = {
            "returncode": None,
            "timed_out": True,
            "stdout": exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
            "stderr": exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or ""),
        }
    finally:
        if stdin_handle is not None:
            stdin_handle.close()
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    (workdir / f"{label}.stdout.log").write_text(result["stdout"], encoding="utf-8")
    (workdir / f"{label}.stderr.log").write_text(result["stderr"], encoding="utf-8")
    return result


def _matching(workdir: Path, patterns: tuple[str, ...] | list[str]) -> list[Path]:
    paths: set[Path] = set()
    for pattern in patterns:
        for path in workdir.glob(pattern):
            if path.is_file() and not path.is_symlink():
                paths.add(path)
    return sorted(paths)


def _corpus(paths: list[Path]) -> str:
    values = []
    for path in paths:
        try:
            if path.stat().st_size > 8 * 1024 * 1024:
                continue
            payload = path.read_bytes()
            prefix = payload[:4096]
            if b"\x00" in prefix:
                # A few Fortran runtimes emit isolated NUL bytes in otherwise
                # textual logs. Keep those logs, but continue to reject real
                # binary artifacts such as NetCDF/HDF5 files.
                cleaned = prefix.replace(b"\x00", b"")
                printable = sum(
                    byte in (9, 10, 13) or 32 <= byte <= 126 for byte in cleaned
                )
                if (
                    not cleaned
                    or (len(cleaned) < 32 and len(cleaned) * 2 < len(prefix))
                    or printable / len(cleaned) < 0.9
                ):
                    continue
                payload = payload.replace(b"\x00", b"")
            values.append(payload.decode("utf-8", errors="replace"))
        except OSError:
            continue
    return "\n".join(values)


def _version_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        if re.search(r"(?i)\b(version|release|revision)\b", line):
            value = line.strip()
            if value and value not in lines:
                lines.append(value[:500])
        if len(lines) >= 10:
            break
    return lines


def _artifact_records(workdir: Path, paths: list[Path]) -> list[dict[str, Any]]:
    return [
        {
            "path": path.relative_to(workdir).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in paths
    ]


def _availability_probe(
    plan: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str] | None, str | None]:
    """Inspect runtime/executable dependencies without invoking the target command."""

    probe: dict[str, Any] = {
        "method": "resolve executable, inspect shebang or run ldd on ELF; target is not invoked",
        "runtime": plan["runtime"],
        "runtime_environment": plan.get("environment"),
    }
    try:
        additions = runtime_environment(plan["runtime"])
        environment = {**os.environ, **additions}
        probe["runtime_status"] = "available"
        probe["runtime_environment_keys"] = sorted(additions)
    except Exception as exc:  # runtime configuration errors are evidence, not runner crashes
        probe.update(
            runtime_status="unavailable",
            runtime_error=f"{type(exc).__name__}: {exc}",
            executable_status="not_probed",
            dependency_status="not_probed",
            overall_status="unavailable",
        )
        return probe, None, None

    try:
        executable = resolve_executable(plan["runtime"], plan["execution_command"])
    except Exception as exc:  # keep all 79 records even when one profile is broken
        probe.update(
            executable_status="unavailable",
            executable_error=f"{type(exc).__name__}: {exc}",
            dependency_status="not_probed",
            overall_status="unavailable",
        )
        return probe, environment, None
    if not executable:
        probe.update(
            executable_status="unavailable",
            dependency_status="not_probed",
            overall_status="unavailable",
        )
        return probe, environment, None

    path = Path(executable)
    try:
        resolved = path.resolve(strict=True)
        exists = resolved.is_file()
        executable_bit = os.access(resolved, os.X_OK)
    except OSError as exc:
        probe.update(
            resolved_executable=str(path),
            executable_status="unavailable",
            executable_error=f"{type(exc).__name__}: {exc}",
            dependency_status="not_probed",
            overall_status="unavailable",
        )
        return probe, environment, None
    probe.update(
        resolved_executable=str(resolved),
        executable_exists=exists,
        executable_bit=executable_bit,
        executable_status="available" if exists and executable_bit else "unavailable",
    )
    if not exists:
        probe.update(dependency_status="not_probed", overall_status="unavailable")
        return probe, environment, None

    try:
        prefix = resolved.read_bytes()[:4096]
    except OSError as exc:
        probe.update(
            file_kind="unreadable",
            dependency_status="not_probed",
            dependency_error=f"{type(exc).__name__}: {exc}",
            overall_status="unavailable",
        )
        return probe, environment, str(resolved)

    dependency_status = "unknown"
    if prefix.startswith(b"\x7fELF"):
        probe["file_kind"] = "ELF"
        ldd = shutil.which("ldd", path=environment.get("PATH"))
        if not ldd:
            probe.update(dependency_method="ldd", dependency_status="not_probed", dependency_error="ldd is unavailable")
            dependency_status = "not_probed"
        else:
            try:
                completed = subprocess.run(
                    [ldd, str(resolved)],
                    cwd=PROJECT_ROOT,
                    env=environment,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=30,
                    check=False,
                )
                evidence = (completed.stdout + completed.stderr).strip()
                missing = [
                    line.strip()
                    for line in evidence.splitlines()
                    if re.search(r"=>\s+not found\b", line)
                ]
                static_binary = bool(
                    re.search(r"(?i)(not a dynamic executable|statically linked)", evidence)
                )
                dependency_status = (
                    "available"
                    if not missing and (completed.returncode == 0 or static_binary)
                    else "unavailable"
                )
                probe.update(
                    dependency_method="ldd",
                    dependency_status=dependency_status,
                    dependency_returncode=completed.returncode,
                    missing_dynamic_libraries=missing,
                    dependency_evidence=evidence[:65536],
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                dependency_status = "not_probed"
                probe.update(
                    dependency_method="ldd",
                    dependency_status=dependency_status,
                    dependency_error=f"{type(exc).__name__}: {exc}",
                )
    elif prefix.startswith(b"#!"):
        probe["file_kind"] = "script"
        first_line = prefix.splitlines()[0].decode("utf-8", errors="replace")
        try:
            tokens = shlex.split(first_line[2:].strip())
        except ValueError:
            tokens = []
        interpreter: str | None = None
        if tokens:
            if Path(tokens[0]).name == "env":
                candidates = [token for token in tokens[1:] if not token.startswith("-")]
                if candidates:
                    interpreter = shutil.which(candidates[0], path=environment.get("PATH"))
            else:
                candidate = Path(tokens[0])
                interpreter = str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
        dependency_status = "available" if interpreter else "unavailable"
        probe.update(
            dependency_method="shebang",
            shebang=first_line,
            resolved_interpreter=interpreter,
            dependency_status=dependency_status,
        )
    else:
        probe.update(
            file_kind="other",
            dependency_method="file-header",
            dependency_status="not_applicable",
        )
        dependency_status = "not_applicable"

    probe["overall_status"] = (
        "available"
        if probe["executable_status"] == "available"
        and dependency_status in {"available", "not_applicable"}
        else "unavailable"
        if dependency_status == "unavailable" or probe["executable_status"] == "unavailable"
        else "partial"
    )
    return probe, environment, str(resolved)


def execute_plan(plan: dict[str, Any], work_root: Path) -> dict[str, Any]:
    recipe: Recipe = plan["recipe"]
    record = {
        **_public(plan),
        "started_at": _now(),
        "status": "blocked" if plan["blocked_reason"] else "running",
    }
    availability_probe, environment, executable = _availability_probe(plan)
    record["availability_probe"] = availability_probe
    if plan["blocked_reason"]:
        record["finished_at"] = _now()
        return record

    workdir = work_root / plan["software_id"] / plan["command"].replace("/", "_")
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    (workdir / "scratch").mkdir()
    record["work_directory"] = str(workdir)
    try:
        staged = []
        for item in recipe.inputs:
            staged.extend(_copy_input(item, workdir))
        record["staged_inputs"] = staged
    except (OSError, ValueError) as exc:
        record.update(
            status="blocked",
            blocked_reason=f"could not materialize real inputs: {exc}",
            finished_at=_now(),
        )
        return record

    if not executable:
        record.update(
            status="failed",
            failure_reason="configured executable did not resolve in the declared runtime",
            finished_at=_now(),
        )
        return record
    record["resolved_executable"] = executable
    if environment is None:
        record.update(
            status="failed",
            failure_reason="configured runtime environment could not be resolved",
            finished_at=_now(),
        )
        return record
    environment.update(
        {
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "TMPDIR": str(workdir / "scratch"),
        }
    )
    for key, value in recipe.environment.items():
        environment[key] = value.format(workdir=workdir)

    setup_records = []
    for index, step in enumerate(recipe.setup_steps):
        setup_executable = resolve_executable(plan["runtime"], step.executable)
        if not setup_executable:
            setup_records.append(
                {"label": step.label, "returncode": None, "reason": "executable unresolved"}
            )
            break
        outcome = _run(
            setup_executable,
            step.arguments,
            workdir=workdir,
            environment=environment,
            stdin_target=None,
            timeout_seconds=recipe.timeout_seconds,
            label=f"setup-{index}-{step.label}",
        )
        setup_records.append(
            {
                "label": step.label,
                "command": [setup_executable, *step.arguments],
                "returncode": outcome["returncode"],
                "timed_out": outcome["timed_out"],
                "elapsed_seconds": outcome["elapsed_seconds"],
            }
        )
        if outcome["returncode"] != 0 or outcome["timed_out"]:
            break
    record["setup_steps"] = setup_records
    if any(item.get("returncode") != 0 or item.get("timed_out") for item in setup_records):
        record.update(
            status="failed",
            failure_reason="a required scientific setup step failed",
            finished_at=_now(),
        )
        return record

    process_executable = executable
    process_arguments = list(plan["arguments"])
    if recipe.launcher:
        launcher_executable = resolve_executable(plan["runtime"], recipe.launcher)
        if not launcher_executable:
            record.update(
                status="failed",
                failure_reason=f"configured launcher did not resolve: {recipe.launcher}",
                finished_at=_now(),
            )
            return record
        process_executable = launcher_executable
        process_arguments = [
            *recipe.launcher_arguments,
            executable,
            *process_arguments,
        ]
        record["resolved_launcher"] = launcher_executable

    outcome = _run(
        process_executable,
        process_arguments,
        workdir=workdir,
        environment=environment,
        stdin_target=plan.get("stdin_target"),
        timeout_seconds=recipe.timeout_seconds,
        label="command",
    )
    shutil.copy2(workdir / "command.stdout.log", workdir / "stdout.log")
    shutil.copy2(workdir / "command.stderr.log", workdir / "stderr.log")
    record["process"] = {
        "command": [process_executable, *process_arguments],
        "returncode": outcome["returncode"],
        "timed_out": outcome["timed_out"],
        "elapsed_seconds": outcome["elapsed_seconds"],
    }

    patterns = tuple(dict.fromkeys((*recipe.artifacts, "stdout.log", "stderr.log")))
    artifacts = _matching(workdir, patterns)
    corpus = _corpus(artifacts)
    marker_hits = [
        marker for marker in plan["normal_markers"] if marker.casefold() in corpus.casefold()
    ]
    science_checks = []
    for index, pattern in enumerate(recipe.science_patterns):
        match = re.search(pattern, corpus, flags=re.I | re.M | re.S)
        science_checks.append(
            {
                "check_id": f"science_{index + 1}",
                "pattern": pattern,
                "status": "passed" if match else "failed",
                "evidence": match.group(0)[:500] if match else None,
            }
        )
    fatal_hits = [
        pattern for pattern in FATAL_PATTERNS if re.search(pattern, corpus, flags=re.I)
    ]
    missing_artifacts = [
        pattern for pattern in recipe.artifacts if not _matching(workdir, [pattern])
    ]
    record.update(
        normal_marker_status="passed" if marker_hits else "failed",
        normal_marker_hits=marker_hits,
        scientific_checks=science_checks,
        fatal_runtime_patterns=fatal_hits,
        missing_artifact_patterns=missing_artifacts,
        artifacts=_artifact_records(workdir, artifacts),
        observed_version_evidence=_version_lines(corpus),
    )
    passed = (
        outcome["returncode"] == 0
        and not outcome["timed_out"]
        and bool(marker_hits)
        and bool(science_checks)
        and all(check["status"] == "passed" for check in science_checks)
        and not fatal_hits
        and not missing_artifacts
    )
    record["status"] = "passed" if passed else "failed"
    if not passed:
        reasons = []
        if outcome["returncode"] != 0:
            reasons.append(f"return code {outcome['returncode']}")
        if outcome["timed_out"]:
            reasons.append("timeout")
        if not marker_hits:
            reasons.append("normal-termination marker absent")
        if not science_checks or any(check["status"] != "passed" for check in science_checks):
            reasons.append("task-specific scientific criterion failed")
        if fatal_hits:
            reasons.append(f"fatal runtime signature: {fatal_hits}")
        if missing_artifacts:
            reasons.append(f"missing artifacts: {missing_artifacts}")
        record["failure_reason"] = "; ".join(reasons)
    record["finished_at"] = _now()
    return record


def _select(raw: list[str] | None, plans: list[dict[str, Any]]) -> set[str]:
    known = {plan["software_id"] for plan in plans}
    if not raw:
        return known
    selected = {
        item.strip().lower().replace("-", "_")
        for value in raw
        for item in value.split(",")
        if item.strip()
    }
    unknown = selected - known
    if unknown:
        raise ValueError(f"unknown --software values: {sorted(unknown)}")
    return selected


def _counts(records: list[dict[str, Any]], disabled: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        status = str(record.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    counts["policy_validated"] = sum(
        item.get("policy_status") == "policy_validated" for item in disabled
    )
    return counts


def execute(
    plans: list[dict[str, Any]],
    disabled: list[dict[str, Any]],
    selected: set[str],
    output: Path,
    *,
    resume: bool,
) -> dict[str, Any]:
    selected_plans = [plan for plan in plans if plan["software_id"] in selected]
    selected_disabled = [item for item in disabled if item["software_id"] in selected]
    previous: dict[str, dict[str, Any]] = {}
    started_at = _now()
    if resume and output.is_file():
        old = json.loads(output.read_text(encoding="utf-8"))
        started_at = old.get("started_at") or started_at
        previous = {
            str(item["case_id"]): item
            for item in old.get("commands", [])
            if isinstance(item, dict) and item.get("case_id")
        }
    report: dict[str, Any] = {
        "schema_version": 1,
        "runner": "chemistry_toolbox/scripts/run_full_native_scientific_validation.py",
        "started_at": started_at,
        "updated_at": _now(),
        "scope": {
            "authoritative_software": EXPECTED_SOFTWARE,
            "authoritative_enabled_commands": EXPECTED_ENABLED,
            "authoritative_disabled_commands": EXPECTED_DISABLED,
            "selected_software": sorted(selected),
            "selected_enabled_commands": len(selected_plans),
            "pass_policy": (
                "Exit zero, real normal termination, every declared artifact, no fatal runtime "
                "signature, and all task-specific criteria are mandatory. Help/version/missing-input "
                "probes never pass."
            ),
        },
        "contract_overrides": [
            {"software_id": key[0], "command": key[1], **value}
            for key, value in sorted(CONTRACT_OVERRIDES.items())
        ],
        "commands": [],
        "disabled_commands": selected_disabled,
        "counts": {},
    }
    work_root = output.parent / f"{output.stem}_artifacts"
    work_root.mkdir(parents=True, exist_ok=True)
    records = []
    for plan in selected_plans:
        old_record = previous.get(plan["case_id"])
        record = (
            old_record
            if old_record and old_record.get("status") == "passed"
            else execute_plan(plan, work_root)
        )
        records.append(record)
        report["commands"] = records
        report["counts"] = _counts(records, selected_disabled)
        report["updated_at"] = _now()
        _atomic_json(output, report)
    report["finished_at"] = _now()
    report["counts"] = _counts(records, selected_disabled)
    _atomic_json(output, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List plans without executing software.")
    parser.add_argument(
        "--software",
        action="append",
        metavar="ID[,ID...]",
        help="Select software IDs; repeat or use comma-separated values.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse passed records and rerun failed or blocked records from --output.",
    )
    args = parser.parse_args(argv)

    plans, disabled = build_plans()
    selected = _select(args.software, plans)
    if args.list:
        selected_plans = [plan for plan in plans if plan["software_id"] in selected]
        payload = {
            "schema_version": 1,
            "counts": {
                "software": len({plan["software_id"] for plan in plans}),
                "enabled_commands": len(plans),
                "disabled_commands": len(disabled),
                "selected_software": len(selected),
                "selected_enabled_commands": len(selected_plans),
                "runnable": sum(plan["availability"] == "runnable" for plan in selected_plans),
                "blocked": sum(plan["availability"] == "blocked" for plan in selected_plans),
            },
            "commands": [_public(plan) for plan in selected_plans],
            "disabled_commands": [
                item for item in disabled if item["software_id"] in selected
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    report = execute(
        plans,
        disabled,
        selected,
        args.output.expanduser().resolve(),
        resume=args.resume,
    )
    print(json.dumps({"output": str(args.output), "counts": report["counts"]}, indent=2))
    if report["counts"].get("failed"):
        return 1
    if report["counts"].get("blocked"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
