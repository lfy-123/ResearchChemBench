"""External chemistry data actions."""

from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import httpx

from .common import module_version, request_parts, success, unavailable, unsupported


ACTIONS = {
    "search_compounds", "search_protein_structures", "search_materials",
    "search_catalysis_records", "lookup_nist_webbook_species",
}


_NIST_WEBBOOK_ENDPOINT = "https://webbook.nist.gov/cgi/cbook.cgi"
_CAS_NUMBER = re.compile(r"^\d{2,7}-\d{2}-\d$")
_EXACT_FORMULA = re.compile(r"^[A-Za-z0-9()[\]+.\-]+$")


def _compact_html_text(parts: list[str]) -> str:
    return re.sub(r"\s+", " ", "".join(parts)).strip()


class _NISTWebBookHTMLParser(HTMLParser):
    """Extract only species identifiers and general metadata from one CGI page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self.list_items: list[dict[str, Any]] = []
        self.headings: list[str] = []
        self._link_href: str | None = None
        self._link_text: list[str] = []
        self._list_text: list[str] | None = None
        self._list_links: list[dict[str, str]] | None = None
        self._heading_tag: str | None = None
        self._heading_text: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "a":
            self._link_href = attributes.get("href")
            self._link_text = []
        elif tag == "li":
            self._list_text = []
            self._list_links = []
        elif tag in {"h1", "h2", "h3"}:
            self._heading_tag = tag
            self._heading_text = []
        elif tag == "br":
            if self._list_text is not None:
                self._list_text.append(" ")
            if self._link_href is not None:
                self._link_text.append(" ")
            if self._heading_tag is not None:
                self._heading_text.append(" ")

    def handle_data(self, data: str) -> None:
        if self._list_text is not None:
            self._list_text.append(data)
        if self._link_href is not None:
            self._link_text.append(data)
        if self._heading_tag is not None:
            self._heading_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._link_href is not None:
            record = {
                "href": self._link_href,
                "text": _compact_html_text(self._link_text),
            }
            self.links.append(record)
            if self._list_links is not None:
                self._list_links.append(record)
            self._link_href = None
            self._link_text = []
        elif tag == "li" and self._list_text is not None:
            self.list_items.append(
                {
                    "text": _compact_html_text(self._list_text),
                    "links": list(self._list_links or []),
                }
            )
            self._list_text = None
            self._list_links = None
        elif tag == self._heading_tag:
            value = _compact_html_text(self._heading_text)
            if value:
                self.headings.append(value)
            self._heading_tag = None
            self._heading_text = []


def _nist_general_metadata(parser: _NISTWebBookHTMLParser) -> dict[str, Any]:
    fields = {
        "formula": "Formula:",
        "molecular_weight": "Molecular weight:",
        "cas_registry_number": "CAS Registry Number:",
        "inchi": "IUPAC Standard InChI:",
        "inchi_key": "IUPAC Standard InChIKey:",
    }
    result: dict[str, Any] = {}
    for item in parser.list_items:
        text = str(item["text"])
        for key, prefix in fields.items():
            if text.startswith(prefix):
                value = text[len(prefix) :].strip()
                if key == "molecular_weight":
                    try:
                        result[key] = float(value)
                    except ValueError:
                        result[key] = value
                else:
                    result[key] = value
    return result


def _nist_species_records(
    parser: _NISTWebBookHTMLParser,
    *,
    page_url: str,
    max_records: int,
) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for item in parser.list_items:
        summary = str(item["text"])
        for link in item["links"]:
            absolute = urljoin(page_url, str(link["href"]))
            parsed = urlparse(absolute)
            if parsed.hostname != "webbook.nist.gov" or parsed.path != "/cgi/cbook.cgi":
                continue
            webbook_id = str((parse_qs(parsed.query).get("ID") or [""])[0])
            if not webbook_id or webbook_id in records:
                continue
            formula_match = re.search(r"\(([^()]*)\)\s*$", summary)
            records[webbook_id] = {
                "webbook_id": webbook_id,
                "name": str(link["text"]) or None,
                "formula": formula_match.group(1) if formula_match else None,
                "summary": summary,
                "url": absolute,
            }
            if len(records) >= max_records:
                return list(records.values())
    return list(records.values())


def _nist_webbook(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    query = inputs["query"]
    if not isinstance(query, dict):
        raise ValueError(
            "NIST WebBook query must be {identifier: ..., namespace: cas|name|formula}"
        )
    extra_query = sorted(set(query) - {"identifier", "namespace"})
    if extra_query:
        raise ValueError(f"Unknown NIST WebBook query fields: {extra_query}")
    identifier = str(query.get("identifier") or "").strip()
    namespace = str(query.get("namespace") or "").strip().lower()
    if namespace not in {"cas", "name", "formula"}:
        raise ValueError("NIST WebBook namespace must be cas, name, or formula")
    if not identifier or len(identifier) > 160 or any(ord(char) < 32 for char in identifier):
        raise ValueError("NIST WebBook identifier must contain 1 to 160 printable characters")

    units = str(settings.get("units") or "").strip().upper()
    if units not in {"SI", "CAL"}:
        raise ValueError("NIST WebBook units must be explicitly set to SI or CAL")
    max_records = int(settings.get("max_records", 10))
    if max_records < 1 or max_records > 20:
        raise ValueError("NIST WebBook max_records must be between 1 and 20")
    timeout = float(settings.get("timeout_seconds", 30))
    if timeout < 1 or timeout > 60:
        raise ValueError("NIST WebBook timeout_seconds must be between 1 and 60")

    parameters: dict[str, Any] = {"Units": units}
    if namespace == "cas":
        if not _CAS_NUMBER.fullmatch(identifier):
            raise ValueError("NIST WebBook CAS query requires a dashed CAS registry number")
        parameters["ID"] = "C" + identifier.replace("-", "")
    elif namespace == "name":
        if "*" in identifier:
            raise ValueError("Pattern searches are not exposed by this bounded single-species Action")
        parameters["Name"] = identifier
    else:
        if not _EXACT_FORMULA.fullmatch(identifier) or any(
            value in identifier for value in ("*", "?")
        ):
            raise ValueError("Formula queries must be exact and cannot contain wildcards")
        parameters["Formula"] = identifier
        for setting, parameter in (
            ("match_isotopes", "MatchIso"),
            ("exclude_ions", "NoIon"),
        ):
            if setting not in settings or not isinstance(settings[setting], bool):
                raise ValueError(
                    f"Formula queries require explicit boolean action_settings.{setting}"
                )
            if settings[setting]:
                parameters[parameter] = "on"

    response = httpx.get(
        _NIST_WEBBOOK_ENDPOINT,
        params=parameters,
        headers={
            "Accept": "text/html",
            "User-Agent": "ResearchChemBench/1.0 bounded-single-species-query",
        },
        timeout=timeout,
        follow_redirects=True,
    )
    response.raise_for_status()
    final_url = str(response.url)
    parsed_url = urlparse(final_url)
    if parsed_url.hostname != "webbook.nist.gov" or parsed_url.path != "/cgi/cbook.cgi":
        raise RuntimeError("NIST WebBook response redirected outside the official CGI endpoint")
    content = response.content
    if len(content) > 2 * 1024 * 1024:
        raise RuntimeError("NIST WebBook response exceeds the 2 MiB bounded-response limit")
    content_type = response.headers.get("content-type", "").lower()
    if "html" not in content_type:
        raise RuntimeError(f"NIST WebBook returned unexpected content type: {content_type}")

    parser = _NISTWebBookHTMLParser()
    parser.feed(response.text)
    records = _nist_species_records(
        parser, page_url=final_url, max_records=max_records
    )
    general = _nist_general_metadata(parser)
    response_id = str((parse_qs(parsed_url.query).get("ID") or [""])[0])
    if general and not records:
        headings = [
            value
            for value in parser.headings
            if value not in {"NIST Chemistry WebBook", "Search Results"}
        ]
        records = [
            {
                "webbook_id": response_id or None,
                "name": headings[0] if headings else None,
                **general,
                "url": final_url,
            }
        ]
    elif len(records) == 1 and general:
        records[0].update(general)

    generic_headings = {
        "NIST Chemistry WebBook",
        "Search Results",
        *(str(record.get("name")) for record in records),
    }
    available_sections = [
        heading for heading in parser.headings if heading not in generic_headings
    ]
    return success(
        {
            "query": {"identifier": identifier, "namespace": namespace},
            "units": units,
            "count": len(records),
            "records": records[:max_records],
            "available_page_sections": available_sections,
            "request_url": _NIST_WEBBOOK_ENDPOINT + "?" + urlencode(parameters),
            "interface_scope": (
                "Official parameterized CGI, one bounded species lookup; no REST/JSON "
                "API, bulk crawl, wildcard name/formula search, or table mirroring."
            ),
            "citation": "NIST Chemistry WebBook, SRD 69, DOI 10.18434/T4D303",
            "rights_url": (
                "https://www.nist.gov/open/copyright-fair-use-and-licensing-"
                "statements-srd-data-software-and-technical-series-publications"
            ),
        },
        backend_version=module_version("httpx"),
    )


def _pubchem(request: dict[str, Any]) -> dict[str, Any]:
    import pubchempy as pcp

    inputs, _method, settings = request_parts(request)
    query = inputs["query"]
    if isinstance(query, dict):
        identifier = str(query["identifier"])
        namespace = str(query.get("namespace", settings.get("namespace", "name")))
    else:
        identifier = str(query)
        namespace = str(settings.get("namespace", "name"))
    allowed = {"name", "cid", "smiles", "inchi", "inchikey", "formula"}
    if namespace not in allowed:
        raise ValueError(f"PubChem namespace must be one of {sorted(allowed)}")
    limit = int(settings.get("max_records", 10))
    if limit < 1 or limit > 100:
        raise ValueError("max_records must be between 1 and 100")
    compounds = pcp.get_compounds(identifier, namespace)[:limit]
    records = [
        {
            "cid": compound.cid,
            "canonical_smiles": compound.canonical_smiles,
            "isomeric_smiles": compound.isomeric_smiles,
            "inchi": compound.inchi,
            "inchikey": compound.inchikey,
            "molecular_formula": compound.molecular_formula,
            "molecular_weight": compound.molecular_weight,
            "iupac_name": compound.iupac_name,
        }
        for compound in compounds
    ]
    return success(
        {"query": {"identifier": identifier, "namespace": namespace}, "count": len(records), "records": records},
        backend_version=module_version("pubchempy"),
    )


def _rcsb(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    query = inputs["query"]
    timeout = float(settings.get("timeout_seconds", 30))
    if isinstance(query, str) and len(query.strip()) == 4 and query.strip().isalnum():
        pdb_id = query.strip().upper()
        response = httpx.get(f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}", timeout=timeout)
        response.raise_for_status()
        value = response.json()
        record = {
            "pdb_id": pdb_id,
            "title": (value.get("struct") or {}).get("title"),
            "experimental_methods": [item.get("method") for item in value.get("exptl", [])],
            "resolution_angstrom": (value.get("rcsb_entry_info") or {}).get("resolution_combined"),
            "release_date": (value.get("rcsb_accession_info") or {}).get("initial_release_date"),
            "polymer_entity_count": (value.get("rcsb_entry_info") or {}).get("polymer_entity_count"),
        }
        return success({"query": query, "count": 1, "records": [record]}, backend_version=module_version("httpx"))
    search_query = query if isinstance(query, dict) else {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {"value": str(query)},
        },
        "return_type": "entry",
    }
    search_query.setdefault("request_options", {})["paginate"] = {
        "start": 0,
        "rows": int(settings.get("max_records", 10)),
    }
    response = httpx.post(
        "https://search.rcsb.org/rcsbsearch/v2/query",
        json=search_query,
        timeout=timeout,
    )
    response.raise_for_status()
    value = response.json()
    records = [
        {"pdb_id": item.get("identifier"), "score": item.get("score")}
        for item in value.get("result_set", [])
    ]
    return success({"query": query, "count": len(records), "records": records}, backend_version=module_version("httpx"))


def _materials_project(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    query = inputs["query"]
    api_key = os.environ.get("MP_API_KEY", "").strip()
    if not api_key:
        return unavailable("MP_API_KEY is not configured", install="Set MP_API_KEY for the Materials Project account")
    fields = list(
        settings.get(
            "fields",
            [
                "material_id", "formula_pretty", "energy_above_hull", "band_gap",
                "is_stable", "symmetry", "volume", "density",
            ],
        )
    )
    criteria: dict[str, Any]
    if isinstance(query, str):
        criteria = {"material_ids": [query]} if query.startswith("mp-") else {"formula": query}
    elif isinstance(query, dict):
        criteria = dict(query)
    else:
        raise ValueError("Materials Project query must be a string or mapping")
    limit = int(settings.get("max_records", 20))
    if limit < 1 or limit > 1000:
        raise ValueError("max_records must be between 1 and 1000")
    parameters: dict[str, Any] = {
        "_fields": ",".join(fields),
        "_limit": limit,
    }
    for name, value in criteria.items():
        if isinstance(value, (list, set)):
            parameters[name] = ",".join(str(item) for item in value)
        elif isinstance(value, tuple) and len(value) == 2:
            if value[0] is not None:
                parameters[f"{name}_min"] = value[0]
            if value[1] is not None:
                parameters[f"{name}_max"] = value[1]
        elif isinstance(value, bool):
            parameters[name] = str(value).lower()
        else:
            parameters[name] = value
    endpoint = os.environ.get(
        "MP_API_ENDPOINT", "https://api.materialsproject.org"
    ).rstrip("/")
    response = httpx.get(
        endpoint + "/materials/summary/",
        params=parameters,
        headers={"X-API-KEY": api_key},
        timeout=float(settings.get("timeout_seconds", 30)),
    )
    response.raise_for_status()
    payload = response.json()
    records = list(payload.get("data") or [])
    return success(
        {
            "query": criteria,
            "count": len(records),
            "records": records,
            "api_metadata": payload.get("meta") or {},
        },
        backend_version=module_version("httpx"),
    )


def _catalysis_hub(request: dict[str, Any]) -> dict[str, Any]:
    inputs, _method, settings = request_parts(request)
    query = inputs["query"]
    if not isinstance(query, dict):
        raise ValueError("Catalysis-Hub query must be a mapping")
    reactants = str(query.get("reactants") or "")
    products = str(query.get("products") or "")
    if not reactants and not products:
        raise ValueError("At least one of query.reactants or query.products is required")
    first = int(settings.get("max_records", 20))
    declarations = ["$first: Int!"]
    arguments = ["first: $first"]
    variables: dict[str, Any] = {"first": first}
    if reactants:
        declarations.append("$reactants: String!")
        arguments.append("reactants: $reactants")
        variables["reactants"] = reactants
    if products:
        declarations.append("$products: String!")
        arguments.append("products: $products")
        variables["products"] = products
    graphql = """
    query Search(%s) {
      reactions(%s) {
        totalCount
        edges { node { id reactants products reactionEnergy activationEnergy chemicalComposition surfaceComposition facet } }
      }
    }
    """ % (", ".join(declarations), ", ".join(arguments))
    response = httpx.post(
        "https://api.catalysis-hub.org/graphql",
        json={
            "query": graphql,
            "variables": variables,
        },
        timeout=float(settings.get("timeout_seconds", 60)),
    )
    response.raise_for_status()
    value = response.json()
    if value.get("errors"):
        raise RuntimeError(f"Catalysis-Hub GraphQL errors: {value['errors']}")
    reactions = ((value.get("data") or {}).get("reactions") or {})
    records = [edge.get("node", {}) for edge in reactions.get("edges", [])]
    return success(
        {
            "query": {"reactants": reactants or None, "products": products or None},
            "total_count": reactions.get("totalCount", len(records)),
            "count": len(records),
            "records": records,
        },
        backend_version=module_version("httpx"),
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if action_id == "search_compounds" and backend_id == "pubchem":
        return _pubchem(request)
    if action_id == "search_protein_structures" and backend_id == "rcsb_pdb":
        return _rcsb(request)
    if action_id == "search_materials" and backend_id == "materials_project":
        return _materials_project(request)
    if action_id == "search_catalysis_records" and backend_id == "catalysis_hub":
        return _catalysis_hub(request)
    if action_id == "lookup_nist_webbook_species" and backend_id == "nist_webbook":
        return _nist_webbook(request)
    return unsupported(f"Unsupported data action/backend combination: {action_id}/{backend_id}")
