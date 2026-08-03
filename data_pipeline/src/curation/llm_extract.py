from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from src.core.io import merge_dict
from src.core.logging import log_progress
from src.curation.llm_client import call_json_chat
from src.curation.source_excerpt import evidence_excerpt

EDITABLE_FIELDS = {
    "central_problem",
    "inputs",
    "expected_outputs",
    "methods",
    "tools",
    "evidence",
    "controls",
    "hypotheses",
    "workflow",
    "reference_results",
    "runtime",
    "information_richness",
}


class OpenAICompatibleEvidenceExtractor:
    """Enrich ScientificRecords through an OpenAI-compatible chat endpoint."""

    def __init__(
        self,
        model: str,
        base_url: str = "https://api.openai.com/v1",
        api_key: str | None = None,
        timeout_seconds: float = 600,
        max_source_chars: int = 100_000,
        max_tokens: int | None = None,
        retries: int = 2,
        thinking: str | None = None,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.environ.get("RCB_LLM_API_KEY")
        if not self.api_key:
            raise ValueError("RCB_LLM_API_KEY is required when semantic review is enabled")
        self.timeout_seconds = timeout_seconds
        self.max_source_chars = max_source_chars
        self.max_tokens = max_tokens
        self.retries = retries
        self.thinking = thinking

    def review(self, record: dict[str, Any]) -> dict[str, Any]:
        source_text = _source_text(record, self.max_source_chars)
        packet = {
            "record": record,
            "source_text": source_text,
            "allowed_override_fields": sorted(EDITABLE_FIELDS),
        }
        override, metadata = call_json_chat(
            model=self.model,
            base_url=self.base_url,
            api_key=self.api_key,
            timeout_seconds=self.timeout_seconds,
            max_tokens=self.max_tokens,
            retries=self.retries,
            thinking=self.thinking,
            system_prompt=(
                "You are a computational-chemistry evidence extractor. Improve the supplied ScientificRecord "
                "using only facts explicitly supported by source_text. Return one JSON object containing only "
                "allowed_override_fields. For each input, result, method parameter, workflow step, hypothesis, "
                "and evidence unit, preserve a source quote or locator when available. Do not invent input files, "
                "coordinates, values, software, parameters, or availability. Use empty lists for unsupported "
                "fields. Keep paper identity, assets, classification, and task-selection fields unchanged. "
                "Be selective and concise: at most 12 inputs, 12 methods, 12 workflow steps, 20 evidence units, "
                "8 hypotheses, 8 controls, and 12 reference results. Prefer discriminative quantitative evidence."
            ),
            user_content=json.dumps(packet, ensure_ascii=False),
        )
        safe_override = {key: value for key, value in override.items() if key in EDITABLE_FIELDS}
        reviewed = merge_dict(record, safe_override)
        reviewed.setdefault("curation", {}).update(
            {"semantic_reviewer": self.model, "semantic_review_call": metadata}
        )
        return reviewed


def review_records(records: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    reviewer = OpenAICompatibleEvidenceExtractor(
        model=config["model"],
        base_url=config.get("base_url", "https://api.openai.com/v1"),
        api_key=_api_key(config),
        timeout_seconds=float(config.get("timeout_seconds", 600)),
        max_source_chars=int(config.get("max_source_chars", 100_000)),
        max_tokens=config.get("max_tokens"),
        retries=int(config.get("retries", 2)),
        thinking=config.get("thinking"),
    )
    cache_dir = Path(config["cache_dir"]).expanduser() if config.get("cache_dir") else None
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)

    def run_one(record: dict[str, Any]) -> dict[str, Any]:
        cache_path = cache_dir / f"{record['paper_id']}.json" if cache_dir else None
        if cache_path and cache_path.is_file():
            return json.loads(cache_path.read_text(encoding="utf-8"))
        reviewed = reviewer.review(record)
        if cache_path:
            cache_path.write_text(
                json.dumps(reviewed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        return reviewed

    workers = max(1, min(int(config.get("max_workers", 1)), len(records) or 1))
    output: list[dict[str, Any] | None] = [None] * len(records)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_one, record): index for index, record in enumerate(records)}
        completed_count = 0
        for future in as_completed(futures):
            index = futures[future]
            try:
                output[index] = future.result()
            except Exception as exc:
                fallback = dict(records[index])
                fallback.setdefault("curation", {})["semantic_review_error"] = (
                    f"{type(exc).__name__}: {exc}"
                )
                output[index] = fallback
            completed_count += 1
            status = (
                "failed"
                if (output[index].get("curation") or {}).get("semantic_review_error")
                else "complete"
            )
            log_progress(
                "stage_11_scientific_record_extraction",
                completed_count,
                len(records),
                records[index].get("paper_id", str(index)),
                status=status,
            )
    return [item for item in output if item is not None]


def _api_key(config: dict[str, Any]) -> str | None:
    if config.get("api_key"):
        return str(config["api_key"])
    if config.get("api_key_env"):
        return os.environ.get(str(config["api_key_env"]))
    return os.environ.get("RCB_LLM_API_KEY")


def _source_text(record: dict[str, Any], max_chars: int) -> str:
    return evidence_excerpt((record.get("assets") or {}).get("text", []), max_chars)
