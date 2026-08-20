from __future__ import annotations

import http.client
import hashlib
import os
import socket
import threading
import urllib.error
from pathlib import Path
from typing import Any, Callable

from src.contracts import canonical_hash, read_json, safe_component, write_json
from src.integrations.llm_client import call_json_chat

ModelCaller = Callable[..., tuple[dict[str, Any], dict[str, Any]]]
REMOTE_API_ROLES = frozenset({"stage05_router", "suitability", "builder", "judge"})
DEFAULT_REMOTE_API_PROXY = "http://httpproxy-headless.kubebrain.svc.pjlab.local:3128"


def is_transient_connection_error(exc: BaseException) -> bool:
    """Return whether an exception represents endpoint infrastructure loss."""

    current: BaseException | None = exc
    seen: set[int] = set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(
            current,
            (
                ConnectionError,
                TimeoutError,
                socket.timeout,
                urllib.error.URLError,
                http.client.RemoteDisconnected,
            ),
        ):
            return True
        message = str(current).casefold()
        if any(
            marker in message
            for marker in (
                "connection refused",
                "remote end closed connection",
                "connection reset",
                "llm http 500",
                "llm http 502",
                "llm http 503",
                "llm http 504",
            )
        ):
            return True
        current = current.__cause__ or current.__context__
    return False


class RoleModelClient:
    """Audited JSON client for one configured model role."""

    def __init__(
        self,
        *,
        role: str,
        config: dict[str, Any],
        cache_root: str | Path,
        caller: ModelCaller = call_json_chat,
    ) -> None:
        self.role = role
        self.config = dict(config)
        self.cache_root = Path(cache_root).expanduser().resolve() / role
        self.cache_root.mkdir(parents=True, exist_ok=True)
        self.caller = caller
        self._semaphore = threading.BoundedSemaphore(max(1, int(self.config.get("workers", 1))))

    @property
    def model(self) -> str:
        return str(self.config["model"])

    def _candidate_configs(
        self, *, selection_key: str = ""
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Return the primary plus the configured fallback candidates.

        ``random_one`` deliberately means one fallback attempt, rather than a
        shuffled list of all fallbacks.  A stable hash distributes papers over
        the fallback pool while keeping a resumed run deterministic.
        """

        candidates = [dict(self.config)]
        fallbacks = list(self.config.get("fallback_models") or [])
        strategy = str(self.config.get("fallback_strategy", "sequential")).strip().lower()
        if strategy in {"random_one", "random_single"} and fallbacks:
            digest = hashlib.sha256(
                f"{self.role}\0{selection_key}".encode("utf-8")
            ).digest()
            selected_index = int.from_bytes(digest[:8], "big") % len(fallbacks)
            selected = dict(self.config)
            selected.update(fallbacks[selected_index])
            selected.pop("fallback_models", None)
            candidates.append(selected)
            return candidates, {
                "strategy": "random_one",
                "pool_size": len(fallbacks),
                "selected_pool_index": selected_index,
                "selected_model": str(selected.get("model") or ""),
            }
        for fallback in fallbacks:
            candidate = dict(self.config)
            candidate.update(dict(fallback))
            candidate.pop("fallback_models", None)
            candidates.append(candidate)
        return candidates, {
            "strategy": "sequential",
            "pool_size": len(fallbacks),
        }

    def call_json(
        self,
        *,
        namespace: str,
        record_id: str,
        prompt_version: str,
        system_prompt: str,
        user_content: str,
        max_tokens: int | None = None,
        thinking: str | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        effective_thinking = self.config.get("thinking") if thinking is None else thinking
        chat_template_kwargs = self.config.get("chat_template_kwargs")
        request_record = {
            "role": self.role,
            "namespace": namespace,
            "record_id": record_id,
            "prompt_version": prompt_version,
            "model": self.model,
            "base_url": self.config["base_url"],
            "system_prompt": system_prompt,
            "user_content": user_content,
            "max_tokens": int(max_tokens or self.config.get("max_tokens", 2048)),
            "thinking": effective_thinking,
            "chat_template_kwargs": chat_template_kwargs,
            "fallback_models": [
                {
                    key: candidate.get(key)
                    for key in (
                        "model",
                        "base_url",
                        "api_key_env",
                        "max_tokens",
                        "thinking",
                        "chat_template_kwargs",
                    )
                }
                for candidate in self.config.get("fallback_models") or []
            ],
            "proxy_enabled": self._proxy_enabled(),
            "fallback_strategy": str(self.config.get("fallback_strategy", "sequential")),
        }
        request_hash = canonical_hash(request_record)
        directory = self.cache_root / safe_component(namespace)
        cache_path = directory / f"{safe_component(record_id)}.{request_hash}.json"
        if self.config.get("cache", True) and cache_path.is_file():
            cached = read_json(cache_path)
            return cached["response"], {**cached["audit"], "cache_hit": True}

        with self._semaphore:
            guard = self.config.get("_managed_service_guard")
            if guard is not None:
                guard.ensure_healthy()
            response, audit = self._call_with_fallbacks(
                system_prompt=system_prompt,
                user_content=user_content,
                max_tokens=max_tokens,
                thinking=effective_thinking,
                guard=guard,
                selection_key=request_hash,
            )
        audit_record = {
            **audit,
            "role": self.role,
            "prompt_version": prompt_version,
            "request_hash": request_hash,
            "cache_hit": False,
        }
        write_json(
            cache_path,
            {"request": request_record, "response": response, "audit": audit_record},
        )
        return response, audit_record

    def _call(
        self,
        *,
        api_key,
        system_prompt,
        user_content,
        max_tokens,
        thinking,
        chat_template_kwargs=None,
        candidate_config=None,
    ):
        config = candidate_config or self.config
        return self.caller(
            model=str(config["model"]),
            base_url=str(config["base_url"]),
            api_key=api_key,
            system_prompt=system_prompt,
            user_content=user_content,
            timeout_seconds=float(config.get("timeout_seconds", 900)),
            max_tokens=int(max_tokens or config.get("max_tokens", 2048)),
            retries=int(config.get("retries", 2)),
            thinking=thinking,
            chat_template_kwargs=chat_template_kwargs,
            proxy_url=self._proxy_url(config),
        )

    def _call_with_fallbacks(
        self,
        *,
        system_prompt: str,
        user_content: str,
        max_tokens: int | None,
        thinking: str | None,
        guard: Any,
        selection_key: str,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        failures: list[dict[str, Any]] = []
        candidates, selection = self._candidate_configs(selection_key=selection_key)
        for index, candidate in enumerate(candidates):
            key_name = str(candidate.get("api_key_env") or "")
            api_key = os.environ.get(key_name, "")
            if not api_key:
                exc: Exception = RuntimeError(
                    f"missing API key environment variable for {self.role}: {key_name}"
                )
                failures.append(self._fallback_failure(candidate, exc))
                if index + 1 < len(candidates):
                    continue
                raise exc
            candidate_thinking = candidate.get("thinking", thinking)
            candidate_kwargs = candidate.get("chat_template_kwargs")
            try:
                response, audit = self._call(
                    api_key=api_key,
                    system_prompt=system_prompt,
                    user_content=user_content,
                    max_tokens=max_tokens,
                    thinking=None if candidate_kwargs is not None else candidate_thinking,
                    chat_template_kwargs=candidate_kwargs,
                    candidate_config=candidate,
                )
            except Exception as exc:
                if guard is not None and is_transient_connection_error(exc):
                    try:
                        guard.recover()
                        response, audit = self._call(
                            api_key=api_key,
                            system_prompt=system_prompt,
                            user_content=user_content,
                            max_tokens=max_tokens,
                            thinking=None if candidate_kwargs is not None else candidate_thinking,
                            chat_template_kwargs=candidate_kwargs,
                            candidate_config=candidate,
                        )
                    except Exception as recovered_exc:
                        exc = recovered_exc
                    else:
                        return response, {
                            **audit,
                            "fallback_used": bool(index),
                            "fallback_index": index,
                            "fallback_selection": selection,
                            "model_failures": failures,
                        }
                failures.append(self._fallback_failure(candidate, exc))
                if index + 1 < len(candidates):
                    continue
                raise RuntimeError(
                    f"all configured models failed for role {self.role}: "
                    + "; ".join(
                        f"{row['model']}: {row['error_type']}" for row in failures
                    )
                ) from exc
            return response, {
                **audit,
                "fallback_used": bool(index),
                "fallback_index": index,
                "fallback_selection": selection,
                "model_failures": failures,
            }
        raise RuntimeError(f"no model candidates configured for role {self.role}")

    @staticmethod
    def _fallback_failure(candidate: dict[str, Any], exc: Exception) -> dict[str, Any]:
        return {
            "model": str(candidate.get("model") or ""),
            "base_url": str(candidate.get("base_url") or ""),
            "error_type": type(exc).__name__,
            "message": str(exc)[:1000],
        }

    def _proxy_enabled(self) -> bool:
        return bool(self.config.get("use_proxy", self.role in REMOTE_API_ROLES))

    def _proxy_url(self, config: dict[str, Any] | None = None) -> str:
        value = config or self.config
        if not bool(value.get("use_proxy", self.role in REMOTE_API_ROLES)):
            # An empty string tells the lower-level client to disable both
            # explicit and environment-derived proxies for local endpoints.
            return ""
        env_name = str(value.get("proxy_url_env") or "HTTPS_PROXY")
        candidates = [
            os.environ.get(env_name),
            os.environ.get(env_name.lower()),
            os.environ.get("HTTPS_PROXY"),
            os.environ.get("https_proxy"),
            os.environ.get("HTTP_PROXY"),
            os.environ.get("http_proxy"),
            value.get("proxy_url"),
        ]
        return str(next((value for value in candidates if value), DEFAULT_REMOTE_API_PROXY))
