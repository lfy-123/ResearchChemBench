"""Stage 04: normalize Stage 03 passes with high-quality MinerU parsing."""

from src.integrations.mineru import run_mineru_queue
from src.v2.stages import _toolbox_resource as _impl
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
    run_mineru_deep_normalization,
    run_toolbox_resource_screening,
)

__all__ = [
    "_bound_prompt_packet",
    "_call_complete_inventory",
    "_combine_decision",
    "_compact_softcite_mentions",
    "_deep_normalize_passed_papers",
    "_looks_like_nonsoftware_name",
    "_merge_explicit_executable_cues",
    "_safe_output_tokens",
    "_sanitize_review",
    "_softcite_mentions",
    "_target_blocks",
    "coverage_gate",
    "find_explicit_executable_cues",
    "find_software_mentions",
    "resolve_software",
    "resource_gate",
    "run_mineru_queue",
    "run_stage04",
]


def run_stage04(**kwargs):
    if "model" in kwargs:
        if "stage03_records" in kwargs and "stage02_records" not in kwargs:
            kwargs["stage02_records"] = kwargs.pop("stage03_records")
        return run_toolbox_resource_screening(**kwargs)
    return run_mineru_deep_normalization(**kwargs)


def _deep_normalize_passed_papers(**kwargs):
    # Expose the old helper while allowing tests/callers to replace the queue.
    _impl.run_mineru_queue = globals()["run_mineru_queue"]
    return _impl._deep_normalize_passed_papers(**kwargs)
