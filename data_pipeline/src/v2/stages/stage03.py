"""Stage 03: review native-software coverage and resource feasibility."""

from src.v2.stages._computational_content import (
    _call_complete_json,
    _chunks,
    _compact_chunk_review,
    _find_deterministic_author_experiments,
    _is_atomic_coordinate_dump,
    _is_explicit_author_laboratory_evidence,
    _is_stage03_eligible,
    _non_original_article_guard,
    _reduce_evidence_packet,
    _sanitize_reduce_response,
    _validate_experiment_map,
    _validate_map,
    run_computational_content_screening,
)
from src.v2.stages._toolbox_resource import (
    _bound_prompt_packet,
    _call_complete_inventory,
    _combine_decision,
    _compact_softcite_mentions,
    _looks_like_nonsoftware_name,
    _merge_explicit_executable_cues,
    _safe_output_tokens,
    _sanitize_review,
    _softcite_mentions,
    _target_blocks,
    coverage_gate,
    find_explicit_executable_cues,
    find_software_mentions,
    resolve_software,
    resource_gate,
    run_toolbox_resource_screening,
)

__all__ = [
    "_bound_prompt_packet",
    "_call_complete_inventory",
    "_call_complete_json",
    "_chunks",
    "_combine_decision",
    "_compact_chunk_review",
    "_compact_softcite_mentions",
    "_find_deterministic_author_experiments",
    "_is_atomic_coordinate_dump",
    "_is_explicit_author_laboratory_evidence",
    "_is_stage03_eligible",
    "_looks_like_nonsoftware_name",
    "_merge_explicit_executable_cues",
    "_non_original_article_guard",
    "_reduce_evidence_packet",
    "_safe_output_tokens",
    "_sanitize_reduce_response",
    "_sanitize_review",
    "_softcite_mentions",
    "_target_blocks",
    "_validate_experiment_map",
    "_validate_map",
    "coverage_gate",
    "find_explicit_executable_cues",
    "find_software_mentions",
    "resolve_software",
    "resource_gate",
    "run_stage03",
]


def run_stage03(**kwargs):
    if "stage02_records" not in kwargs:
        return run_computational_content_screening(**kwargs)
    return run_toolbox_resource_screening(**kwargs)
