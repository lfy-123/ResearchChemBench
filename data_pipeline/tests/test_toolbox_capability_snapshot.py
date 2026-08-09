import json
import subprocess
import sys
from pathlib import Path

import pytest
from chemistry_toolbox.src.actions import ACTION_SPECS
from chemistry_toolbox.src.backend_specs import BACKEND_SPECS
from chemistry_toolbox.src.catalog import catalog_hash

from src.stages.stage05_preliminary_coverage import aggregate_preliminary_coverage

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSET_ROOT = PROJECT_ROOT / "data_pipeline/assets"
EXPANDED_SOFTWARE = {
    "acpype",
    "airss",
    "bagel",
    "gmx_mmpbsa",
    "gplearn",
    "pmx",
    "pyfrag",
    "sisso",
    "tdep",
    "vaspkit",
}
EXPANDED_FAMILIES = {
    "acpype": "molecular_dynamics",
    "airss": "periodic_materials",
    "bagel": "electronic_structure",
    "gmx_mmpbsa": "free_energy",
    "gplearn": "machine_learning_chemistry",
    "pmx": "free_energy",
    "pyfrag": "reaction_kinetics",
    "sisso": "machine_learning_chemistry",
    "tdep": "periodic_materials",
    "vaspkit": "periodic_materials",
}
REMOVED_SOFTWARE = {
    "castep",
    "crystal",
    "easyspin",
    "matlab",
    "molpro",
    "openeye",
    "qchem",
    "schrodinger",
    "terachem",
    "turbomole",
    "wien2k",
}
STRICT = {
    "screening_policy": "strict",
    "accepted_validation_levels": ["functional"],
    "require_execution_context": True,
    "require_method_match": True,
    "continue_without_software_name": False,
    "allow_capability_equivalent": False,
    "continue_on_stage_error": False,
    "require_all_core_software": True,
    "require_all_method_families": True,
    "reject_unclassified_execution_software": True,
    "require_pure_computational_review": True,
    "require_complete_software_inventory": True,
}


def _read(name):
    return json.loads((ASSET_ROOT / name).read_text(encoding="utf-8"))


def test_generated_toolbox_assets_are_current():
    subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "data_pipeline/scripts/sync_toolbox_capabilities.py"),
            "--check",
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )


def test_toolbox_profile_matches_current_catalog_and_evidence():
    profile = _read("toolbox.json")
    assert set(profile["actions"]) == {item.id for item in ACTION_SPECS}
    assert set(profile["backends"]) == {item.id for item in BACKEND_SPECS}
    assert profile["catalog_hash"] == catalog_hash(include_health=False)
    assert set(profile["backends"]) <= set(profile["scientific_smoke"])
    assert profile["local_installation_status"] == "not_evaluated"


def test_native_executables_are_exported_as_backend_aliases():
    aliases = _read("software_aliases.json")
    for backend in BACKEND_SPECS:
        if backend.id.startswith("internal_"):
            continue
        expected = {
            executable
            for executable in backend.executables
            if executable.casefold() != "mpirun"
        }
        assert expected <= set(aliases[backend.id])


def test_configured_requested_software_is_exported_for_native_layer_screening():
    aliases = _read("software_aliases.json")
    capabilities = _read("toolbox_capabilities.json")
    native = capabilities["native_software"]

    assert "vmd" in native
    assert native["vmd"]["availability"] == "configured_in_toolbox_runtime"
    assert native["vmd"]["execution_layer"] == "native_software_documentation"
    assert {"VMD", "vmd"} <= set(aliases["vmd"])
    assert not REMOVED_SOFTWARE & set(native)


def test_expanded_software_is_functional_and_method_mapped():
    profile = _read("toolbox.json")
    capabilities = _read("toolbox_capabilities.json")
    aliases = _read("software_aliases.json")
    assert EXPANDED_SOFTWARE <= set(profile["backends"])
    assert EXPANDED_SOFTWARE <= set(profile["scientific_smoke"])
    for software, family in EXPANDED_FAMILIES.items():
        assert software in aliases
        assert software in capabilities["method_families"][family]["backends"]
        assert capabilities["backends"][software]["validation_level"] == "functional"


def test_removed_or_unintegrated_software_is_not_claimed_available():
    profile = _read("toolbox.json")
    aliases = _read("software_aliases.json")
    capability_equivalents = _read("software_capability_map.json")
    assert profile["unavailable"] == []
    assert not REMOVED_SOFTWARE & set(profile["backends"])
    assert not REMOVED_SOFTWARE & set(profile["available_identifiers"])
    assert not REMOVED_SOFTWARE & set(aliases)
    assert not REMOVED_SOFTWARE & set(capability_equivalents)


@pytest.mark.parametrize(
    ("software", "family", "raw_name"),
    [
        ("acpype", "molecular_dynamics", "ACPYPE"),
        ("airss", "periodic_materials", "AIRSS"),
        ("bagel", "electronic_structure", "BAGEL"),
        ("gmx_mmpbsa", "free_energy", "gmx_MMPBSA"),
        ("gplearn", "machine_learning_chemistry", "gplearn"),
        ("pmx", "free_energy", "pmx"),
        ("pyfrag", "reaction_kinetics", "PyFrag 2019"),
        ("sisso", "machine_learning_chemistry", "SISSO"),
        ("tdep", "periodic_materials", "TDEP"),
        ("vaspkit", "periodic_materials", "VASPKIT"),
    ],
)
def test_expanded_software_passes_real_strict_stage05_route(
    software, family, raw_name
):
    profile = _read("toolbox.json")
    capabilities = _read("toolbox_capabilities.json")
    aliases = _read("software_aliases.json")
    paper = {
        "paper_id": "expanded-toolbox-paper",
        "supplementary_acquisition": {"presence_status": "absent_confirmed"},
        "computation_relevance": {
            "decision": "strong_candidate",
            "method_families": [family],
        },
        "llm_computation_review": {
            "study_mode": "pure_computational",
            "author_performed_experiments": "no",
            "computation_role": "primary",
            "software_inventory_complete": "yes",
            "required_software": [{"name": raw_name, "purpose": family}],
        },
    }
    mention = {
        "normalized_name": software,
        "direct_support": {
            "supported": True,
            "validation_level": "functional",
        },
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    document = {
        "document_id": "expanded-toolbox-document",
        "document_role": "main_paper",
        "software_coverage": {
            "decision": "direct_covered",
            "core_software": [mention],
            "unclassified_software": [],
        },
    }

    result = aggregate_preliminary_coverage(
        [paper],
        {paper["paper_id"]: [document]},
        profile,
        capabilities,
        screening_config=STRICT,
        software_aliases=aliases,
    )[0]

    assert result["preliminary_coverage"]["decision"] == "direct_candidate"
    assert result["pipeline_routing"]["continue"] is True
