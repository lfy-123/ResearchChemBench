#!/usr/bin/env python3
"""Build dual-track Electron Isodensity Surface benchmark tasks.

The open-discovery track exposes only scientific questions and raw molecular /
experimental inputs.  The guided-reproduction track adds the paper's public
conformer coordinates, method hierarchy, and execution route.  Neither track
exposes author wavefunctions, quantum-chemistry outputs, computed surface
matrices, the optimal cutoff, or reference answers.

The source archive supplied during curation is used only to bootstrap a small,
versioned shared reference area.  Generated task data are ordinary files: no
ZIP files, symlinks, or archive-extraction instructions are placed in an
agent-visible task directory.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = PROJECT_ROOT / "tasks"
SOURCE_ARCHIVE = TASKS_ROOT / "ResearchChemBench_Paper_Datasets.zip"
SHARED_ROOT = TASKS_ROOT / "_electron_isodensity_shared"
REFERENCE_ROOT = SHARED_ROOT / "reference"

ARCHIVE_REPRO_ROOT = (
    "ResearchChemBench_Paper_Datasets/02_Guided_Paper_Reproduction_Benchmark/"
    "Electron_Isodensity_Surface_Reproduction"
)
ARCHIVE_AGENT_ROOT = f"{ARCHIVE_REPRO_ROOT}/01_agent_tasks_and_data"
ARCHIVE_HIDDEN_ROOT = f"{ARCHIVE_REPRO_ROOT}/02_hidden_reference_answers"

DOI = "10.1038/s41467-024-50408-8"


MOLECULES: dict[str, dict[str, Any]] = {
    "ISO-M1": {
        "name": "ethane",
        "smiles": "CC",
        "formula": "C2H6",
        "atom_count": 8,
        "charge": 0,
        "multiplicity": 1,
        "source_prefix": "995",
        "published_conformer_count": 1,
        "te_surface_angstrom2": 75.0867,
        "paper_iso_surface_0_0016_angstrom2": 75.61296,
    },
    "ISO-M2": {
        "name": "furan",
        "smiles": "c1cocc1",
        "formula": "C4H4O",
        "atom_count": 9,
        "charge": 0,
        "multiplicity": 1,
        "source_prefix": "1081",
        "published_conformer_count": 1,
        "te_surface_angstrom2": 97.7096,
        "paper_iso_surface_0_0016_angstrom2": 95.76939,
    },
    "ISO-M3": {
        "name": "pyridine",
        "smiles": "n1ccccc1",
        "formula": "C5H5N",
        "atom_count": 11,
        "charge": 0,
        "multiplicity": 1,
        "source_prefix": "1679",
        "published_conformer_count": 1,
        "te_surface_angstrom2": 113.206,
        "paper_iso_surface_0_0016_angstrom2": 110.9705,
    },
    "ISO-M4": {
        "name": "tetrahydrofuran",
        "smiles": "C1CCOC1",
        "formula": "C4H8O",
        "atom_count": 13,
        "charge": 0,
        "multiplicity": 1,
        "source_prefix": "1765",
        "published_conformer_count": 1,
        "te_surface_angstrom2": 110.538,
        "paper_iso_surface_0_0016_angstrom2": 109.9966,
    },
    "ISO-M5": {
        "name": "1,4-dioxane",
        "smiles": "O1CCOCC1",
        "formula": "C4H8O2",
        "atom_count": 14,
        "charge": 0,
        "multiplicity": 1,
        "source_prefix": "142",
        "published_conformer_count": 3,
        "te_surface_angstrom2": 118.956,
        "paper_iso_surface_0_0016_angstrom2": 117.1575,
    },
    "ISO-M6": {
        "name": "1-pentanethiol",
        "smiles": "CCCCCS",
        "formula": "C5H12S",
        "atom_count": 18,
        "charge": 0,
        "multiplicity": 1,
        "source_prefix": "1475",
        "published_conformer_count": 25,
        "te_surface_angstrom2": 156.507,
        "paper_iso_surface_0_0016_angstrom2": 157.1994,
    },
    "ISO-M7": {
        "name": "cyclohexanone",
        "smiles": "O=C1CCCCC1",
        "formula": "C6H10O",
        "atom_count": 17,
        "charge": 0,
        "multiplicity": 1,
        "source_prefix": "805",
        "published_conformer_count": 3,
        "te_surface_angstrom2": 143.248,
        "paper_iso_surface_0_0016_angstrom2": 136.6333,
    },
}

PAPER_CUTOFF_MUPE = {
    "0.0008": 10.40862824831,
    "0.0009": 8.59042749507472,
    "0.0010": 6.983977915614389,
    "0.0011": 5.547764622689169,
    "0.0012": 4.313527166731575,
    "0.0013": 3.2656707175422146,
    "0.0014": 2.4291555602334407,
    "0.0015": 1.8430780321134992,
    "0.0016": 1.5922920870480508,
    "0.0017": 1.7123077185580835,
    "0.0018": 2.1015745078180954,
    "0.0019": 2.6093848553808394,
    "0.0020": 3.1672347890461414,
    "0.0021": 3.7864502111219207,
    "0.0022": 4.394986623871028,
    "0.0023": 4.987117230524248,
    "0.0024": 5.561497411438547,
    "0.0025": 6.1088686723640855,
}


@dataclass(frozen=True)
class TaskSpec:
    number: str
    suffix: str
    title: str
    molecule_ids: tuple[str, ...]
    visible_te_ids: tuple[str, ...]
    open_task: str
    reproduction_task: str
    open_requirements: tuple[str, ...]
    reproduction_requirements: tuple[str, ...]
    deliverables: tuple[tuple[str, str, bool], ...]
    reference_key: str

    @property
    def open_id(self) -> str:
        return f"Electron_Isodensity_{self.number}_{self.suffix}"

    @property
    def reproduction_id(self) -> str:
        return f"Electron_Isodensity_Reproduction_{self.number}_{self.suffix}"


COMMON_DELIVERABLES = (
    (
        "report/research_plan.json",
        "Initial hypotheses, resource tiers, validation gates, stopping criteria, and revisions.",
        False,
    ),
    (
        "report/tool_trace.jsonl",
        "One provenance record per real chemistry-software invocation.",
        False,
    ),
    (
        "report/failure_log.jsonl",
        "Failed or inconclusive branches and their scientific consequence.",
        True,
    ),
    (
        "report/report.md",
        "Artifact-linked scientific report separating computed results, experiment, inference, and uncertainty.",
        False,
    ),
)

TASK_SPECS = (
    TaskSpec(
        number="01",
        suffix="Method_Selection",
        title="Electronic-density method selection",
        molecule_ids=("ISO-M1", "ISO-M2", "ISO-M3"),
        visible_te_ids=(),
        open_task=(
            "Starting only from the supplied neutral molecular identities, independently determine which "
            "affordable electronic-structure approach gives electron-density isosurface areas closest to "
            "a higher-level reference on the same geometries. Generate all three-dimensional structures, "
            "choose a defensible hierarchy of candidate and reference calculations, evaluate multiple "
            "density cutoffs, and justify the production method from newly computed evidence. Do not "
            "identify or search for the source publication or use published surface values."
        ),
        reproduction_task=(
            "Using the supplied paper method hierarchy and public conformer coordinates for ISO-M1 to "
            "ISO-M3, reproduce the comparison of PBE, B3LYP, and DSD-PBEP86 electron-density surfaces "
            "against feasible CCSD(T) references at def2-TZVPD. Recompute every wavefunction and surface "
            "in this run and report whether the paper's production-method selection is recovered."
        ),
        open_requirements=(
            "Compare at least three meaningfully different affordable electronic-structure approximations on common structures and basis-quality conditions.",
            "Create a higher-level reference for at least the smallest molecule, or provide calculation-backed bounds when that reference is unaffordable.",
            "Evaluate more than one density cutoff and keep wavefunction-to-surface provenance for every numerical comparison.",
        ),
        reproduction_requirements=(
            "Use the supplied def2-TZVPD method-comparison hierarchy consistently across ISO-M1 to ISO-M3.",
            "Run the complete supplied cutoff grid for each successful method and molecule.",
            "Keep current-software recomputations separate from hidden paper-published numerical targets.",
        ),
        deliverables=COMMON_DELIVERABLES
        + (
            ("report/quantum_calculations.csv", "Method, basis, convergence, energy, and wavefunction artifact inventory.", False),
            ("report/surface_matrix.csv", "Molecule by method by cutoff recomputed surface areas.", False),
            ("report/method_comparison.json", "Reference-relative errors, selected production method, and uncertainty.", False),
        ),
        reference_key="method_selection",
    ),
    TaskSpec(
        number="02",
        suffix="Conformer_Effects",
        title="Conformer sampling effects",
        molecule_ids=("ISO-M5", "ISO-M6"),
        visible_te_ids=("ISO-M5", "ISO-M6"),
        open_task=(
            "Using the supplied molecular identities and experimental TE surface areas, independently test "
            "whether conformer sampling materially changes the theoretical electron-density surface of "
            "1,4-dioxane and 1-pentanethiol. Generate, screen, deduplicate, refine, and weight conformers "
            "with a resource-aware workflow of your own design. Compare the lowest-energy conformer with "
            "the final ensemble using newly generated quantum and isosurface artifacts."
        ),
        reproduction_task=(
            "Using the supplied public paper conformers and production electronic-density protocol, "
            "reproduce the single-conformer versus Boltzmann-ensemble surface comparison for 1,4-dioxane "
            "and 1-pentanethiol. Do not rerun conformer discovery unless validating the published set; "
            "recompute all energies, wavefunctions, cutoff surfaces, and weights in this run."
        ),
        open_requirements=(
            "Perform an actual conformer search from the supplied molecular identities rather than assuming one input geometry is representative.",
            "Record the candidate count, energy window, deduplication rule, exclusions, and normalized statistical weights.",
            "Compare single-conformer and ensemble predictions against the supplied experimental TE surfaces.",
        ),
        reproduction_requirements=(
            "Validate all supplied public conformer files before calculation and report any connectivity changes or failures.",
            "Apply the supplied production electron-density and cutoff protocol to every retained conformer.",
            "Use one documented, internally consistent energy convention for Boltzmann weights and identify the paper ambiguity in the weighting energy if it affects the result.",
        ),
        deliverables=COMMON_DELIVERABLES
        + (
            ("report/conformer_inventory.csv", "All generated or supplied conformers, validation, deduplication, and status.", False),
            ("report/conformer_weights.csv", "Energy convention and normalized statistical weights.", False),
            ("report/surface_by_conformer.csv", "Conformer and cutoff resolved surface areas.", False),
            ("report/ensemble_comparison.json", "Single-conformer versus ensemble results and experimental errors.", False),
        ),
        reference_key="conformer_effects",
    ),
    TaskSpec(
        number="03",
        suffix="Cutoff_Calibration",
        title="Electron-density cutoff calibration",
        molecule_ids=("ISO-M1", "ISO-M2", "ISO-M3", "ISO-M5", "ISO-M6", "ISO-M7"),
        visible_te_ids=("ISO-M1", "ISO-M2", "ISO-M3", "ISO-M5", "ISO-M6", "ISO-M7"),
        open_task=(
            "Using the supplied calibration molecules and experimental TE surface areas, independently "
            "determine which electron-density cutoff best represents molecular surface area. Design and "
            "execute the electronic-structure, conformer, isosurface, and statistical workflow yourself; "
            "sample the cutoff domain densely enough to locate and support an optimum rather than testing "
            "a single assumed value. Report subset limitations instead of importing a literature answer."
        ),
        reproduction_task=(
            "Using the supplied paper conformers, DSD-PBEP86/def2-QZVPD density protocol, and complete "
            "0.0008 to 0.0025 a.u. cutoff grid, reproduce the cutoff-calibration analysis for the supplied "
            "six-molecule benchmark subset. Recompute conformer surfaces and weights, calculate MUPE and "
            "Pearson R at every cutoff, and compare the subset optimum with the hidden paper-level result."
        ),
        open_requirements=(
            "Use all supplied calibration measurements unless a molecule is excluded with calculation-backed justification.",
            "Evaluate a multi-point cutoff curve and report the objective function, nearby alternatives, outliers, and uncertainty.",
            "For flexible molecules, use an ensemble or quantify the bias caused by a reduced conformer treatment.",
        ),
        reproduction_requirements=(
            "Use the supplied paper conformers and production density method for the main profile.",
            "Compute every cutoff from 0.0008 through 0.0025 a.u. at 0.0001 a.u. intervals.",
            "Report the supplied-subset optimum separately from the hidden 104-molecule paper result.",
        ),
        deliverables=COMMON_DELIVERABLES
        + (
            ("report/conformer_weights.csv", "Energy convention and normalized weights for flexible molecules.", False),
            ("report/surface_by_molecule_and_cutoff.csv", "Conformer-averaged surface matrix for all calibration molecules.", False),
            ("report/cutoff_metrics.csv", "MUPE, Pearson R, and diagnostics for every tested cutoff.", False),
            ("report/cutoff_selection.json", "Selected cutoff, neighbor comparison, outliers, and uncertainty.", False),
        ),
        reference_key="cutoff_calibration",
    ),
    TaskSpec(
        number="04",
        suffix="Blind_Prediction",
        title="Held-out tetrahydrofuran prediction",
        molecule_ids=("ISO-M1", "ISO-M2", "ISO-M3", "ISO-M4"),
        visible_te_ids=("ISO-M1", "ISO-M2", "ISO-M3"),
        open_task=(
            "Calibrate an electron-density surface workflow using the three supplied molecules with known "
            "experimental TE areas, lock all choices before inspecting the held-out system, and predict "
            "the molecular surface area of tetrahydrofuran from its supplied identity. The tetrahydrofuran "
            "experimental value is intentionally hidden. Generate all structural, quantum, isosurface, and "
            "uncertainty evidence in this run without searching for the source publication."
        ),
        reproduction_task=(
            "Follow the supplied paper route on the public conformers for ISO-M1 to ISO-M4: use the three "
            "calibration molecules to select the cutoff from recomputed surfaces, lock it, then reproduce "
            "the held-out tetrahydrofuran surface prediction. The experimental and paper-computed ISO-M4 "
            "values remain hidden until scoring."
        ),
        open_requirements=(
            "Record the calibration procedure and lock the selected method and cutoff before calculating the held-out prediction.",
            "Generate a tetrahydrofuran conformer treatment appropriate to its flexibility and quantify its contribution to uncertainty.",
            "Do not infer or search for the hidden tetrahydrofuran TE surface.",
        ),
        reproduction_requirements=(
            "Use the supplied public conformers and paper method hierarchy for the main calculation.",
            "Select the cutoff only from newly recomputed ISO-M1 to ISO-M3 calibration evidence.",
            "Report the blind ISO-M4 value before any hidden-target comparison.",
        ),
        deliverables=COMMON_DELIVERABLES
        + (
            ("report/calibration_evidence.csv", "Calibration surfaces, metrics, and locked choices.", False),
            ("report/blind_prediction.json", "Held-out surface prediction and uncertainty decomposition.", False),
        ),
        reference_key="blind_prediction",
    ),
    TaskSpec(
        number="05",
        suffix="End_to_End",
        title="End-to-end molecular-surface investigation",
        molecule_ids=("ISO-M1", "ISO-M2", "ISO-M3", "ISO-M4", "ISO-M5", "ISO-M6", "ISO-M7"),
        visible_te_ids=("ISO-M1", "ISO-M2", "ISO-M3", "ISO-M5", "ISO-M6", "ISO-M7"),
        open_task=(
            "Starting only from the supplied seven molecular identities and six experimental TE surface "
            "areas, independently design and execute an end-to-end study of electron-density molecular "
            "surfaces. Establish a credible electronic-density method, determine whether conformer sampling "
            "is necessary, calibrate a density cutoff, and make a locked blind prediction for tetrahydrofuran. "
            "No software, method, basis set, conformer route, cutoff grid, or stopping path is prescribed."
        ),
        reproduction_task=(
            "Use the supplied public conformers and paper-reconstructed ORCA-to-Multiwfn route to reproduce "
            "the paper's method comparison, conformer-ensemble analysis, cutoff calibration, and held-out "
            "tetrahydrofuran prediction on the seven-molecule benchmark subset. Generate every energy, "
            "wavefunction, surface, weight, and statistical result anew."
        ),
        open_requirements=(
            "Write a resource-tiered plan with explicit validation gates and revise it when calculations fail or evidence changes.",
            "Use real structure generation, conformer sampling, quantum chemistry, electron-density surface analysis, and statistical calibration.",
            "Keep the ISO-M4 target hidden until the workflow and cutoff are locked.",
            "Separate experimental inputs, computed artifacts, inference, uncertainty, and unresolved limitations.",
        ),
        reproduction_requirements=(
            "Apply the supplied method hierarchy and public conformers consistently across the seven-molecule subset.",
            "Run the full supplied cutoff grid and reconstruct conformer-weighted surfaces from new calculations.",
            "Keep subset-level reproduction results separate from paper-level 104-molecule targets.",
            "Record version-compatible changes to the paper's ORCA 5.0.3 and Multiwfn command streams.",
        ),
        deliverables=COMMON_DELIVERABLES
        + (
            ("report/environment_report.json", "Software, versions, executables, resources, and compatibility substitutions.", False),
            ("report/conformer_inventory.csv", "All conformers and validation outcomes.", False),
            ("report/quantum_calculations.csv", "All electronic-structure calculations and wavefunction artifacts.", False),
            ("report/surface_by_conformer_and_cutoff.csv", "Complete conformer and cutoff resolved surface matrix.", False),
            ("report/conformer_weights.csv", "Consistent energies and normalized ensemble weights.", False),
            ("report/cutoff_metrics.csv", "Cutoff-dependent calibration statistics.", False),
            ("report/final_answer.json", "Machine-readable method, cutoff, ensemble conclusions, blind prediction, and confidence.", False),
        ),
        reference_key="end_to_end",
    ),
)


COMPUTATIONAL_PROTOCOL: dict[str, Any] = {
    "schema_version": 1,
    "protocol_type": "paper_reconstructed_guided_reproduction",
    "paper_doi": DOI,
    "result_values_included": False,
    "author_wavefunctions_included": False,
    "author_quantum_outputs_included": False,
    "conformer_source": {
        "paper_method": "CREST with GFN2-xTB",
        "paper_limit": "up to 25 low-energy conformers per molecule",
        "task_policy": "Use the supplied public Supplementary Data 2 XYZ conformers; rerunning CREST is not required for the main reproduction profile.",
    },
    "method_comparison": {
        "software": "ORCA 5.0.3 or a documented compatible newer ORCA version",
        "methods": ["PBE", "B3LYP", "DSD-PBEP86", "CCSD(T)"],
        "basis": "def2-TZVPD",
        "comparison_rule": "Compare DFT surface areas against feasible CCSD(T) surface areas on the same geometry and cutoff grid.",
        "resource_policy": "CCSD(T) may be restricted to the smallest molecule when a larger reference is unaffordable, but the missing comparison must be explicit.",
        "correlated_density_compatibility": {
            "paper_label": "CCSD(T)",
            "orca_6_limitation": "ORCA 6.1 does not provide an unrelaxed CCSD(T) one-particle density because the perturbative triples correction has no supported density. It does provide an unrelaxed CCSD density from the same coupled-cluster module.",
            "reproduction_policy": "Use a canonical CCSD unrelaxed density at def2-TZVPD as the reproducible correlated-density reference, optionally report the matching CCSD(T) energy separately, and label this substitution explicitly rather than claiming an exact CCSD(T) density.",
            "density_export": "Export the MDCI density with orca_plot to a density grid or another format accepted by the surface analyzer; orca_2aim on the ordinary GBW would export reference orbitals rather than the MDCI density.",
            "compatible_template": "author_input_templates/ccsd_density_orca_6.in",
            "orca_plot_menu_template": "author_input_templates/orca_plot_ccsd_density.menu",
            "multiwfn_grid_menu_template": "author_input_templates/Multiwfn_2026_external_grid_surface.menu",
        },
    },
    "production_density": {
        "software": "ORCA 5.0.3 or compatible version",
        "method": "DSD-PBEP86",
        "orbital_basis": "def2-QZVPD",
        "auxiliary_basis": "def2-TZVPD/C",
        "dispersion": "D3BJ",
        "frozen_core": False,
        "density": "relaxed MP2/double-hybrid density",
        "scf": "VeryTightSCF with stability checking",
        "paper_template": "author_input_templates/orca_input.in",
        "compatible_template": "author_input_templates/orca_6_compatible.in",
        "paper_template_note": "The verbatim Supplementary Software snippet ends with an incomplete '*xyzfile molecule.xyz' placeholder and does not explicitly request MP2 natural orbitals. A runnable ORCA input must add charge and multiplicity. The compatible template also requests NatOrbs so orca_2aim exports the relaxed double-hybrid density rather than silently falling back to the reference-orbital GBW.",
        "required_outputs": ["ORCA text output", "GBW", "WFN or WFX readable by Multiwfn"],
    },
    "surface_analysis": {
        "software": "Multiwfn using the improved marching tetrahedra molecular-surface implementation",
        "density_cutoff_start_au": 0.0008,
        "density_cutoff_stop_au": 0.0025,
        "density_cutoff_step_au": 0.0001,
        "paper_grid_spacing": 0.1,
        "surface_area_unit": "angstrom^2",
        "paper_template": "author_input_templates/Multiwfn.in",
        "compatible_menu_template": "author_input_templates/Multiwfn_2026_surface_area.menu",
        "version_note": "The author command stream is retained verbatim as provenance. Multiwfn menu numbering changed in the installed 2026.7.15 version, so use a tested version-compatible menu stream while preserving cutoff and grid settings.",
    },
    "ensemble": {
        "temperature_kelvin": 298.15,
        "aggregation": "Boltzmann-weighted surface area over retained conformers",
        "consistency_requirement": "Use one documented energy convention and unit for all conformers of a molecule, normalize weights to one, and do not mix electronic and free energies silently.",
        "paper_ambiguity": "The accessible paper and public templates do not uniquely specify a separate thermochemistry calculation for conformer weights. Report the chosen paper-compatible energy convention and sensitivity instead of inventing unavailable details.",
    },
    "statistics": {
        "mupe_formula": "mean(abs((TE - isodensity) / TE)) * 100",
        "correlation": "Pearson R across molecules",
        "blind_policy": "Choose and lock the cutoff using calibration molecules before evaluating ISO-M4.",
    },
    "version_policy": {
        "exact_numeric_identity_required": False,
        "required": "real recomputation, preserved scientific settings, provenance, convergence checks, and an explicit explanation of version-dependent deviations",
    },
}

ORCA_6_COMPATIBLE_TEMPLATE = """! DSD-PBEP86 def2-QZVPD def2-TZVPD/C D3BJ NoFrozenCore PModel VeryTightSCF PAL16
%maxcore 1500
%mp2
  Density relaxed
  NatOrbs true
end
%scf
  GuessMode CMatrix
  STABPerform true
  STABRestartUHFifUnstable true
end
* xyzfile 0 1 molecule.xyz
"""

MULTIWFN_2026_SURFACE_MENU = """12
1
1
<DENSITY_CUTOFF_AU>
3
0.1
6
-1
-1
q
"""

ORCA_PLOT_CCSD_DENSITY_MENU = """1
7
y
4
100 100 100
11
12
"""

MULTIWFN_2026_EXTERNAL_GRID_SURFACE_MENU = """12
1
11
<DENSITY_CUTOFF_AU>
3
0.1
6
-1
-1
q
"""

CCSD_DENSITY_ORCA_6_TEMPLATE = """! CCSD def2-TZVPD NoFrozenCore VeryTightSCF PAL16
%maxcore 1500
%mdci
  Density unrelaxed
end
* xyzfile 0 1 molecule.xyz
"""


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n").encode()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_replace_directory(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    os.replace(source, destination)


def _archive_bytes(archive: zipfile.ZipFile, member: str) -> bytes:
    try:
        return archive.read(member)
    except KeyError as exc:
        raise RuntimeError(f"Required source member is missing: {member}") from exc


def _bootstrap_shared_reference() -> None:
    required = [
        REFERENCE_ROOT / "paper.pdf",
        REFERENCE_ROOT / "published_conformers" / "ISO-M1" / "995-1.xyz",
        REFERENCE_ROOT / "author_input_templates" / "orca_input.in",
    ]
    if all(path.is_file() for path in required):
        return
    if not SOURCE_ARCHIVE.is_file():
        raise RuntimeError(
            "Shared reference is incomplete and the bootstrap archive is unavailable: "
            f"{SOURCE_ARCHIVE}"
        )

    REFERENCE_ROOT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(SOURCE_ARCHIVE) as archive:
        binary_sources = {
            "paper.pdf": f"{ARCHIVE_HIDDEN_ROOT}/paper/Electron_iso_density_surfaces.pdf",
            "fulltext.xml": f"{ARCHIVE_HIDDEN_ROOT}/sources/PMC11271626_fullTextXML.xml",
            "supplementary/Supplementary_Information.docx": f"{ARCHIVE_HIDDEN_ROOT}/sources/extracted_supplementary/41467_2024_50408_MOESM1_ESM.docx",
            "supplementary/Supplementary_Data_1.xlsx": f"{ARCHIVE_HIDDEN_ROOT}/sources/extracted_supplementary/41467_2024_50408_MOESM4_ESM.xlsx",
            "supplementary/Supplementary_Data_2.zip": f"{ARCHIVE_HIDDEN_ROOT}/sources/extracted_supplementary/41467_2024_50408_MOESM5_ESM.zip",
            "supplementary/Supplementary_Software.zip": f"{ARCHIVE_HIDDEN_ROOT}/sources/extracted_supplementary/41467_2024_50408_MOESM6_ESM.zip",
            "supplementary/Source_Data.xlsx": f"{ARCHIVE_HIDDEN_ROOT}/sources/extracted_supplementary/41467_2024_50408_MOESM8_ESM.xlsx",
            "author_input_templates/orca_input.in": f"{ARCHIVE_HIDDEN_ROOT}/sources/supplementary_software/orca_input.in",
            "author_input_templates/Multiwfn.in": f"{ARCHIVE_HIDDEN_ROOT}/sources/supplementary_software/Multiwfn.in",
            "author_input_templates/analyze_surf.m": f"{ARCHIVE_HIDDEN_ROOT}/sources/supplementary_software/analyze_surf.m",
        }
        for relative, member in binary_sources.items():
            destination = REFERENCE_ROOT / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(_archive_bytes(archive, member))

        for molecule_id, molecule in MOLECULES.items():
            count = molecule["published_conformer_count"]
            prefix = molecule["source_prefix"]
            for index in range(1, count + 1):
                filename = f"{prefix}-{index}.xyz"
                member = (
                    f"{ARCHIVE_AGENT_ROOT}/task_inputs/published_conformer_seeds/"
                    f"{molecule_id}/{filename}"
                )
                destination = REFERENCE_ROOT / "published_conformers" / molecule_id / filename
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(_archive_bytes(archive, member))

    source_manifest = {
        "schema_version": 1,
        "paper": {
            "title": "Electron iso-density surfaces provide a thermodynamically consistent representation of atomic and molecular surfaces",
            "authors": ["Amin Alibakhshi", "Lars V. Schaefer"],
            "journal": "Nature Communications",
            "year": 2024,
            "doi": DOI,
            "official_url": f"https://doi.org/{DOI}",
            "pmcid": "PMC11271626",
            "pmc_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11271626/",
            "license": "CC BY 4.0",
        },
        "official_resources": [
            {"name": "Supplementary Information", "local_path": "supplementary/Supplementary_Information.docx"},
            {"name": "Supplementary Data 1", "local_path": "supplementary/Supplementary_Data_1.xlsx"},
            {"name": "Supplementary Data 2", "local_path": "supplementary/Supplementary_Data_2.zip"},
            {"name": "Supplementary Software", "local_path": "supplementary/Supplementary_Software.zip"},
            {"name": "Source Data", "local_path": "supplementary/Source_Data.xlsx"},
        ],
        "online_search_audit": {
            "checked": ["Nature article and data/code availability sections", "PubMed Central article package", "DOI and general web search for separate repositories"],
            "separate_public_repository_found": False,
            "missing_public_resource_detected": False,
            "note": "The official article points to article supplements and source data; no separate author repository was identified.",
        },
        "dataset_count_discrepancy": {
            "paper_reported_conformers": 1071,
            "supplementary_data_2_xyz_files": 1074,
            "unique_molecule_prefixes": 104,
            "policy": "Retain the discrepancy in provenance; do not silently rewrite either count.",
        },
    }
    for item in source_manifest["official_resources"]:
        path = REFERENCE_ROOT / item["local_path"]
        item["size_bytes"] = path.stat().st_size
        item["sha256"] = _sha256(path)
    source_manifest["paper"]["local_path"] = "paper.pdf"
    source_manifest["paper"]["sha256"] = _sha256(REFERENCE_ROOT / "paper.pdf")
    _write_json(REFERENCE_ROOT / "source_manifest.json", source_manifest)

    _write_text(
        REFERENCE_ROOT / "CURATION_AUDIT.md",
        """# Electron Isodensity source curation audit

The official Nature Communications article, PubMed Central package, article
supplements, source data, and general web results were checked.  The public
record contains Supplementary Information, Supplementary Data 1, the complete
Supplementary Data 2 coordinate archive, Supplementary Software, and Source
Data.  No separate author GitHub or data repository was identified.

The paper reports 1071 conformers for 104 molecules, whereas the public
Supplementary Data 2 archive contains 1074 XYZ files with 104 unique molecule
prefixes.  This discrepancy is retained as provenance.  The benchmark uses
only seven named molecules and copies only task-relevant conformers into each
guided-reproduction task.

Agent-visible task data never include the paper PDF, Supplementary Data 1,
Source Data, author-computed surface areas, wavefunctions, ORCA outputs, or the
paper's optimal cutoff.  Public conformer coordinates are exposed only in the
guided-reproduction track.
""",
    )

    paper_reference = {
        "paper_level": {
            "optimal_density_cutoff_au": 0.0016,
            "ensemble_mupe_percent": 1.5922920870480508,
            "ensemble_pearson_r": 0.995,
            "single_lowest_conformer_mupe_percent": 1.87,
            "method_validation_mupe_percent": {"PBE": 0.24, "B3LYP": 0.36, "DSD-PBEP86": 0.08},
            "cutoff_mupe_curve_percent": PAPER_CUTOFF_MUPE,
        },
        "molecules": {
            molecule_id: {
                key: value
                for key, value in molecule.items()
                if key
                in {
                    "name",
                    "source_prefix",
                    "published_conformer_count",
                    "te_surface_angstrom2",
                    "paper_iso_surface_0_0016_angstrom2",
                }
            }
            for molecule_id, molecule in MOLECULES.items()
        },
        "conformer_example": {
            "molecule_id": "ISO-M6",
            "individual_surface_areas_angstrom2": [159.8, 149.2],
            "paper_ensemble_surface_angstrom2": 157.1994,
        },
    }
    _write_json(REFERENCE_ROOT / "paper_reference.json", paper_reference)


def _molecular_systems(spec: TaskSpec) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "systems": {
            molecule_id: {
                "name": MOLECULES[molecule_id]["name"],
                "smiles": MOLECULES[molecule_id]["smiles"],
                "formula": MOLECULES[molecule_id]["formula"],
                "atom_count": MOLECULES[molecule_id]["atom_count"],
                "charge": MOLECULES[molecule_id]["charge"],
                "multiplicity": MOLECULES[molecule_id]["multiplicity"],
                "input_role": (
                    "held_out_blind_prediction" if molecule_id == "ISO-M4" else "calculation_system"
                ),
            }
            for molecule_id in spec.molecule_ids
        },
    }


def _measurements(spec: TaskSpec) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "measurement_type": "experimentally derived thermodynamically effective molecular surface",
        "surface_area_unit": "angstrom^2",
        "source_boundary": "Values are experimental TE inputs from Supplementary Data 1; paper-computed isodensity surfaces are not included.",
        "measurements": [
            {
                "measurement_id": f"TE-{molecule_id}",
                "molecule_id": molecule_id,
                "value": MOLECULES[molecule_id]["te_surface_angstrom2"],
                "role": "calibration",
            }
            for molecule_id in spec.visible_te_ids
        ],
        "hidden_measurements": ["TE-ISO-M4"] if "ISO-M4" in spec.molecule_ids else [],
    }


def _copy_published_conformers(spec: TaskSpec, data_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for molecule_id in spec.molecule_ids:
        source_dir = REFERENCE_ROOT / "published_conformers" / molecule_id
        destination_dir = data_root / "initial_structures" / molecule_id
        destination_dir.mkdir(parents=True, exist_ok=True)
        files = sorted(source_dir.glob("*.xyz"), key=lambda path: int(path.stem.split("-")[-1]))
        expected = MOLECULES[molecule_id]["published_conformer_count"]
        if len(files) != expected:
            raise RuntimeError(f"{molecule_id}: expected {expected} public conformers, found {len(files)}")
        for source in files:
            destination = destination_dir / source.name
            shutil.copyfile(source, destination)
            first_line = destination.read_text(encoding="utf-8").splitlines()[0].strip()
            atom_count = int(first_line)
            if atom_count != MOLECULES[molecule_id]["atom_count"]:
                raise RuntimeError(
                    f"{destination}: expected {MOLECULES[molecule_id]['atom_count']} atoms, found {atom_count}"
                )
            records.append(
                {
                    "molecule_id": molecule_id,
                    "conformer_id": source.stem,
                    "path": destination.relative_to(data_root).as_posix(),
                    "atom_count": atom_count,
                    "charge": MOLECULES[molecule_id]["charge"],
                    "multiplicity": MOLECULES[molecule_id]["multiplicity"],
                    "geometry_status": "paper_supplementary_data_2_public_conformer",
                    "sha256": _sha256(destination),
                }
            )
    return records


def _data_readme(spec: TaskSpec, reproduction: bool) -> str:
    mode_text = (
        "This guided-reproduction input adds the paper-reconstructed protocol and public Supplementary Data 2 conformers."
        if reproduction
        else "This open-discovery input contains no software choice, method hierarchy, basis set, conformer workflow, cutoff grid, or paper route."
    )
    coordinate_text = (
        "The XYZ files are public paper conformers and are starting inputs, not wavefunctions, energies, or surface results."
        if reproduction
        else "No author conformer coordinates are included; generate appropriate three-dimensional structures and conformers from the molecular identities."
    )
    return f"""# {spec.title} input data

{mode_text}

Visible experimental values are thermodynamically effective (TE) surface-area
inputs.  The tetrahydrofuran TE value is hidden wherever ISO-M4 is a blind
system.  No paper-computed isodensity surface, optimal cutoff, wavefunction,
quantum output, conformer energy, statistical weight, or reference answer is
present.

{coordinate_text}
"""


def _workflow_requirements(spec: TaskSpec) -> dict[str, Any]:
    stage_map = {
        "01": [
            "validate public conformers",
            "run PBE/B3LYP/DSD-PBEP86/CCSD(T) at def2-TZVPD as feasible",
            "export wavefunctions",
            "run the full cutoff grid",
            "compare DFT surfaces to newly computed CCSD(T) references",
        ],
        "02": [
            "validate all supplied conformers",
            "run DSD-PBEP86/def2-QZVPD densities",
            "export wavefunctions and compute the full cutoff grid",
            "derive internally consistent Boltzmann weights",
            "compare lowest conformer and ensemble surfaces",
        ],
        "03": [
            "validate all supplied conformers",
            "run production densities and full cutoff grid",
            "derive conformer-weighted molecular surfaces",
            "calculate subset MUPE and Pearson R at every cutoff",
            "select the subset optimum without reading hidden paper values",
        ],
        "04": [
            "recompute calibration-molecule surfaces",
            "select and lock a cutoff",
            "recompute the ISO-M4 surface",
            "submit the blind prediction before hidden comparison",
        ],
        "05": [
            "reproduce the method comparison",
            "recompute production wavefunctions for all public conformers",
            "run the full cutoff grid",
            "reconstruct conformer ensembles and cutoff statistics",
            "lock and report the ISO-M4 blind prediction",
        ],
    }
    return {
        "schema_version": 1,
        "task_id_suffix": f"{spec.number}_{spec.suffix}",
        "result_values_included": False,
        "author_quantum_outputs_included": False,
        "required_main_profile_stages": stage_map[spec.number],
        "failure_policy": [
            "Retain failed ORCA and Multiwfn logs and record the attempted remedy.",
            "Do not silently remove a conformer or change molecular connectivity.",
            "Do not substitute paper-computed surfaces for failed calculations.",
            "Report a partial result and missing evidence when a required stage cannot be completed.",
        ],
    }


def _manifest_records(data_root: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted(data_root.rglob("*")):
        if not path.is_file() or path.name == "input_manifest.json":
            continue
        records.append(
            {
                "path": path.relative_to(data_root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
        )
    return records


def _task_info(spec: TaskSpec, reproduction: bool) -> dict[str, Any]:
    task_id = spec.reproduction_id if reproduction else spec.open_id
    requirements = spec.reproduction_requirements if reproduction else spec.open_requirements
    deliverables = [
        {"path": path, "description": description, **({"allow_empty": True} if allow_empty else {})}
        for path, description, allow_empty in spec.deliverables
    ]
    return {
        "task_id": task_id,
        "source_id": (
            "electron_isodensity_2024_guided_reproduction"
            if reproduction
            else "electron_isodensity_2024_open_discovery"
        ),
        "category": "molecular_surface_quantum_chemistry",
        "task": spec.reproduction_task if reproduction else spec.open_task,
        "scientific_mode": "guided_reproduction" if reproduction else (
            "independent_open_discovery" if spec.number == "05" else "focused_open_discovery"
        ),
        "scientific_mode_description": (
            "The paper-reconstructed method hierarchy, public conformers, cutoff route, and validation sequence are supplied; all numerical results must be recomputed."
            if reproduction
            else "The scientific question and input data are fixed, but no software, method, conformer route, cutoff grid, provider, or stopping path is prescribed."
        ),
        "scientific_requirements": list(requirements),
        "required_deliverables": deliverables,
        "data": [
            {
                "name": (
                    "Guided Electron Isodensity reproduction inputs"
                    if reproduction
                    else "Electron Isodensity open-discovery inputs"
                ),
                "path": "data/benchmark_data",
                "type": "directory",
                "description": (
                    "Task-specific molecular identities and experimental inputs plus public paper conformers, method protocol, author input templates, and workflow requirements. No author quantum output or result is included."
                    if reproduction
                    else "Task-specific molecular identities and experimental TE inputs only. No paper method, route, conformer, calculation output, or result is included."
                ),
            }
        ],
        "archive_extractions": [],
        "benchmark_family": "electron_isodensity_surface",
        "task_mode": "guided_reproduction" if reproduction else "open_discovery",
        "method_disclosure": "paper_reconstructed_protocol" if reproduction else "none",
        "pathway_disclosure": "paper_execution_route" if reproduction else "none",
    }


def _reference_result(spec: TaskSpec) -> dict[str, Any]:
    if spec.reference_key == "method_selection":
        return {
            "paper_conclusion": "DSD-PBEP86 is the closest tested DFT density to CCSD(T) and is selected for production calculations.",
            "paper_full_comparison_mupe_percent": {"PBE": 0.24, "B3LYP": 0.36, "DSD-PBEP86": 0.08},
            "subset_scoring_policy": "Score the recomputed ranking and evidence; exact paper-wide errors are not required from the three-molecule subset.",
        }
    if spec.reference_key == "conformer_effects":
        return {
            "paper_conclusion": "Conformer sampling improves agreement, especially for flexible molecules.",
            "paper_global_single_lowest_mupe_percent": 1.87,
            "paper_global_ensemble_mupe_percent": 1.5922920870480508,
            "molecule_targets": {
                molecule_id: {
                    "te_surface_angstrom2": MOLECULES[molecule_id]["te_surface_angstrom2"],
                    "paper_ensemble_surface_angstrom2": MOLECULES[molecule_id]["paper_iso_surface_0_0016_angstrom2"],
                    "published_conformer_count": MOLECULES[molecule_id]["published_conformer_count"],
                }
                for molecule_id in spec.molecule_ids
            },
            "ISO-M6_example_individual_surfaces_angstrom2": [159.8, 149.2],
        }
    if spec.reference_key == "cutoff_calibration":
        return {
            "paper_104_molecule_optimum_cutoff_au": 0.0016,
            "paper_104_molecule_mupe_percent": 1.5922920870480508,
            "paper_104_molecule_pearson_r": 0.995,
            "paper_cutoff_mupe_curve_percent": PAPER_CUTOFF_MUPE,
            "subset_scoring_policy": "The supplied six-molecule optimum must be computed and reported separately; closeness to 0.0016 is supportive but process evidence is primary.",
        }
    if spec.reference_key == "blind_prediction":
        return {
            "held_out_molecule_id": "ISO-M4",
            "hidden_te_surface_angstrom2": MOLECULES["ISO-M4"]["te_surface_angstrom2"],
            "paper_iso_surface_0_0016_angstrom2": MOLECULES["ISO-M4"]["paper_iso_surface_0_0016_angstrom2"],
            "full_credit_relative_error_to_paper_percent": 2.0,
            "partial_credit_relative_error_to_paper_percent": 5.0,
        }
    return {
        "paper_method_conclusion": "DSD-PBEP86 was selected as the production density method after CCSD(T) comparison.",
        "paper_optimum_cutoff_au": 0.0016,
        "paper_ensemble_mupe_percent": 1.5922920870480508,
        "paper_pearson_r": 0.995,
        "paper_single_lowest_mupe_percent": 1.87,
        "held_out_ISO_M4": {
            "hidden_te_surface_angstrom2": MOLECULES["ISO-M4"]["te_surface_angstrom2"],
            "paper_iso_surface_angstrom2": MOLECULES["ISO-M4"]["paper_iso_surface_0_0016_angstrom2"],
        },
        "subset_scoring_policy": "Evaluate the seven-molecule reproduction as a benchmark subset and do not require exact equality to the 104-molecule aggregate.",
    }


def _ground_truth(spec: TaskSpec, reproduction: bool, manifest_sha256: str) -> dict[str, Any]:
    task_id = spec.reproduction_id if reproduction else spec.open_id
    expected_paths = [path for path, _, _ in spec.deliverables]
    task_specific = {
        "01": ("method_hierarchy", "A real higher-level reference and density-surface method comparison support the selected production method."),
        "02": ("conformer_ensemble", "Multiple validated conformers, consistent weights, and single-versus-ensemble surfaces support the conformer conclusion."),
        "03": ("cutoff_curve", "A recomputed multi-point cutoff curve and statistics support the selected optimum."),
        "04": ("blind_prediction", "Calibration choices are locked before a newly computed ISO-M4 prediction is reported."),
        "05": ("end_to_end_science", "Method, conformer, cutoff, and blind-prediction conclusions form one internally consistent computed workflow."),
    }
    criterion_id, criterion_description = task_specific[spec.number]
    gates = [
        {
            "id": "real_quantum_evidence",
            "description": "At least one valid newly generated quantum-chemistry output and wavefunction artifact supports reported surface values.",
            "score_cap_if_failed": 35,
        },
        {
            "id": "real_surface_evidence",
            "description": "Surface areas come from a real electron-density isosurface program in this run, not from paper tables or geometric proxies.",
            "score_cap_if_failed": 45,
        },
        {
            "id": "input_and_hidden_boundary",
            "description": "No hidden reference, source-data surface, or internet-discovered answer is substituted for computation.",
            "score_cap_if_failed": 20,
        },
    ]
    if spec.number in {"02", "03", "05"}:
        gates.append(
            {
                "id": "conformer_evidence",
                "description": "Flexible-molecule conclusions include multiple conformers or an explicit calculation-backed limitation.",
                "score_cap_if_failed": 60,
            }
        )
    if spec.number in {"04", "05"}:
        gates.append(
            {
                "id": "blind_lock",
                "description": "The ISO-M4 prediction is recorded before hidden-target comparison.",
                "score_cap_if_failed": 70,
            }
        )
    return {
        "expected_tool_calls": [
            {"class": "structure_or_conformer_generation", "required": not reproduction},
            {"class": "electronic_structure", "backend_examples": ["orca"]},
            {"class": "wavefunction_conversion", "backend_examples": ["orca_2aim"]},
            {"class": "electron_isodensity_surface", "backend_examples": ["multiwfn"]},
        ],
        "expected_result": _reference_result(spec),
        "expected_structured_output": expected_paths,
        "evaluation_mode": "rubric_100",
        "score_max": 100,
        "scoring_rubric": [
            {"id": "planning_and_provenance", "max_score": 15, "description": "Resource-aware plan, software versions, inputs, commands, artifacts, failures, and revisions are traceable."},
            {"id": "real_computation", "max_score": 25, "description": "New quantum wavefunctions and electron-density isosurface calculations are complete and validated."},
            {"id": "data_and_numerical_quality", "max_score": 20, "description": "Molecular identity, charge, multiplicity, conformers, units, weights, cutoff handling, and statistics are internally consistent."},
            {"id": criterion_id, "max_score": 25, "description": criterion_description},
            {"id": "reporting_and_uncertainty", "max_score": 15, "description": "The report links claims to artifacts and separates computed evidence, experiment, inference, version effects, and unresolved uncertainty."},
        ],
        "critical_failures": [
            "No real electronic-structure calculation was executed.",
            "No real electron-density isosurface calculation was executed.",
            "Paper-published surface values or the hidden ISO-M4 target were presented as newly computed outputs.",
            "Reported numerical claims cannot be traced to artifacts from this run.",
        ],
        "judge_instructions": (
            "Score computation and evidence before numerical agreement. The visible task is a seven-molecule or smaller benchmark subset, whereas several hidden aggregate values are from the 104-molecule paper. Do not require the subset to reproduce paper-wide metrics exactly. Apply every evidence gate and explain any cap."
        ),
        "reference_evidence": {
            "paper_doi": DOI,
            "task_id": task_id,
            "task_mode": "guided_reproduction" if reproduction else "open_discovery",
            "input_manifest_sha256": manifest_sha256,
            "paper_reference": _reference_result(spec),
            "source_boundary": "Hidden paper and source-data results are evaluator-only; visible experimental TE values are raw calibration inputs.",
        },
        "managed_computation_policy": {
            "allow_direct_native_software_execution": True,
            "per_calculation_target_minutes": 10,
            "parallel_execution_allowed": True,
            "do_not_fabricate_on_timeout": True,
        },
        "evidence_gate_policy": {"judge_must_assess_all": True, "gates": gates},
        "current_toolbox_reproduction_baseline": {
            "status": "representative_components_verified",
            "classification": "solvable",
            "major_paper_conclusion_reproduced_in_this_audit": False,
            "installed_software": ["ORCA 6.1.1", "Multiwfn 2026.7.15", "CREST 3.0.2", "xTB 6.7.1"],
            "verified_components": [
                "DSD-PBEP86/def2-QZVPD ORCA wavefunction generation on ethane and 1-pentanethiol",
                "ORCA GBW to WFN conversion with orca_2aim",
                "Multiwfn molecular electron-isodensity surface area at a paper-relevant cutoff",
                "CCSD unrelaxed MDCI density generation, orca_plot cube export, and Multiwfn external-grid surface analysis on ethane",
                "Version-compatible Multiwfn 2026.7.15 menu streams for WFN/WFX and external-grid inputs",
            ],
            "unresolved_requirements": [
                "No typed batch Action currently exposes electron-isodensity surface-area scans; direct native Multiwfn execution is required.",
                "The accessible paper does not uniquely specify a separate thermochemical energy for conformer weights; sensitivity must be reported.",
            ],
        },
    }


def _build_task(spec: TaskSpec, reproduction: bool) -> None:
    task_id = spec.reproduction_id if reproduction else spec.open_id
    with tempfile.TemporaryDirectory(prefix=f".{task_id}.", dir=TASKS_ROOT) as temporary:
        build_root = Path(temporary) / task_id
        data_root = build_root / "data" / "benchmark_data"
        data_root.mkdir(parents=True)

        _write_text(data_root / "README.md", _data_readme(spec, reproduction))
        _write_json(data_root / "molecular_systems.json", _molecular_systems(spec))
        _write_json(
            data_root / "conditions.json",
            {
                "schema_version": 1,
                "temperature_kelvin": 298.15,
                "density_unit": "electrons/bohr^3",
                "surface_area_unit": "angstrom^2",
                "blind_molecule_ids": ["ISO-M4"] if "ISO-M4" in spec.molecule_ids else [],
            },
        )
        if spec.visible_te_ids:
            _write_json(data_root / "experimental_measurements" / "te_surfaces.json", _measurements(spec))

        conformer_records: list[dict[str, Any]] = []
        if reproduction:
            conformer_records = _copy_published_conformers(spec, data_root)
            protocol = dict(COMPUTATIONAL_PROTOCOL)
            protocol["task_scope"] = {
                "task_id": task_id,
                "molecule_ids": list(spec.molecule_ids),
                "visible_experimental_ids": list(spec.visible_te_ids),
            }
            _write_json(data_root / "computational_protocol.json", protocol)
            _write_json(data_root / "workflow_requirements.json", _workflow_requirements(spec))
            template_root = data_root / "author_input_templates"
            template_root.mkdir(parents=True, exist_ok=True)
            for filename in ("orca_input.in", "Multiwfn.in"):
                shutil.copyfile(
                    REFERENCE_ROOT / "author_input_templates" / filename,
                    template_root / filename,
                )
            _write_text(template_root / "orca_6_compatible.in", ORCA_6_COMPATIBLE_TEMPLATE)
            _write_text(
                template_root / "ccsd_density_orca_6.in",
                CCSD_DENSITY_ORCA_6_TEMPLATE,
            )
            _write_text(
                template_root / "Multiwfn_2026_surface_area.menu",
                MULTIWFN_2026_SURFACE_MENU,
            )
            _write_text(
                template_root / "orca_plot_ccsd_density.menu",
                ORCA_PLOT_CCSD_DENSITY_MENU,
            )
            _write_text(
                template_root / "Multiwfn_2026_external_grid_surface.menu",
                MULTIWFN_2026_EXTERNAL_GRID_SURFACE_MENU,
            )

        manifest = {
            "schema_version": 1,
            "task_id": task_id,
            "task_mode": "guided_reproduction" if reproduction else "open_discovery",
            "molecule_ids": list(spec.molecule_ids),
            "visible_te_measurement_ids": [f"TE-{item}" for item in spec.visible_te_ids],
            "hidden_measurement_ids": ["TE-ISO-M4"] if "ISO-M4" in spec.molecule_ids else [],
            "published_conformer_count": len(conformer_records),
            "published_conformer_records": conformer_records,
            "author_quantum_outputs": 0,
            "author_wavefunctions": 0,
            "author_surface_results": 0,
            "published_optimal_cutoff_values": 0,
            "reference_answers": 0,
            "method_protocol_files": ["computational_protocol.json"] if reproduction else [],
            "workflow_requirement_files": ["workflow_requirements.json"] if reproduction else [],
            "files": _manifest_records(data_root),
        }
        _write_json(data_root / "input_manifest.json", manifest)
        manifest_sha = _sha256(data_root / "input_manifest.json")
        _write_json(build_root / "task_info.json", _task_info(spec, reproduction))
        _write_json(
            build_root / "target_study" / "ground_truth.json",
            _ground_truth(spec, reproduction, manifest_sha),
        )
        _safe_replace_directory(build_root, TASKS_ROOT / task_id)


def main() -> None:
    _bootstrap_shared_reference()
    for spec in TASK_SPECS:
        _build_task(spec, reproduction=False)
        _build_task(spec, reproduction=True)
    print("Built Electron Isodensity dual-track tasks:")
    for spec in TASK_SPECS:
        print(f"  {spec.open_id}")
        print(f"  {spec.reproduction_id}")


if __name__ == "__main__":
    main()
