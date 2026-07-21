"""External chemistry data actions."""

from __future__ import annotations

import os
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, urlencode, urljoin, urlparse

import httpx

from ..proxy import configure_pubchem_proxy_environment
from .common import failed, module_version, partial_success, request_parts, success, unavailable, unsupported


ACTIONS = {
    "search_compounds", "search_protein_structures", "search_materials",
    "search_catalysis_records", "lookup_nist_webbook_species",
    "resolve_chemical_identity", "retrieve_compound_properties",
    "retrieve_compound_structure",
    "search_similar_compounds", "search_substructures",
}


_NIST_WEBBOOK_ENDPOINT = "https://webbook.nist.gov/cgi/cbook.cgi"
_CAS_NUMBER = re.compile(r"^\d{2,7}-\d{2}-\d$")
_EXACT_FORMULA = re.compile(r"^[A-Za-z0-9()[\]+.\-]+$")
_TRANSIENT_HTTP_STATUSES = {408, 425, 429, 500, 502, 503, 504}


class _RemoteServiceUnavailable(RuntimeError):
    def __init__(self, service: str, attempts: int, cause: Exception):
        self.diagnostics = _remote_error_diagnostics(cause)
        detail = f"; diagnostics={self.diagnostics}" if self.diagnostics else ""
        super().__init__(
            f"{service} remained unavailable after {attempts} attempt(s): "
            f"{type(cause).__name__}: {cause}{detail}"
        )
        self.service = service
        self.attempts = attempts
        self.cause = cause


def _remote_error_diagnostics(exc: Exception) -> dict[str, Any]:
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", {}) or {}
    diagnostics = {
        "status_code": getattr(response, "status_code", None) or getattr(exc, "code", None),
        "retry_after": headers.get("Retry-After") or headers.get("retry-after"),
        "x_throttling_control": headers.get("x-throttling-control"),
    }
    return {key: value for key, value in diagnostics.items() if value is not None}


def _remote_retry_policy(settings: dict[str, Any]) -> tuple[int, float]:
    retries = int(settings.get("max_retries", 1))
    backoff = float(settings.get("retry_backoff_seconds", 1.0))
    if retries < 0 or retries > 4:
        raise ValueError("max_retries must be between 0 and 4")
    if backoff < 0.0 or backoff > 30.0:
        raise ValueError("retry_backoff_seconds must be between 0 and 30")
    return retries + 1, backoff


def _retryable_remote_exception(exc: Exception) -> bool:
    response = getattr(exc, "response", None)
    status_code = getattr(response, "status_code", None)
    if status_code is None:
        status_code = getattr(exc, "code", None)
    if status_code in _TRANSIENT_HTTP_STATUSES:
        return True
    return isinstance(exc, (httpx.TimeoutException, httpx.TransportError, TimeoutError, ConnectionError))


def _retry_after_seconds(exc: Exception) -> float | None:
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", {}) or {}
    value = headers.get("Retry-After") or headers.get("retry-after")
    try:
        delay = float(value)
    except (TypeError, ValueError):
        return None
    return min(60.0, max(0.0, delay))


def _remote_call_with_retry(
    operation: Any,
    *,
    service: str,
    settings: dict[str, Any],
) -> tuple[Any, int]:
    attempts, base_backoff = _remote_retry_policy(settings)
    for attempt in range(1, attempts + 1):
        try:
            return operation(), attempt
        except Exception as exc:
            if not _retryable_remote_exception(exc):
                raise
            if attempt == attempts:
                raise _RemoteServiceUnavailable(service, attempt, exc) from exc
            delay = _retry_after_seconds(exc)
            if delay is None:
                delay = base_backoff * (2 ** (attempt - 1))
            if delay:
                time.sleep(delay)
    raise AssertionError("remote retry loop terminated unexpectedly")


def _pubchem_rate_limit(settings: dict[str, Any]) -> None:
    """Enforce a cross-worker request interval below PubChem's 5 request/s limit."""

    interval = float(settings.get("minimum_request_interval_seconds", 0.25))
    if interval < 0.0 or interval > 30.0:
        raise ValueError("minimum_request_interval_seconds must be between 0 and 30")
    if interval == 0.0:
        return
    state_path = Path(
        os.environ.get(
            "RESEARCHCHEMBENCH_PUBCHEM_RATE_STATE",
            str(Path(__file__).resolve().parents[4] / ".software_cache" / "pubchem" / "request_rate.state"),
        )
    )
    state_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import fcntl

        with state_path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            handle.seek(0)
            try:
                previous = float(handle.read().strip() or 0.0)
            except ValueError:
                previous = 0.0
            delay = interval - (time.time() - previous)
            if delay > 0.0:
                time.sleep(delay)
            handle.seek(0)
            handle.truncate()
            handle.write(str(time.time()))
            handle.flush()
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError:
        # The retry/backoff layer still protects the remote service if shared state
        # cannot be written in a restricted deployment.
        return


def _pubchem_get_compounds(
    pcp: Any,
    identifier: str,
    namespace: str,
    settings: dict[str, Any],
    **kwargs: Any,
) -> tuple[list[Any], int]:
    if hasattr(pcp, "Compound"):
        payload, attempts = _pubchem_compound_json(
            identifier,
            namespace,
            settings,
            **kwargs,
        )
        return [pcp.Compound(record) for record in payload.get("PC_Compounds") or []], attempts
    compounds, attempts = _remote_call_with_retry(
        lambda: pcp.get_compounds(identifier, namespace, **kwargs),
        service="PubChem PUG REST",
        settings=settings,
    )
    return list(compounds), attempts


def _pubchem_compound_json(
    identifier: str,
    namespace: str,
    settings: dict[str, Any],
    **parameters: Any,
) -> tuple[dict[str, Any], int]:
    """Fetch full PubChem compound JSON while preserving Retry-After headers."""

    headers = {
        "Accept": "application/json",
        "User-Agent": "ResearchChemBench/1.0 bounded-pubchem-query",
    }
    base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"

    def fetch(query_namespace: str, query_identifier: str) -> tuple[dict[str, Any], int]:
        if query_namespace == "formula":
            url = f"{base}/formula/{quote(query_identifier, safe='')}/JSON"

            def request_value():
                _pubchem_rate_limit(settings)
                response = httpx.get(
                    url,
                    params=parameters,
                    headers=headers,
                    timeout=float(settings.get("timeout_seconds", 30)),
                    follow_redirects=True,
                )
                if getattr(response, "status_code", 200) != 404:
                    response.raise_for_status()
                return response
        elif query_namespace == "listkey":
            url = f"{base}/listkey/{quote(query_identifier, safe='')}/JSON"

            def request_value():
                _pubchem_rate_limit(settings)
                response = httpx.get(
                    url,
                    params=parameters,
                    headers=headers,
                    timeout=float(settings.get("timeout_seconds", 30)),
                    follow_redirects=True,
                )
                if getattr(response, "status_code", 200) != 404:
                    response.raise_for_status()
                return response
        else:
            url = f"{base}/{query_namespace}/JSON"

            def request_value():
                _pubchem_rate_limit(settings)
                response = httpx.post(
                    url,
                    params=parameters,
                    data={query_namespace: query_identifier},
                    headers=headers,
                    timeout=float(settings.get("timeout_seconds", 30)),
                    follow_redirects=True,
                )
                if getattr(response, "status_code", 200) != 404:
                    response.raise_for_status()
                return response

        response, request_attempts = _remote_call_with_retry(
            request_value,
            service="PubChem PUG REST",
            settings=settings,
        )
        content = getattr(response, "content", b"")
        if content and len(content) > 32 * 1024 * 1024:
            raise RuntimeError("PubChem compound response exceeds the 32 MiB bounded-response limit")
        return response.json(), request_attempts

    payload, attempts = fetch(namespace, identifier)
    waiting = payload.get("Waiting") or {}
    maximum_polls = int(settings.get("max_poll_attempts", 15))
    poll_interval = float(settings.get("poll_interval_seconds", 2.0))
    if maximum_polls < 1 or maximum_polls > 60:
        raise ValueError("max_poll_attempts must be between 1 and 60")
    if poll_interval < 0.1 or poll_interval > 30.0:
        raise ValueError("poll_interval_seconds must be between 0.1 and 30")
    polls = 0
    while waiting.get("ListKey"):
        polls += 1
        if polls > maximum_polls:
            raise _RemoteServiceUnavailable(
                "PubChem PUG REST",
                attempts,
                TimeoutError("asynchronous PubChem ListKey did not complete within the polling bound"),
            )
        time.sleep(poll_interval)
        payload, poll_attempts = fetch("listkey", str(waiting["ListKey"]))
        attempts += poll_attempts
        waiting = payload.get("Waiting") or {}
    return payload, attempts


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
    compounds, attempts = _pubchem_get_compounds(pcp, identifier, namespace, settings)
    compounds = compounds[:limit]
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
        provenance={"remote_attempts": attempts},
    )


def _pubchem_query(request: dict[str, Any], *, allowed: set[str]) -> tuple[str, str, dict[str, Any]]:
    inputs, _method, settings = request_parts(request)
    query = inputs["query"]
    if isinstance(query, dict):
        extra = sorted(set(query) - {"identifier", "namespace"})
        if extra:
            raise ValueError(f"Unknown PubChem query fields: {extra}")
        identifier = str(query.get("identifier") or "").strip()
        namespace = str(query.get("namespace") or "").strip().lower()
    else:
        identifier = str(query).strip()
        namespace = str(settings.get("namespace", "name")).strip().lower()
    if not identifier or len(identifier) > 10000 or any(ord(character) < 32 for character in identifier):
        raise ValueError("PubChem identifier must contain bounded printable text")
    if namespace not in allowed:
        raise ValueError(f"PubChem namespace must be one of {sorted(allowed)}")
    return identifier, namespace, settings


def _pubchem_identity(request: dict[str, Any]) -> dict[str, Any]:
    import pubchempy as pcp

    identifier, namespace, settings = _pubchem_query(
        request,
        allowed={"name", "cid", "smiles", "inchi", "inchikey"},
    )
    maximum = int(settings.get("max_records", 10))
    if maximum < 1 or maximum > 100:
        raise ValueError("max_records must be between 1 and 100")
    compounds, attempts = _pubchem_get_compounds(pcp, identifier, namespace, settings)
    compounds = compounds[:maximum]
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
    require_unique = bool(settings["require_unique"])
    payload = {
        "query": {"identifier": identifier, "namespace": namespace},
        "match_count": len(records),
        "identity": records[0] if len(records) == 1 else None,
        "candidates": records,
        "unique": len(records) == 1,
    }
    if require_unique and len(records) != 1:
        return partial_success(
            payload,
            backend_version=module_version("pubchempy"),
            warnings=[f"PubChem identity resolution returned {len(records)} records instead of exactly one."],
            provenance={"remote_attempts": attempts},
        )
    return success(
        payload,
        backend_version=module_version("pubchempy"),
        provenance={"remote_attempts": attempts},
    )


_PUBCHEM_PROPERTIES = {
    "cid": "cid",
    "canonical_smiles": "canonical_smiles",
    "isomeric_smiles": "isomeric_smiles",
    "inchi": "inchi",
    "inchikey": "inchikey",
    "molecular_formula": "molecular_formula",
    "molecular_weight": "molecular_weight",
    "iupac_name": "iupac_name",
    "xlogp": "xlogp",
    "tpsa": "tpsa",
    "charge": "charge",
    "complexity": "complexity",
    "h_bond_donor_count": "h_bond_donor_count",
    "h_bond_acceptor_count": "h_bond_acceptor_count",
    "rotatable_bond_count": "rotatable_bond_count",
}


def _pubchem_properties(request: dict[str, Any]) -> dict[str, Any]:
    import pubchempy as pcp

    identifier, namespace, settings = _pubchem_query(
        request,
        allowed={"name", "cid", "smiles", "inchi", "inchikey", "formula"},
    )
    properties = list(settings["properties"])
    if not properties or len(properties) > len(_PUBCHEM_PROPERTIES):
        raise ValueError("properties must contain a non-empty bounded list")
    unknown = sorted(set(properties) - set(_PUBCHEM_PROPERTIES))
    if unknown:
        raise ValueError(f"Unsupported PubChem properties: {unknown}")
    maximum = int(settings["max_records"])
    if maximum < 1 or maximum > 100:
        raise ValueError("max_records must be between 1 and 100")
    compounds, attempts = _pubchem_get_compounds(pcp, identifier, namespace, settings)
    compounds = compounds[:maximum]
    records = [
        {name: getattr(compound, _PUBCHEM_PROPERTIES[name], None) for name in properties}
        for compound in compounds
    ]
    return success(
        {
            "query": {"identifier": identifier, "namespace": namespace},
            "properties": properties,
            "count": len(records),
            "records": records,
        },
        backend_version=module_version("pubchempy"),
        provenance={"remote_attempts": attempts},
    )


_ELEMENT_SYMBOLS = (
    "X H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn "
    "Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr "
    "Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra "
    "Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og"
).split()


def _pubchem_structure(request: dict[str, Any]) -> dict[str, Any]:
    import pubchempy as pcp

    identifier, namespace, settings = _pubchem_query(
        request,
        allowed={"name", "cid", "smiles", "inchi", "inchikey"},
    )
    record_type = str(settings["record_type"]).strip().lower()
    if record_type not in {"2d", "3d"}:
        raise ValueError("record_type must be 2d or 3d")
    hydrogen_policy = str(settings["hydrogen_policy"]).strip().lower()
    if hydrogen_policy not in {"explicit", "omit"}:
        raise ValueError("hydrogen_policy must be explicit or omit")
    maximum = int(settings["max_records"])
    if maximum < 1 or maximum > 20:
        raise ValueError("max_records must be between 1 and 20")
    compounds, attempts = _pubchem_get_compounds(
        pcp,
        identifier,
        namespace,
        settings,
        record_type=record_type,
    )
    compounds = compounds[:maximum]
    structures = []
    for compound in compounds:
        record = dict(compound.record)
        atom_block = dict(record.get("atoms") or {})
        coordinate_blocks = list(record.get("coords") or [])
        if not coordinate_blocks:
            raise RuntimeError(f"PubChem record {getattr(compound, 'cid', None)} contains no coordinates")
        coordinate_block = coordinate_blocks[0]
        conformers = list(coordinate_block.get("conformers") or [])
        if not conformers:
            raise RuntimeError(f"PubChem record {getattr(compound, 'cid', None)} contains no conformer")
        conformer = conformers[0]
        coordinate_aids = list(coordinate_block.get("aid") or [])
        x_values = list(conformer.get("x") or [])
        y_values = list(conformer.get("y") or [])
        z_values = list(conformer.get("z") or [0.0] * len(coordinate_aids))
        if not (
            len(coordinate_aids) == len(x_values) == len(y_values) == len(z_values)
        ):
            raise RuntimeError("PubChem coordinate arrays are not aligned")
        coordinates = {
            int(aid): [float(x), float(y), float(z)]
            for aid, x, y, z in zip(coordinate_aids, x_values, y_values, z_values)
        }
        atom_aids = list(atom_block.get("aid") or [])
        atomic_numbers = list(atom_block.get("element") or [])
        if len(atom_aids) != len(atomic_numbers):
            raise RuntimeError("PubChem atom identifier and element arrays are not aligned")
        retained_aids: set[int] = set()
        atoms = []
        for aid, atomic_number in zip(atom_aids, atomic_numbers):
            aid = int(aid)
            atomic_number = int(atomic_number)
            if not 0 < atomic_number < len(_ELEMENT_SYMBOLS):
                raise RuntimeError(f"Unsupported PubChem atomic number: {atomic_number}")
            if hydrogen_policy == "omit" and atomic_number == 1:
                continue
            if aid not in coordinates:
                raise RuntimeError(f"PubChem coordinates are missing atom id {aid}")
            retained_aids.add(aid)
            atoms.append(
                {
                    "atom_id": aid,
                    "element": _ELEMENT_SYMBOLS[atomic_number],
                    "position_angstrom": coordinates[aid],
                }
            )
        bond_block = dict(record.get("bonds") or {})
        aid1_values = list(bond_block.get("aid1") or [])
        aid2_values = list(bond_block.get("aid2") or [])
        order_values = list(bond_block.get("order") or [])
        if not (len(aid1_values) == len(aid2_values) == len(order_values)):
            raise RuntimeError("PubChem bond arrays are not aligned")
        bonds = [
            {"atom_id_a": int(aid1), "atom_id_b": int(aid2), "order": int(order)}
            for aid1, aid2, order in zip(aid1_values, aid2_values, order_values)
            if int(aid1) in retained_aids and int(aid2) in retained_aids
        ]
        structures.append(
            {
                "cid": int(compound.cid),
                "record_type": record_type,
                "hydrogen_policy": hydrogen_policy,
                "structure": {
                    "atoms": atoms,
                    "bonds": bonds,
                    "charge": int(getattr(compound, "charge", 0) or 0),
                    "multiplicity": 1,
                    "pbc": [False, False, False],
                    "smiles": getattr(compound, "smiles", None)
                    or getattr(compound, "canonical_smiles", None),
                },
            }
        )
    payload = {
        "query": {"identifier": identifier, "namespace": namespace},
        "record_type": record_type,
        "hydrogen_policy": hydrogen_policy,
        "count": len(structures),
        "unique": len(structures) == 1,
        "structures": structures,
    }
    if bool(settings["require_unique"]) and len(structures) != 1:
        return partial_success(
            payload,
            backend_version=module_version("pubchempy"),
            warnings=[f"PubChem structure retrieval returned {len(structures)} records instead of exactly one."],
            provenance={"remote_attempts": attempts},
        )
    return success(
        payload,
        backend_version=module_version("pubchempy"),
        provenance={"remote_attempts": attempts},
    )


def _bounded_pubchem_json(
    url: str,
    *,
    params: dict[str, Any],
    timeout: float,
    settings: dict[str, Any],
) -> tuple[dict[str, Any], int]:
    def request_value():
        _pubchem_rate_limit(settings)
        response = httpx.get(
            url,
            params=params,
            headers={"Accept": "application/json", "User-Agent": "ResearchChemBench/1.0 bounded-pubchem-query"},
            timeout=timeout,
            follow_redirects=True,
        )
        if getattr(response, "status_code", 200) != 404:
            response.raise_for_status()
        return response

    response, attempts = _remote_call_with_retry(
        request_value,
        service="PubChem PUG REST",
        settings=settings,
    )
    content = getattr(response, "content", b"")
    if content and len(content) > 2 * 1024 * 1024:
        raise RuntimeError("PubChem response exceeds the 2 MiB bounded-response limit")
    return response.json(), attempts


def _pubchem_structure_search(action_id: str, request: dict[str, Any]) -> dict[str, Any]:
    if action_id == "search_similar_compounds":
        allowed = {"cid", "smiles", "inchi"}
        operation = "fastsimilarity_2d"
    else:
        allowed = {"cid", "smiles", "smarts", "inchi"}
        operation = "fastsubstructure"
    identifier, namespace, settings = _pubchem_query(request, allowed=allowed)
    maximum = int(settings["max_records"])
    if maximum < 1 or maximum > 1000:
        raise ValueError("max_records must be between 1 and 1000")
    parameters: dict[str, Any] = {
        "MaxRecords": maximum,
        "MaxSeconds": min(60, int(settings.get("timeout_seconds", 30))),
    }
    if action_id == "search_similar_compounds":
        threshold = int(settings["threshold"])
        if threshold < 0 or threshold > 100:
            raise ValueError("threshold must be between 0 and 100")
        parameters["Threshold"] = threshold
    else:
        parameters.update(
            {
                "Stereo": "exact" if bool(settings["match_stereo"]) else "ignore",
                "MatchCharges": str(bool(settings.get("match_charges", False))).lower(),
                "MatchIsotopes": str(bool(settings.get("match_isotopes", False))).lower(),
            }
        )
    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
        f"{operation}/{namespace}/{quote(identifier, safe='')}/cids/JSON"
    )
    payload, attempts = _bounded_pubchem_json(
        url,
        params=parameters,
        timeout=float(settings.get("timeout_seconds", 30)),
        settings=settings,
    )
    identifiers = list((payload.get("IdentifierList") or {}).get("CID") or [])
    records = [{"cid": int(value)} for value in identifiers[:maximum]]
    return success(
        {
            "query": {"identifier": identifier, "namespace": namespace},
            "operation": operation,
            "count": len(records),
            "records": records,
            "request_url": url,
            "matching_controls": parameters,
        },
        backend_version=module_version("httpx"),
        provenance={"remote_attempts": attempts},
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
    endpoint = "https://api.catalysis-hub.org/graphql"

    def request_value():
        response = httpx.post(
            endpoint,
            json={
                "query": graphql,
                "variables": variables,
            },
            headers={
                "Accept": "application/json",
                "User-Agent": "ResearchChemBench/1.0 bounded-catalysis-hub-query",
            },
            timeout=float(settings.get("timeout_seconds", 60)),
            follow_redirects=True,
        )
        response.raise_for_status()
        return response

    response, attempts = _remote_call_with_retry(
        request_value,
        service="Catalysis-Hub GraphQL",
        settings=settings,
    )
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
        provenance={"remote_attempts": attempts, "endpoint": endpoint},
    )


def execute(action_id: str, backend_id: str, request: dict[str, Any]) -> dict[str, Any]:
    try:
        if backend_id == "pubchem":
            configure_pubchem_proxy_environment()
        if action_id == "search_compounds" and backend_id == "pubchem":
            return _pubchem(request)
        if action_id == "resolve_chemical_identity" and backend_id == "pubchem":
            return _pubchem_identity(request)
        if action_id == "retrieve_compound_properties" and backend_id == "pubchem":
            return _pubchem_properties(request)
        if action_id == "retrieve_compound_structure" and backend_id == "pubchem":
            return _pubchem_structure(request)
        if action_id in {"search_similar_compounds", "search_substructures"} and backend_id == "pubchem":
            return _pubchem_structure_search(action_id, request)
        if action_id == "search_protein_structures" and backend_id == "rcsb_pdb":
            return _rcsb(request)
        if action_id == "search_materials" and backend_id == "materials_project":
            return _materials_project(request)
        if action_id == "search_catalysis_records" and backend_id == "catalysis_hub":
            return _catalysis_hub(request)
        if action_id == "lookup_nist_webbook_species" and backend_id == "nist_webbook":
            return _nist_webbook(request)
        return unsupported(f"Unsupported data action/backend combination: {action_id}/{backend_id}")
    except _RemoteServiceUnavailable as exc:
        result = failed(str(exc), code="remote_service_unavailable", retryable=True)
        result["error"].update(
            {
                "service": exc.service,
                "attempts": exc.attempts,
                "diagnostics": exc.diagnostics,
            }
        )
        return result
