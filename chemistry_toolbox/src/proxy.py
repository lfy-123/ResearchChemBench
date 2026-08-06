"""Local proxy configuration for PubChem network access."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

from .paths import PROJECT_ROOT


PROXY_URL_VARIABLES = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)
PROXY_ENVIRONMENT_VARIABLES = (
    *PROXY_URL_VARIABLES,
    "NO_PROXY",
    "no_proxy",
)
PUBCHEM_PROXY_URL_VARIABLE = "RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL"
PUBCHEM_NO_PROXY_VARIABLE = "RESEARCHCHEMBENCH_PUBCHEM_NO_PROXY"
PUBCHEM_PROXY_MODE_VARIABLE = "RESEARCHCHEMBENCH_PUBCHEM_PROXY_MODE"
_DISABLED_PROXY_MODES = {"0", "false", "no", "off", "disabled"}


def configure_pubchem_proxy_environment(
    config_path: Path | None = None,
) -> dict[str, Any]:
    """Load only proxy variables from the ignored local environment file.

    An already exported proxy (for example from ``proxy_on``) always wins. The
    proxy URL is never returned, so callers can safely include this status in
    diagnostics and provenance.
    """

    active = sorted(
        name for name in PROXY_URL_VARIABLES if os.environ.get(name, "").strip()
    )
    if active:
        return {"enabled": True, "source": "environment", "variables": active}

    mode = os.environ.get(PUBCHEM_PROXY_MODE_VARIABLE, "auto").strip().lower()
    if mode in _DISABLED_PROXY_MODES:
        return {"enabled": False, "source": "disabled", "variables": []}

    path = config_path or PROJECT_ROOT / "config.local.env"
    try:
        values = dotenv_values(path) if path.is_file() else {}
    except OSError:
        values = {}

    configured_url = os.environ.get(PUBCHEM_PROXY_URL_VARIABLE, "").strip()
    source = "pubchem_environment" if configured_url else "none"
    if not configured_url:
        configured_url = str(values.get(PUBCHEM_PROXY_URL_VARIABLE) or "").strip()
        if configured_url:
            source = "config.local.env"

    if configured_url:
        for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
            os.environ.setdefault(name, configured_url)
        configured_no_proxy = (
            os.environ.get(PUBCHEM_NO_PROXY_VARIABLE, "").strip()
            or str(values.get(PUBCHEM_NO_PROXY_VARIABLE) or "").strip()
        )
        if configured_no_proxy:
            os.environ.setdefault("NO_PROXY", configured_no_proxy)
    elif config_path is not None:
        for name in PROXY_ENVIRONMENT_VARIABLES:
            value = values.get(name)
            if value is not None and str(value).strip() and not os.environ.get(name):
                os.environ[name] = str(value).strip()
        if any(os.environ.get(name, "").strip() for name in PROXY_URL_VARIABLES):
            source = "config.local.env"

    active = sorted(
        name for name in PROXY_URL_VARIABLES if os.environ.get(name, "").strip()
    )
    return {
        "enabled": bool(active),
        "source": source if active else "none",
        "variables": active,
    }
