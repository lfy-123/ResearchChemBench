from src.stages.stage05_benchmark_suitability.stage import _audit_dimensions


def test_stage05_derived_dimensions_do_not_require_fake_source_citations() -> None:
    value = {
        name: {
            "state": "confirmed",
            "support": f"Structured support for {name}",
            "missing_fields": [],
            "evidence_ids": ["mineru-1"] if name not in {"software", "cost", "leakage_risk"} else [],
        }
        for name in (
            "scientific_significance",
            "workflow_completeness",
            "input_assets",
            "parameters",
            "ground_truth",
            "software",
            "cost",
            "leakage_risk",
        )
    }

    normalized, errors = _audit_dimensions(value, {"mineru-1"})

    assert errors == []
    assert normalized["software"]["evidence_ids"] == []
