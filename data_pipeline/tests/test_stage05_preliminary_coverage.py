from src.stages.stage05_preliminary_coverage import aggregate_preliminary_coverage

TOOLBOX = {
    "profile_id": "test",
    "catalog_hash": "hash",
    "backends": ["orca"],
    "unavailable": [],
    "scientific_smoke": ["orca"],
}
CATALOG = {
    "schema_version": 1,
    "unknown_field_policy": "unknown",
    "method_families": {"electronic_structure": {"backends": ["orca"]}},
}


def _paper(families=None):
    return {
        "paper_id": "p1",
        "supplementary_acquisition": {"presence_status": "absent_confirmed"},
        "computation_relevance": {
            "decision": "strong_candidate",
            "method_families": families or [],
        },
        "llm_computation_review": {
            "study_mode": "pure_computational",
            "author_performed_experiments": "no",
            "computation_role": "primary",
            "software_inventory_complete": "yes",
            "required_software": [],
        },
    }


def _document(decision, mentions, *, unclassified=None):
    return {
        "document_id": "d1",
        "document_role": "main_paper",
        "software_coverage": {
            "decision": decision,
            "core_software": mentions,
            "unclassified_software": unclassified or [],
        },
    }


def test_stage05_does_not_reject_missing_software_name():
    result = aggregate_preliminary_coverage(
        [_paper(["electronic_structure"])], {"p1": []}, TOOLBOX, CATALOG
    )[0]
    assert result["preliminary_coverage"]["decision"] == "method_only_candidate"
    assert result["pipeline_routing"]["continue"] is True


def test_stage05_accepts_direct_toolbox_software():
    mention = {
        "normalized_name": "orca",
        "direct_support": {"supported": True},
        "capability_equivalence": None,
    }
    result = aggregate_preliminary_coverage(
        [_paper()], {"p1": [_document("direct_covered", [mention])]}, TOOLBOX, CATALOG
    )[0]
    assert result["preliminary_coverage"]["decision"] == "direct_candidate"


def test_stage05_rejects_only_explicit_unsupported_core_software():
    mention = {
        "normalized_name": "proprietary_x",
        "direct_support": {"supported": False},
        "capability_equivalence": None,
    }
    result = aggregate_preliminary_coverage(
        [_paper()], {"p1": [_document("unsupported", [mention])]}, TOOLBOX, CATALOG
    )[0]
    assert result["preliminary_coverage"]["decision"] == "explicitly_unsupported"
    assert result["pipeline_routing"]["continue"] is False


def test_stage05_isolates_extraction_errors():
    result = aggregate_preliminary_coverage(
        [_paper()], {}, TOOLBOX, CATALOG, errors={"p1": [{"error": "boom"}]}
    )[0]
    assert result["preliminary_coverage"]["decision"] == "stage_error"
    assert result["pipeline_routing"]["continue"] is True


def test_stage05_rejects_unknown_supplementary_status_before_coverage():
    paper = _paper(["electronic_structure"])
    paper["supplementary_acquisition"] = {
        "presence_status": "unknown",
        "download_status": "access_blocked",
        "attachments": [],
    }
    result = aggregate_preliminary_coverage(
        [paper], {"p1": []}, TOOLBOX, CATALOG
    )[0]
    assert result["preliminary_coverage"]["decision"] == "supplementary_unavailable"
    assert result["pipeline_routing"]["continue"] is False
    assert result["pipeline_routing"]["stop_reason"] == (
        "supplementary_not_confirmed_absent_or_downloaded"
    )


def test_stage05_keeps_downloaded_supplementary(tmp_path):
    si = tmp_path / "si.pdf"
    si.write_bytes(b"%PDF-1.7")
    paper = _paper(["electronic_structure"])
    paper["supplementary_acquisition"] = {
        "presence_status": "available",
        "download_status": "downloaded",
        "attachments": [{"path": str(si)}],
    }
    result = aggregate_preliminary_coverage(
        [paper], {"p1": []}, TOOLBOX, CATALOG
    )[0]
    assert result["preliminary_coverage"]["decision"] == "method_only_candidate"
    assert result["pipeline_routing"]["continue"] is True


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


def test_stage05_strict_accepts_only_functional_contextual_method_match():
    mention = {
        "normalized_name": "orca",
        "direct_support": {"supported": True, "validation_level": "functional"},
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    result = aggregate_preliminary_coverage(
        [_paper(["electronic_structure"])],
        {"p1": [_document("direct_covered", [mention])]},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "direct_candidate"
    assert result["pipeline_routing"]["continue"] is True


def test_stage05_strict_rejects_interface_only_direct_support():
    mention = {
        "normalized_name": "orca",
        "direct_support": {"supported": True, "validation_level": "interface"},
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    result = aggregate_preliminary_coverage(
        [_paper(["electronic_structure"])],
        {"p1": [_document("direct_covered", [mention])]},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "workflow_software_uncovered"
    assert result["pipeline_routing"]["continue"] is False


def test_stage05_strict_rejects_method_only_candidate():
    result = aggregate_preliminary_coverage(
        [_paper(["electronic_structure"])],
        {"p1": []},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "method_only_rejected"
    assert result["pipeline_routing"]["continue"] is False


def test_stage05_strict_rejects_candidate_without_software_or_covered_method():
    result = aggregate_preliminary_coverage(
        [_paper()],
        {"p1": []},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "software_unknown_rejected"
    assert result["pipeline_routing"]["continue"] is False
    assert result["pipeline_routing"]["stop_reason"] == (
        "direct_functionally_validated_backend_required"
    )


def test_stage05_strict_rejects_extraction_error():
    result = aggregate_preliminary_coverage(
        [_paper()],
        {},
        TOOLBOX,
        CATALOG,
        errors={"p1": [{"error": "boom"}]},
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "stage_error"
    assert result["pipeline_routing"]["continue"] is False


def test_stage05_strict_rejects_when_any_core_software_is_uncovered():
    covered = {
        "normalized_name": "orca",
        "direct_support": {"supported": True, "validation_level": "functional"},
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    uncovered = {
        "normalized_name": "custom_kinetics",
        "direct_support": {"supported": False, "validation_level": "not_catalogued"},
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    result = aggregate_preliminary_coverage(
        [_paper(["electronic_structure"])],
        {"p1": [_document("unsupported", [covered, uncovered])]},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "workflow_software_uncovered"
    assert result["preliminary_coverage"]["uncovered_workflow_software"] == [
        "custom_kinetics"
    ]
    assert result["pipeline_routing"]["continue"] is False


def test_stage05_strict_rejects_execution_confirmed_unclassified_software():
    covered = {
        "normalized_name": "orca",
        "direct_support": {"supported": True, "validation_level": "functional"},
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    custom = {
        "normalized_name": "in_house_code",
        "execution_context_confirmed": True,
    }
    result = aggregate_preliminary_coverage(
        [_paper(["electronic_structure"])],
        {"p1": [_document("direct_covered", [covered], unclassified=[custom])]},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "workflow_software_uncovered"
    assert "in_house_code" in result["preliminary_coverage"]["uncovered_workflow_software"]


def test_stage05_strict_rejects_mixed_study_defense_in_depth():
    paper = _paper(["electronic_structure"])
    paper["llm_computation_review"].update(
        {
            "study_mode": "mixed_computational_experimental",
            "author_performed_experiments": "yes",
        }
    )
    result = aggregate_preliminary_coverage(
        [paper], {}, TOOLBOX, CATALOG, screening_config=STRICT
    )[0]
    assert result["preliminary_coverage"]["decision"] == "not_pure_computational"
    assert result["pipeline_routing"]["continue"] is False


def test_stage05_strict_requires_functional_backends_to_cover_every_method_family():
    mention = {
        "normalized_name": "orca",
        "direct_support": {"supported": True, "validation_level": "functional"},
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    result = aggregate_preliminary_coverage(
        [_paper(["electronic_structure", "molecular_dynamics"])],
        {"p1": [_document("direct_covered", [mention])]},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
    )[0]
    assert result["preliminary_coverage"]["decision"] == "method_coverage_incomplete"
    assert result["preliminary_coverage"]["uncovered_method_families"] == [
        "molecular_dynamics"
    ]


def test_stage05_strict_can_corroborate_uncertain_inventory_with_two_extractors():
    paper = _paper(["electronic_structure"])
    paper["llm_computation_review"].update(
        {
            "software_inventory_complete": "uncertain",
            "required_software": [{"name": "ORCA", "purpose": "DFT"}],
        }
    )
    mention = {
        "normalized_name": "orca",
        "direct_support": {"supported": True, "validation_level": "functional"},
        "execution_context_confirmed": True,
        "capability_equivalence": None,
    }
    result = aggregate_preliminary_coverage(
        [paper],
        {"p1": [_document("direct_covered", [mention])]},
        TOOLBOX,
        CATALOG,
        screening_config=STRICT,
        software_aliases={"orca": ["ORCA"]},
    )[0]
    assert result["preliminary_coverage"]["decision"] == "direct_candidate"
    assert result["preliminary_coverage"]["software_inventory_corroborated"] is True
