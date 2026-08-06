from src.stages.stage05_preliminary_coverage import aggregate_preliminary_coverage

TOOLBOX = {
    "profile_id": "test",
    "catalog_hash": "hash",
    "backends": ["orca"],
    "unavailable": [],
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
    }


def _document(decision, mentions):
    return {
        "document_id": "d1",
        "document_role": "main_paper",
        "software_coverage": {"decision": decision, "core_software": mentions},
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
