"""Finite, journaled Judge requests. Raw responses are saved before interpretation."""
from __future__ import annotations

import json
import math
import time
from datetime import datetime, timezone
from dataclasses import asdict, dataclass
from pathlib import Path

from chemistry_toolbox.src.recovery_io import atomic_json
from .policies import _parse_judge_json, parse_judge_response, JudgeContractError
from ..execution.provider_errors import normalize_error
from .packing import pack_prompt


@dataclass(frozen=True)
class ScoringBudget:
    # Character defaults accommodate the measured 322k saved-run evidence view
    # plus task/trace context. They do not claim a provider context-window size.
    request_max_chars: int = 500000
    total_request_max_chars: int = 1500000
    max_requests: int = 6
    max_output_tokens: int = 8192
    total_output_tokens: int = 49152
    max_read_items: int = 6
    max_read_chars: int = 24000
    max_input_tokens: int | None = None
    total_input_tokens: int | None = None
    context_window_tokens: int | None = None
    version: str = "scoring-budget-1"

    def __post_init__(self):
        for key, value in asdict(self).items():
            if key != "version" and value is not None and (isinstance(value, bool) or not isinstance(value, int) or value <= 0):
                raise ValueError(f"Invalid scoring budget: {key}")


class ScoringStop(Exception):
    def __init__(self, status, reason, provider_error=None):
        super().__init__(reason)
        self.status, self.reason = status, reason
        self.provider_error = provider_error


def judge_request_payload(prompt, system, maximum, config):
    model, effort = config["judge_model"], config.get("reasoning_effort", "high")
    if config.get("wire_api") == "responses":
        return {"model": model, "instructions": system, "input": prompt, "reasoning": {"effort": effort},
                "max_output_tokens": maximum, "store": False}
    return {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "reasoning_effort": effort, "max_completion_tokens": maximum}


def usage_summary(responses):
    fields = ("prompt_tokens", "completion_tokens", "total_tokens", "cached_input_tokens", "reasoning_output_tokens")
    result = {name: 0 for name in fields}
    for response in responses:
        usage = response.get("_judge_usage") or {}
        for name in fields:
            value = usage.get(name)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
                result[name] = None
            elif result[name] is not None:
                result[name] += value
    return {**result, "request_count": len(responses),
            "accounting_status": "complete" if all(result[k] is not None for k in fields[:3]) else "partial"}


def recorded_usage(directory):
    """Count every recorded request, even if replay accepts an earlier verdict."""
    return usage_summary([json.loads(p.read_text()) for p in sorted((Path(directory) / "requests").glob("*.response.json"))])


def run_judge(directory, payload, system, *, budget, call, validate, read, retry_in_doubt=False, resume=False,
              config=None, unresolved_rule_policy="block"):
    """Replay persisted responses, then continue a bounded protocol if necessary."""
    directory = Path(directory)
    requests = directory / "requests"
    requests.mkdir(exist_ok=True)
    followups, seen_reads = [], set()
    cache = json.loads((directory / "reads.json").read_text()) if (directory / "reads.json").is_file() else {}
    total_chars, reserved_output, input_accounted, repairs = 0, 0, 0, 0
    protocol = (config or {}).get("judge_protocol_version", 1)
    max_repairs = (config or {}).get("max_format_repairs", 2 if protocol >= 3 else 1)
    previous_error = None
    first = requests / "0001.request.json"
    if resume and first.exists():
        system = json.loads(first.read_text())["request"]["system"]
    for number in range(1, budget.max_requests + 1):
        request_path = requests / f"{number:04d}.request.json"
        response_path = requests / f"{number:04d}.response.json"
        def wire_text(prompt):
            request = {"system": system, "prompt": prompt, "max_output_tokens": budget.max_output_tokens}
            envelope = judge_request_payload(prompt, system, budget.max_output_tokens, config) if config else request
            return json.dumps(envelope, ensure_ascii=False)
        char_limit = min(budget.request_max_chars, budget.total_request_max_chars - total_chars)
        def fits(prompt):
            wire = wire_text(prompt)
            tokens = len(wire.encode("utf-8"))
            return (len(wire) <= char_limit
                    and (not budget.max_input_tokens or tokens <= budget.max_input_tokens)
                    and (not budget.total_input_tokens or tokens <= budget.total_input_tokens - input_accounted)
                    and (not budget.context_window_tokens or tokens + budget.max_output_tokens <= budget.context_window_tokens))
        if request_path.exists() and resume:
            request = json.loads(request_path.read_text())["request"]
            prompt, system = request["prompt"], request["system"]
        else:
            view = {**payload, "judge_budget": {"requests_remaining_including_this": budget.max_requests - number + 1,
                    "request_max_chars": char_limit, "total_request_chars_remaining_before_this": budget.total_request_max_chars - total_chars,
                    "format_repairs_remaining": max(0, max_repairs - repairs)}} if protocol >= 3 else payload
            prompt = (pack_prompt(view, followups, fits=fits) if (config or {}).get("packing_version", 2) >= 2
                      else json.dumps({**payload, "followups": followups}, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            request = {"system": system, "prompt": prompt, "max_output_tokens": budget.max_output_tokens}
        # Includes the serialized envelope and a conservative token upper bound.
        envelope = judge_request_payload(prompt, system, budget.max_output_tokens, config) if config else request
        wire = json.dumps(envelope, ensure_ascii=False)
        chars, estimated_tokens = len(wire), len(wire.encode("utf-8"))
        if (chars > budget.request_max_chars or total_chars + chars > budget.total_request_max_chars
                or reserved_output + budget.max_output_tokens > budget.total_output_tokens
                or (budget.max_input_tokens and estimated_tokens > budget.max_input_tokens)
                or (budget.total_input_tokens and input_accounted + estimated_tokens > budget.total_input_tokens)
                or (budget.context_window_tokens and estimated_tokens + budget.max_output_tokens > budget.context_window_tokens)):
            atomic_json(directory / "budget_diagnostic.json", {"request_number": number, "request_chars": chars,
                        "request_limit": budget.request_max_chars, "total_chars_if_sent": total_chars + chars,
                        "total_limit": budget.total_request_max_chars, "input_tokens_upper_estimate": estimated_tokens,
                        "sent": False})
            raise ScoringStop("needs_review", "judge_request_budget_exhausted")
        total_chars += chars
        if request_path.exists() and json.loads(request_path.read_text())["request"] != request:
            raise ValueError("Saved Judge request differs; create a new scoring version")
        journal = {"request": request, "input_characters": chars, "input_tokens_upper_estimate": estimated_tokens,
                   "output_tokens_reserved": budget.max_output_tokens, "usage_estimated": True}
        replay = response_path.exists()
        if replay:
            response = json.loads(response_path.read_text())
        else:
            if request_path.exists():
                response = {"transport_error": "request_without_persisted_response", "status": "in_doubt", "_judge_usage": None}
                atomic_json(response_path, response)
                input_accounted += estimated_tokens
                reserved_output += budget.max_output_tokens
                atomic_json(directory / "state.json", {"status": "in_doubt", "judge_usage": recorded_usage(directory)})
                if retry_in_doubt:
                    continue
                raise ScoringStop("in_doubt", "request_without_persisted_response")
            atomic_json(request_path, journal)
            atomic_json(directory / "state.json", {"status": "judging", "request_number": number,
                        "request_characters": total_chars, "judge_usage": recorded_usage(directory),
                        "retry_in_doubt": retry_in_doubt})
            started_at, started = datetime.now(timezone.utc).isoformat(), time.monotonic()
            try:
                response = call(prompt, system, budget.max_output_tokens)
            except Exception as exc:
                ambiguous = isinstance(exc, (TimeoutError, ConnectionError)) or type(exc).__name__ in {"APITimeoutError", "APIConnectionError"}
                error = normalize_error(exc, source="judge", event_ref=str(response_path))
                response = {"transport_error": error["message"], "provider_error": error,
                            "status": "in_doubt" if ambiguous else "suspended_infrastructure", "_judge_usage": None,
                            "exception_type": type(exc).__name__}
                if getattr(exc, "judge_transport", None):
                    response["transport"] = exc.judge_transport
            if not isinstance(response, dict):
                response = {"raw_text": str(response)}
            response.setdefault("transport", {"started_at": started_at, "finished_at": datetime.now(timezone.utc).isoformat(),
                                                "duration_seconds": time.monotonic() - started,
                                                "timeout_seconds": (config or {}).get("timeout_seconds")})
            atomic_json(response_path, response)
        actual_input = (response.get("_judge_usage") or {}).get("prompt_tokens")
        input_accounted += actual_input if isinstance(actual_input, int) and not isinstance(actual_input, bool) and actual_input >= 0 else estimated_tokens
        actual_output = (response.get("_judge_usage") or {}).get("completion_tokens")
        reserved_output += actual_output if isinstance(actual_output, int) and not isinstance(actual_output, bool) and actual_output >= 0 else budget.max_output_tokens
        atomic_json(directory / "state.json", {"status": "interpreting", "request_number": number,
                    "request_characters": total_chars, "output_tokens_accounted": reserved_output, "input_tokens_accounted": input_accounted,
                    "judge_usage": recorded_usage(directory)})
        if response.get("transport_error"):
            if replay and resume and (response["status"] == "suspended_infrastructure" or retry_in_doubt):
                continue
            raise ScoringStop(response["status"], response["transport_error"], response.get("provider_error"))
        try:
            diagnostics = {}
            value = ((parse_judge_response(response, diagnostics=diagnostics) if protocol >= 3 else _parse_judge_json(response["raw_text"]))
                     if "raw_text" in response else response)
            if diagnostics:
                atomic_json(requests / f"{number:04d}.interpretation.json", diagnostics)
            if value.get("type") == "needs_review" and unresolved_rule_policy == "judge_disposition":
                if not isinstance(value.get("rationale"), str) or not value["rationale"].strip():
                    raise ValueError("needs_review requires a rationale")
                citations = value.get("citations")
                if not isinstance(citations, list) or not citations:
                    raise ValueError("needs_review requires evidence citations")
                for citation in citations:
                    read(citation)
                atomic_json(directory / "judge_output.json", value)
                raise ScoringStop("needs_review", value["rationale"])
            if value.get("type") == "evidence_request":
                reads = value.get("reads")
                if not isinstance(reads, list) or not 1 <= len(reads) <= budget.max_read_items:
                    raise ValueError("invalid number of evidence reads")
                pages, new = [], False
                for item in reads:
                    if not isinstance(item, dict):
                        raise ValueError("evidence read must be an object")
                    key = json.dumps(item, sort_keys=True)
                    new = new or key not in seen_reads
                    seen_reads.add(key)
                    if key not in cache:
                        try:
                            limit = item.get("max_chars", budget.max_read_chars)
                            if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= budget.max_read_chars:
                                raise ValueError("read exceeds configured limit")
                            page = read({**item, "max_chars": limit})
                            if len(json.dumps(page, ensure_ascii=False)) > budget.max_read_chars * 2:
                                raise ValueError("read response exceeds configured limit; narrow the request")
                            cache[key] = page
                        except (ValueError, OSError, KeyError, TypeError) as exc:
                            cache[key] = {"ref": item.get("ref"), "error": str(exc)}
                    pages.append(cache[key])
                if not new:
                    raise ScoringStop("needs_review", "repeated_evidence_request_without_progress")
                followups.append({"request": value, "evidence": pages})
                atomic_json(directory / "reads.json", cache)
                continue
            validate(value)
            unresolved = any(r.get("assessment") == "unresolved" for r in value.get("rule_assessments", []))
            disposition = value.get("unresolved_disposition")
            if unresolved and not (unresolved_rule_policy == "judge_disposition" and disposition == "scorable"):
                atomic_json(directory / "judge_output.json", value)
                raise ScoringStop("needs_review", "unresolved_authored_rules")
            return {**value, "_judge_usage": recorded_usage(directory), "_judge_model": response.get("_judge_model")}
        except (ValueError, TypeError, KeyError) as exc:
            error = str(exc)
            if protocol >= 3:
                diagnostic = {"status": "invalid_contract", "error": error[:7000], "repair_count": repairs}
                if isinstance(exc, JudgeContractError):
                    diagnostic.update(errors=exc.errors, errors_truncated=exc.truncated)
                atomic_json(requests / f"{number:04d}.interpretation.json", diagnostic)
            content = response.get("raw_text", {k: v for k, v in response.items() if not k.startswith("_") and k != "transport"})
            fingerprint = (json.dumps(content, ensure_ascii=False, sort_keys=True), error)
            if repairs >= max_repairs or fingerprint == previous_error:
                raise ScoringStop("judge_error", str(exc)) from exc
            previous_error = fingerprint
            repairs += 1
            if protocol >= 3:
                followups = [v for v in followups if "format_error" not in v]
            followups.append({"format_error": str(exc), "invalid_response": response.get("raw_text", response),
                              "instruction": "Repair the listed contract errors and return a complete response. Preserve other valid citations. You may request existing evidence before giving a verdict."})
    raise ScoringStop("needs_review", "judge_request_count_exhausted")
