from __future__ import annotations

from src.stages.stage02_computational_content.workflows import (
    sanitize_workflow_candidates,
    sanitize_workflow_verifications,
)
from src.stages.stage03_toolbox_resource_gate.stage import (
    STAGE03_FORWARD_DECISIONS,
    _combine_decision,
    _freeze_workflow_bindings,
    _merge_workflow_software_mentions,
    _reconcile_software_roles_with_workflows,
    coverage_gate,
    resolve_software,
    workflow_coverage_results,
)


def test_stage02_confirms_multiple_workflows_in_one_verification_response() -> None:
    discovery = {
        "workflow_candidates": [
            {
                "workflow_id": "wf-energy",
                "chemical_system": "catalyst conformers",
                "scientific_output": "relative energies",
                "scientific_use": "explain selectivity",
                "steps": [
                    {
                        "step_id": "s1",
                        "action": "optimize conformers",
                        "generated_output": "optimized structures",
                        "evidence_ids": ["ev-energy"],
                    }
                ],
                "evidence_ids": ["ev-energy"],
            },
            {
                "workflow_id": "wf-md",
                "chemical_system": "solvated catalyst",
                "scientific_output": "solvation shell distribution",
                "scientific_use": "compare solvents",
                "steps": [
                    {
                        "step_id": "s1",
                        "action": "run molecular dynamics",
                        "generated_output": "trajectory",
                        "evidence_ids": ["ev-md"],
                    }
                ],
                "evidence_ids": ["ev-md"],
            },
        ]
    }
    candidates, warnings = sanitize_workflow_candidates(
        discovery,
        valid_ids={"ev-energy", "ev-md"},
        computational_ids={"ev-energy", "ev-md"},
    )
    verification = {
        "workflow_verifications": [
            _confirmed_verification("wf-energy", "ev-energy"),
            {
                **_confirmed_verification("wf-md", "ev-md"),
                "generated_chemical_output": "uncertain",
            },
        ]
    }

    rows, confirmed, verification_warnings = sanitize_workflow_verifications(
        verification,
        candidates=candidates,
        valid_ids={"ev-energy", "ev-md"},
        computational_ids={"ev-energy", "ev-md"},
        minimum_confidence=0.85,
    )

    assert warnings == []
    assert verification_warnings == []
    assert [row["workflow_id"] for row in confirmed] == ["wf-energy"]
    assert [row["confirmed"] for row in rows] == [True, False]


def test_stage03_official_versions_resolve_to_catalog_backends() -> None:
    aliases = {
        "gaussian": ["Gaussian", "Gaussian 16"],
        "vasp": ["VASP"],
        "cp2k": ["CP2K"],
        "multiwfn": ["Multiwfn"],
    }
    profile = {
        "backends": {
            identifier: {"availability": "declared_supported"}
            for identifier in aliases
        }
    }
    names = [
        "Gaussian 16 Revision C.01",
        "Gaussian16w",
        "VASP 6.3.2",
        "CP2K2024.1",
        "Multiwfn 3.8(dev)",
    ]

    mappings = resolve_software(
        [
            {"raw_name": name, "role": "core_compute", "actual_use": True}
            for name in names
        ],
        aliases,
        profile,
    )

    assert all(row["catalog_present"] for row in mappings)
    assert all(row["coverage_state"] == "covered" for row in mappings)
    assert {row["name_resolution"] for row in mappings} == {"official_version_variant"}


def test_stage03_one_covered_workflow_prevents_global_uncovered_rejection() -> None:
    review = {
        "workflows": [
            _bound_workflow("wf-covered", "Gaussian"),
            _bound_workflow("wf-uncovered", "Molpro"),
        ]
    }
    mappings = [
        _mapping("wf-covered", "Gaussian", "covered", catalog_present=True),
        _mapping("wf-uncovered", "Molpro", "uncovered", catalog_present=False),
    ]

    results = workflow_coverage_results(review, mappings)
    coverage = coverage_gate(review, mappings, {}, {}, workflow_results=results)

    assert [row["status"] for row in results] == [
        "workflow_covered",
        "workflow_uncovered",
    ]
    assert coverage == "covered"
    assert _combine_decision(coverage) == "software_covered"


def test_stage03_rejects_only_when_every_workflow_is_explicitly_uncovered() -> None:
    review = {
        "workflows": [
            _bound_workflow("wf-a", "Molpro"),
            _bound_workflow("wf-b", "TURBOMOLE"),
        ]
    }
    mappings = [
        _mapping("wf-a", "Molpro", "uncovered", catalog_present=False),
        _mapping("wf-b", "TURBOMOLE", "uncovered", catalog_present=False),
    ]

    coverage = coverage_gate(review, mappings, {}, {})

    assert coverage == "core_software_uncovered"
    assert _combine_decision(coverage) == "core_software_uncovered"


def test_stage03_unnamed_software_is_forwarded_for_stage05_review() -> None:
    review = {
        "workflows": [
            {
                "workflow_id": "wf-unnamed",
                "steps": [
                    {
                        "step_id": "s1",
                        "action": "run DFT",
                        "essential": True,
                        "execution_layer": "named_software",
                        "software": None,
                    }
                ],
            }
        ]
    }

    coverage = coverage_gate(review, [], {}, {})
    decision = _combine_decision(coverage)

    assert coverage == "software_inventory_unconfirmed"
    assert decision == "software_inventory_unconfirmed"
    assert decision in STAGE03_FORWARD_DECISIONS


def test_stage03_explicit_bound_named_runtime_absent_from_catalog_is_uncovered() -> None:
    mappings = resolve_software(
        [
            {
                "raw_name": "Independent Quantum Program",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": ["wf1"],
                "evidence_ids": ["ev1"],
                "exact_quote": "Calculations used Independent Quantum Program.",
            }
        ],
        {},
        {"backends": {}},
    )

    assert mappings[0]["coverage_state"] == "uncovered"
    assert mappings[0]["name_resolution"] == "explicit_named_runtime_absent_from_catalog"


def test_stage03_does_not_trust_normalized_hint_as_catalog_identity() -> None:
    mappings = resolve_software(
        [
            {
                "raw_name": "Vienna simulation engine",
                "normalized_hint": "VASP",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": [],
                "evidence_ids": [],
                "exact_quote": "",
            }
        ],
        {"vasp": ["VASP"]},
        {"backends": {"vasp": {"availability": "declared_supported"}}},
    )

    assert mappings[0]["coverage_state"] == "unconfirmed"
    assert mappings[0]["normalized_identifier"] is None


def test_stage03_parenthetical_abbreviation_binds_catalog_mapping_to_step() -> None:
    review = {
        "workflows": [
            _bound_workflow("wf1", "Vienna Ab Initio Simulation Package (VASP)")
        ]
    }
    mappings = [
        {
            **_mapping(
                "wf1",
                "Vienna Ab Initio Simulation Package",
                "covered",
                catalog_present=True,
            ),
            "normalized_identifier": "vasp",
        }
    ]

    results = workflow_coverage_results(review, mappings)

    assert results[0]["status"] == "workflow_covered"
    assert results[0]["step_results"][0]["normalized_identifier"] == "vasp"


def test_stage03_unclosed_parenthetical_abbreviation_resolves_to_catalog() -> None:
    mappings = resolve_software(
        [
            {
                "raw_name": "Vienna Ab Initio Simulation Package (VASP",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
            }
        ],
        {"vasp": ["VASP"]},
        {"backends": {"vasp": {"availability": "declared_supported"}}},
    )

    assert mappings[0]["normalized_identifier"] == "vasp"
    assert mappings[0]["coverage_state"] == "covered"
    assert mappings[0]["name_resolution"] == "parenthetical_alias"


def test_stage03_promoted_preparation_software_is_nonblocking() -> None:
    mentions, _ = _merge_workflow_software_mentions(
        [],
        [
            {
                "workflow_id": "wf1",
                "steps": [
                    {
                        "step_id": "s1",
                        "action": "Prepare receptor input by adding hydrogens and charges",
                        "software": "Independent Preparation Tool",
                        "essential": True,
                        "evidence_ids": ["ev1"],
                    }
                ],
            }
        ],
        {"ev1": "The receptor was prepared using Independent Preparation Tool."},
        {},
    )

    assert mentions[0]["role"] == "required_preprocessing"


def test_stage03_promoted_analysis_software_is_nonblocking() -> None:
    mentions, _ = _merge_workflow_software_mentions(
        [],
        [
            {
                "workflow_id": "wf1",
                "steps": [
                    {
                        "step_id": "s2",
                        "action": "Visualize the generated orbitals",
                        "software": "Independent Viewer",
                        "essential": True,
                        "evidence_ids": ["ev2"],
                    }
                ],
            }
        ],
        {"ev2": "The orbitals were visualized using Independent Viewer."},
        {},
    )

    assert mentions[0]["role"] == "required_analysis"


def test_stage03_reconciles_model_core_role_with_preparation_step() -> None:
    mentions, warnings = _reconcile_software_roles_with_workflows(
        [
            {
                "raw_name": "Independent Preparation Tool",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": ["wf1"],
            }
        ],
        [
            {
                "workflow_id": "wf1",
                "steps": [
                    {
                        "action": "Prepare the receptor by adding hydrogens",
                        "software": "Independent Preparation Tool",
                        "essential": True,
                    }
                ],
            }
        ],
        {},
    )

    assert mentions[0]["role"] == "required_preprocessing"
    assert warnings[0]["reason"] == "role_reconciled_with_workflow_action"


def test_stage03_does_not_promote_model_visualization_role_to_core() -> None:
    mentions, warnings = _reconcile_software_roles_with_workflows(
        [
            {
                "raw_name": "Independent Viewer",
                "role": "visualization",
                "actual_use": True,
                "workflow_ids": ["wf1"],
            }
        ],
        [
            {
                "workflow_id": "wf1",
                "steps": [
                    {
                        "action": "Visualize the molecular dynamics simulation",
                        "software": "Independent Viewer",
                        "essential": True,
                    }
                ],
            }
        ],
        {},
    )

    assert mentions[0]["role"] == "visualization"
    assert warnings == []


def test_stage03_workflow_scoped_preprocessor_is_nonblocking_when_step_is_unnamed() -> None:
    review = {
        "workflows": [
            {
                "workflow_id": "wf1",
                "steps": [
                    {
                        "step_id": "s1",
                        "action": "prepare and run a calculation",
                        "essential": True,
                        "execution_layer": "unknown",
                        "software": None,
                    }
                ],
            }
        ]
    }
    mappings = [
        _mapping("wf1", "Independent Preprocessor", "uncovered", catalog_present=False)
    ]
    mappings[0]["role"] = "required_preprocessing"

    results = workflow_coverage_results(review, mappings)

    assert results[0]["status"] == "workflow_software_inventory_unconfirmed"
    assert results[0]["required_software_results"] == []
    assert results[0]["nonblocking_software_results"][0]["raw_name"] == (
        "Independent Preprocessor"
    )


def test_stage03_uncovered_gaussview_does_not_block_covered_gaussian() -> None:
    review = {"workflows": [_bound_workflow("wf1", "Gaussian 16")]}
    mappings = [
        _mapping("wf1", "Gaussian 16", "covered", catalog_present=True),
        {
            **_mapping("wf1", "GaussView", "uncovered", catalog_present=False),
            "role": "visualization",
        },
    ]

    results = workflow_coverage_results(review, mappings)

    assert results[0]["status"] == "workflow_covered"
    assert [row["raw_name"] for row in results[0]["core_software_results"]] == [
        "Gaussian 16"
    ]
    assert [
        row["raw_name"] for row in results[0]["nonblocking_software_results"]
    ] == ["GaussView"]


def test_stage03_uncovered_iboview_does_not_block_covered_orca_and_multiwfn() -> None:
    review = {"workflows": [_bound_workflow("wf1", "ORCA")]}
    mappings = [
        _mapping("wf1", "ORCA", "covered", catalog_present=True),
        _mapping("wf1", "Multiwfn", "covered", catalog_present=True),
        {
            **_mapping("wf1", "IBOview", "uncovered", catalog_present=False),
            "role": "required_analysis",
        },
    ]

    results = workflow_coverage_results(review, mappings)
    coverage = coverage_gate(review, mappings, {}, {}, workflow_results=results)

    assert results[0]["status"] == "workflow_covered"
    assert coverage == "covered"
    assert [
        row["raw_name"] for row in results[0]["nonblocking_software_results"]
    ] == ["IBOview"]


def test_stage03_freeze_ignores_model_added_workflow_and_preserves_ids() -> None:
    frozen = [
        {
            "workflow_id": "wf1",
            "scientific_output": "energy",
            "scientific_use": "compare states",
            "evidence_ids": ["ev1"],
            "steps": [
                {
                    "step_id": "s1",
                    "action": "calculate energy",
                    "generated_output": "energy",
                    "evidence_ids": ["ev1"],
                }
            ],
        }
    ]
    model_workflows = [
        {
            "workflow_id": "wf1",
            "steps": [
                {
                    "step_id": "s1",
                    "action": "calculate energy",
                    "software": "Gaussian 16",
                    "execution_layer": "named_software",
                    "evidence_ids": ["ev1"],
                }
            ],
        },
        {"workflow_id": "invented", "steps": []},
    ]

    locked, warnings = _freeze_workflow_bindings(
        frozen, model_workflows, {"ev1": "Calculations used Gaussian 16."}
    )

    assert [row["workflow_id"] for row in locked] == ["wf1"]
    assert locked[0]["steps"][0]["software"] == "Gaussian 16"
    assert warnings[0]["reason"] == "model_added_unconfirmed_workflows_ignored"


def _confirmed_verification(workflow_id: str, evidence_id: str) -> dict:
    return {
        "workflow_id": workflow_id,
        "author_performed_computation": "yes",
        "identifiable_chemical_system": "yes",
        "actual_chemical_calculation_or_simulation": "yes",
        "generated_chemical_output": "yes",
        "scientific_use_of_output": "yes",
        "nontrivial_workflow": "yes",
        "experimental_data_analysis_only": "no",
        "evidence_ids": [evidence_id],
        "computational_evidence_ids": [evidence_id],
        "confidence": 0.95,
    }


def _bound_workflow(workflow_id: str, software: str) -> dict:
    return {
        "workflow_id": workflow_id,
        "steps": [
            {
                "step_id": "s1",
                "action": "run calculation",
                "essential": True,
                "execution_layer": "named_software",
                "software": software,
            }
        ],
    }


def _mapping(
    workflow_id: str, software: str, state: str, *, catalog_present: bool
) -> dict:
    return {
        "raw_name": software,
        "role": "core_compute",
        "actual_use": True,
        "workflow_ids": [workflow_id],
        "catalog_present": catalog_present,
        "coverage_state": state,
    }
