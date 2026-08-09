from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Any, Callable

from src.integrations.llm_client import call_json_chat
from src.v2.contracts import canonical_hash, read_json, safe_component, write_json

ModelCaller = Callable[..., tuple[dict[str, Any], dict[str, Any]]]
REMOTE_API_ROLES = frozenset({"suitability", "builder", "judge"})
DEFAULT_REMOTE_API_PROXY = "http://httpproxy-headless.kubebrain.svc.pjlab.local:3128"


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

    def call_json(
        self,
        *,
        namespace: str,
        record_id: str,
        prompt_version: str,
        system_prompt: str,
        user_content: str,
        max_tokens: int | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
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
            "thinking": self.config.get("thinking"),
            "proxy_enabled": self._proxy_enabled(),
        }
        request_hash = canonical_hash(request_record)
        directory = self.cache_root / safe_component(namespace)
        cache_path = directory / f"{safe_component(record_id)}.{request_hash}.json"
        if self.config.get("cache", True) and cache_path.is_file():
            cached = read_json(cache_path)
            return cached["response"], {**cached["audit"], "cache_hit": True}

        key_name = str(self.config.get("api_key_env") or "")
        api_key = os.environ.get(key_name, "")
        if not api_key:
            raise RuntimeError(f"missing API key environment variable for {self.role}: {key_name}")
        with self._semaphore:
            response, audit = self.caller(
                model=self.model,
                base_url=str(self.config["base_url"]),
                api_key=api_key,
                system_prompt=system_prompt,
                user_content=user_content,
                timeout_seconds=float(self.config.get("timeout_seconds", 900)),
                max_tokens=int(max_tokens or self.config.get("max_tokens", 2048)),
                retries=int(self.config.get("retries", 2)),
                thinking=self.config.get("thinking"),
                proxy_url=self._proxy_url(),
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

    def _proxy_enabled(self) -> bool:
        return bool(self.config.get("use_proxy", self.role in REMOTE_API_ROLES))

    def _proxy_url(self) -> str:
        if not self._proxy_enabled():
            # An empty string tells the lower-level client to disable both
            # explicit and environment-derived proxies for local endpoints.
            return ""
        env_name = str(self.config.get("proxy_url_env") or "HTTPS_PROXY")
        candidates = [
            os.environ.get(env_name),
            os.environ.get(env_name.lower()),
            os.environ.get("HTTPS_PROXY"),
            os.environ.get("https_proxy"),
            os.environ.get("HTTP_PROXY"),
            os.environ.get("http_proxy"),
            self.config.get("proxy_url"),
        ]
        return str(next((value for value in candidates if value), DEFAULT_REMOTE_API_PROXY))
