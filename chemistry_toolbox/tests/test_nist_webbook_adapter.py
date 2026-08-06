from __future__ import annotations

import httpx
import pytest

from chemistry_toolbox.src.backends import data


class _FakeResponse:
    def __init__(self, url: str, html: str):
        self.url = httpx.URL(url)
        self.text = html
        self.content = html.encode("utf-8")
        self.headers = {"content-type": "text/html; charset=UTF-8"}

    def raise_for_status(self) -> None:
        return None


def test_nist_webbook_name_lookup_uses_only_the_official_bounded_cgi(monkeypatch):
    captured = {}
    html = """
    <html><body><h1>Search Results</h1><ul>
      <li><a href="/cgi/cbook.cgi?ID=C7732185&amp;Units=SI">Water</a>
          (H<sub>2</sub>O)</li>
    </ul></body></html>
    """

    def fake_get(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return _FakeResponse(
            "https://webbook.nist.gov/cgi/cbook.cgi?Name=water&Units=SI",
            html,
        )

    monkeypatch.setattr(data.httpx, "get", fake_get)
    result = data.execute(
        "lookup_nist_webbook_species",
        "nist_webbook",
        {
            "inputs": {"query": {"identifier": "water", "namespace": "name"}},
            "method_spec": {},
            "action_settings": {"units": "SI", "max_records": 3},
        },
    )

    assert result["status"] == "success"
    assert captured["url"] == "https://webbook.nist.gov/cgi/cbook.cgi"
    assert captured["params"] == {"Units": "SI", "Name": "water"}
    assert captured["follow_redirects"] is True
    assert result["result"]["count"] == 1
    record = result["result"]["records"][0]
    assert record["webbook_id"] == "C7732185"
    assert record["name"] == "Water"
    assert record["formula"] == "H2O"
    assert "no REST/JSON API" in result["result"]["interface_scope"]


def test_nist_webbook_cas_lookup_extracts_only_general_species_metadata(monkeypatch):
    html = """
    <html><body><h1>Water</h1><ul>
      <li><strong>Formula</strong>: H<sub>2</sub>O</li>
      <li><strong>Molecular weight</strong>: 18.0153</li>
      <li><strong>CAS Registry Number</strong>: 7732-18-5</li>
      <li><strong>IUPAC Standard InChI</strong>: InChI=1S/H2O/h1H2</li>
      <li><strong>IUPAC Standard InChIKey</strong>: XLYOFNOQVPJJNP-UHFFFAOYSA-N</li>
    </ul><h2>Gas phase thermochemistry data</h2></body></html>
    """
    monkeypatch.setattr(
        data.httpx,
        "get",
        lambda _url, **_kwargs: _FakeResponse(
            "https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Units=SI",
            html,
        ),
    )
    result = data.execute(
        "lookup_nist_webbook_species",
        "nist_webbook",
        {
            "inputs": {
                "query": {"identifier": "7732-18-5", "namespace": "cas"}
            },
            "method_spec": {},
            "action_settings": {"units": "SI"},
        },
    )
    record = result["result"]["records"][0]
    assert record == {
        "webbook_id": "C7732185",
        "name": "Water",
        "formula": "H2O",
        "molecular_weight": 18.0153,
        "cas_registry_number": "7732-18-5",
        "inchi": "InChI=1S/H2O/h1H2",
        "inchi_key": "XLYOFNOQVPJJNP-UHFFFAOYSA-N",
        "url": "https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Units=SI",
    }
    assert result["result"]["available_page_sections"] == [
        "Gas phase thermochemistry data"
    ]


def test_nist_webbook_formula_choices_are_explicit_and_patterns_are_rejected():
    base = {
        "inputs": {"query": {"identifier": "H2O", "namespace": "formula"}},
        "method_spec": {},
        "action_settings": {"units": "SI"},
    }
    with pytest.raises(ValueError, match="match_isotopes"):
        data._nist_webbook(base)

    wildcard = {
        **base,
        "inputs": {"query": {"identifier": "CH*", "namespace": "formula"}},
        "action_settings": {
            "units": "SI",
            "match_isotopes": False,
            "exclude_ions": True,
        },
    }
    with pytest.raises(ValueError, match="exact"):
        data._nist_webbook(wildcard)
