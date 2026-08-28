from __future__ import annotations

from dataclasses import dataclass
from typing import Any

RETRYABLE_DECISIONS = {
    "copy_incomplete",
    "deep_parse_failed",
    "parse_failed",
    "processing_failed",
    "retryable_acquisition_error",
}


@dataclass(frozen=True)
class WorkDisposition:
    status: str
    failure_class: str | None = None


def classify_stage_record(stage: str, row: dict[str, Any]) -> WorkDisposition:
    """Map a stage record to resume semantics without changing its science decision."""

    decision = str(row.get("decision") or "").casefold()
    processing = str(row.get("processing_status") or "").casefold()
    passed = bool(row.get("passed"))

    # Stage01 is the terminal document-completeness gate. Only a complete
    # package or successfully normalized document is reusable; every other
    # outcome is audited and then terminally pruned instead of retried.
    if stage == "stage01_package":
        package_status = str(row.get("package_status") or "").casefold()
        if package_status in {"complete_with_si", "complete_confirmed_no_si"} and processing not in {
            "failed",
            "pending",
            "processing_failed",
            "retryable_failed",
        }:
            return WorkDisposition("forwarded")
        return WorkDisposition("terminal_reject", "stage01_package_incomplete")
    if stage == "stage01":
        if (passed or decision == "pass") and processing not in {
            "failed",
            "pending",
            "processing_failed",
            "retryable_failed",
        }:
            return WorkDisposition("forwarded")
        return WorkDisposition("terminal_reject", "stage01_document_incomplete")

    # A Stage04 MinerU timeout is the configured cost ceiling, rather than a
    # transient parser/service failure. Keep its audit row but do not schedule
    # it again in a later resume generation.
    if stage == "stage04" and str(row.get("failure_disposition") or "").casefold() == "terminal":
        return WorkDisposition(
            "terminal_reject",
            str(row.get("failure_class") or "mineru_timeout"),
        )

    if processing == "pending" or decision == "processing_pending":
        return WorkDisposition("pending", "awaiting_pending_documents")
    if processing in {"failed", "processing_failed", "retryable_failed"}:
        return WorkDisposition("retryable_failed", _failure_class(stage, row))
    if decision in RETRYABLE_DECISIONS:
        return WorkDisposition("retryable_failed", _failure_class(stage, row))

    if stage == "stage00":
        copy_status = str(row.get("copy_status") or "").casefold()
        if copy_status == "complete":
            return WorkDisposition("succeeded")
        return WorkDisposition("retryable_failed", "remote_copy_incomplete")

    if stage in {"stage02", "stage03", "stage04", "stage05"}:
        if passed or decision == "pass":
            return WorkDisposition("forwarded")
        if stage == "stage05" and decision == "needs_builder_review":
            return WorkDisposition("forwarded")
        if stage == "stage05" and decision == "contract_invalid":
            return WorkDisposition("retryable_failed", "model_contract_invalid")
        return WorkDisposition("terminal_reject")

    if stage in {"stage05_router", "stage05_auditor"}:
        return WorkDisposition("succeeded")
    return WorkDisposition("succeeded")


def classify_exception(stage: str, exc: BaseException) -> str:
    text = f"{type(exc).__name__}: {exc}".casefold()
    if "timeout" in text:
        return f"{stage}_timeout"
    if any(token in text for token in ("http 5", " 502", " 503", " 504", "connection")):
        return f"{stage}_service_unavailable"
    if "json" in text or "contract" in text or "truncat" in text:
        return f"{stage}_invalid_model_response"
    if "sandbox" in text or "reclaim" in text or "terminated" in text:
        return f"{stage}_sandbox_unavailable"
    return f"{stage}_execution_error"


def _failure_class(stage: str, row: dict[str, Any]) -> str:
    error = row.get("error") or {}
    if isinstance(error, dict):
        text = " ".join(str(error.get(key) or "") for key in ("error_type", "message"))
    else:
        text = str(error)
    decision = str(row.get("decision") or "")
    normalized = f"{decision} {text}".casefold()
    if "timeout" in normalized:
        return "mineru_timeout" if stage == "stage04" else f"{stage}_timeout"
    if stage == "stage04":
        return "mineru_parse_failed"
    if stage == "stage01":
        return "document_parse_failed"
    if stage == "stage00":
        return "remote_copy_failed"
    return f"{stage}_infrastructure_failure"
