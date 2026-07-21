from __future__ import annotations

import os

from researchchem_toolbox import proxy
from researchchem_toolbox.backends import data


def _clear_proxy_environment(monkeypatch) -> None:
    for name in proxy.PROXY_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv(proxy.PUBCHEM_PROXY_URL_VARIABLE, raising=False)
    monkeypatch.delenv(proxy.PUBCHEM_NO_PROXY_VARIABLE, raising=False)
    monkeypatch.delenv(proxy.PUBCHEM_PROXY_MODE_VARIABLE, raising=False)


def test_existing_proxy_environment_takes_priority(tmp_path, monkeypatch):
    _clear_proxy_environment(monkeypatch)
    monkeypatch.setenv("HTTPS_PROXY", "http://already-configured.example:3128")
    config = tmp_path / "config.local.env"
    config.write_text("HTTPS_PROXY=http://local-config.example:8080\n", encoding="utf-8")

    status = proxy.configure_pubchem_proxy_environment(config)

    assert status == {
        "enabled": True,
        "source": "environment",
        "variables": ["HTTPS_PROXY"],
    }
    assert os.environ["HTTPS_PROXY"] == "http://already-configured.example:3128"


def test_local_config_loads_only_proxy_values(tmp_path, monkeypatch):
    _clear_proxy_environment(monkeypatch)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = tmp_path / "config.local.env"
    config.write_text(
        "RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL=http://proxy.example:3128\n"
        "OPENAI_API_KEY=must-not-be-loaded\n",
        encoding="utf-8",
    )

    status = proxy.configure_pubchem_proxy_environment(config)

    assert status["enabled"] is True
    assert status["source"] == "config.local.env"
    assert status["variables"] == ["ALL_PROXY", "HTTPS_PROXY", "HTTP_PROXY"]
    assert "OPENAI_API_KEY" not in os.environ


def test_local_proxy_loading_can_be_disabled(tmp_path, monkeypatch):
    _clear_proxy_environment(monkeypatch)
    monkeypatch.setenv(proxy.PUBCHEM_PROXY_MODE_VARIABLE, "off")
    config = tmp_path / "config.local.env"
    config.write_text(
        "RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL=http://proxy.example:3128\n",
        encoding="utf-8",
    )

    status = proxy.configure_pubchem_proxy_environment(config)

    assert status == {"enabled": False, "source": "disabled", "variables": []}
    assert "HTTPS_PROXY" not in os.environ


def test_namespaced_proxy_environment_is_mapped_for_pubchem(monkeypatch):
    _clear_proxy_environment(monkeypatch)
    monkeypatch.setenv(
        proxy.PUBCHEM_PROXY_URL_VARIABLE,
        "http://pubchem-only.example:3128",
    )

    status = proxy.configure_pubchem_proxy_environment()

    assert status["enabled"] is True
    assert status["source"] == "pubchem_environment"
    assert os.environ["HTTP_PROXY"] == "http://pubchem-only.example:3128"
    assert os.environ["HTTPS_PROXY"] == "http://pubchem-only.example:3128"
    assert os.environ["ALL_PROXY"] == "http://pubchem-only.example:3128"


def test_default_project_config_does_not_import_generic_proxy(tmp_path, monkeypatch):
    _clear_proxy_environment(monkeypatch)
    config = tmp_path / "config.local.env"
    config.write_text("HTTPS_PROXY=http://generic.example:3128\n", encoding="utf-8")
    monkeypatch.setattr(proxy, "PROJECT_ROOT", tmp_path)

    status = proxy.configure_pubchem_proxy_environment()

    assert status == {"enabled": False, "source": "none", "variables": []}
    assert "HTTPS_PROXY" not in os.environ


def test_pubchem_backend_configures_proxy_before_dispatch(monkeypatch):
    calls = []
    monkeypatch.setattr(
        data,
        "configure_pubchem_proxy_environment",
        lambda: calls.append("configured") or {"enabled": True},
    )
    monkeypatch.setattr(data, "_pubchem", lambda _request: {"status": "success"})

    result = data.execute("search_compounds", "pubchem", {})

    assert result["status"] == "success"
    assert calls == ["configured"]
