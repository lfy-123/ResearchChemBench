from __future__ import annotations

import contextlib
import os
import re
import shlex
import signal
import subprocess
import time
import urllib.error
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from src.core.logging import log_progress
from src.integrations.pdf_fallback import fallback_pdf_to_tei

TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI_NAMESPACE}


class GrobidError(RuntimeError):
    pass


@dataclass(frozen=True)
class GrobidClient:
    base_url: str = "http://127.0.0.1:8070"
    timeout_seconds: int = 900
    retries: int = 2
    consolidate_header: int = 0
    consolidate_citations: int = 0

    def process_fulltext_document(self, pdf_path: str | Path) -> str:
        pdf_path = Path(pdf_path).expanduser().resolve()
        boundary = f"----ResearchChemBench{uuid.uuid4().hex}"
        body = _multipart_body(
            boundary,
            pdf_path,
            {
                "consolidateHeader": str(self.consolidate_header),
                "consolidateCitations": str(self.consolidate_citations),
                "includeRawAffiliations": "1",
            },
        )
        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/api/processFulltextDocument",
            data=body,
            headers={
                "Accept": "application/xml",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    payload = response.read()
                    if response.status == 204 or not payload.strip():
                        raise GrobidError(f"GROBID returned no content for {pdf_path.name}")
                    return payload.decode("utf-8", errors="replace")
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:2000]
                last_error = GrobidError(
                    f"GROBID HTTP {exc.code} for {pdf_path.name}: {detail or exc.reason}"
                )
                if exc.code != 503 or attempt >= self.retries:
                    raise last_error from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
                if attempt >= self.retries:
                    break
            time.sleep(min(10, 2**attempt))
        raise GrobidError(f"GROBID request failed for {pdf_path.name}: {last_error}")


def grobid_is_alive(base_url: str, timeout_seconds: int = 5) -> bool:
    try:
        with urllib.request.urlopen(
            f"{base_url.rstrip('/')}/api/isalive", timeout=timeout_seconds
        ) as response:
            return response.status == 200 and response.read().decode("utf-8").strip() == "true"
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False


@contextlib.contextmanager
def grobid_service(config: dict[str, Any]) -> Iterator[GrobidClient]:
    base_url = str(config.get("base_url", "http://127.0.0.1:8070"))
    client = GrobidClient(
        base_url=base_url,
        timeout_seconds=int(config.get("timeout_seconds", 900)),
        retries=int(config.get("retries", 2)),
        consolidate_header=int(config.get("consolidate_header", 0)),
        consolidate_citations=int(config.get("consolidate_citations", 0)),
    )
    if grobid_is_alive(base_url):
        yield client
        return
    if not config.get("auto_start", True):
        raise GrobidError(f"GROBID is not reachable at {base_url}")

    working_directory = Path(config["working_directory"]).expanduser().resolve()
    raw_command = config.get("start_command") or ["./gradlew", "--no-daemon", "run"]
    command = shlex.split(raw_command) if isinstance(raw_command, str) else list(raw_command)
    log_path = Path(config["service_log"]).expanduser().resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    java_home = config.get("java_home") or environment.get("GROBID_JAVA_HOME")
    if java_home:
        environment["JAVA_HOME"] = str(java_home)
        environment["PATH"] = f"{Path(java_home) / 'bin'}:{environment.get('PATH', '')}"

    log_handle = log_path.open("a", encoding="utf-8")
    process = subprocess.Popen(
        command,
        cwd=working_directory,
        env=environment,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    startup_timeout = int(config.get("startup_timeout_seconds", 300))
    deadline = time.monotonic() + startup_timeout
    try:
        while time.monotonic() < deadline:
            if grobid_is_alive(base_url):
                yield client
                return
            if process.poll() is not None:
                raise GrobidError(
                    f"GROBID exited with code {process.returncode}; inspect {log_path}"
                )
            time.sleep(2)
        raise GrobidError(
            f"GROBID did not become ready within {startup_timeout}s; inspect {log_path}"
        )
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=10)
        log_handle.close()


def extract_documents_with_grobid(
    inventory: list[dict[str, Any]],
    client: GrobidClient,
    tei_dir: str | Path,
    text_dir: str | Path,
    max_chars: int = 2_000_000,
    reuse_existing: bool = True,
    exclude_supplementary: bool = True,
    fallback_config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    canonical = [
        item
        for item in inventory
        if not item.get("duplicate_of")
        and (not exclude_supplementary or item.get("document_role") != "supplementary")
    ]
    tei_dir = Path(tei_dir).expanduser().resolve()
    text_dir = Path(text_dir).expanduser().resolve()
    tei_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)
    output: list[dict[str, Any]] = []

    for index, item in enumerate(canonical, start=1):
        record = dict(item)
        tei_path = tei_dir / f"{item['document_id']}.tei.xml"
        text_path = text_dir / f"{item['document_id']}.txt"
        request_attempted = False
        request_failed = False
        request_error: str | None = None
        try:
            fallback_used: dict[str, Any] | None = None
            if tei_path.exists() and reuse_existing:
                tei_xml = tei_path.read_text(encoding="utf-8", errors="replace")
                status = "reused"
            else:
                try:
                    request_attempted = True
                    tei_xml = client.process_fulltext_document(item["source_path"])
                    status = "success"
                except Exception as grobid_error:
                    request_failed = True
                    request_error = f"{type(grobid_error).__name__}: {grobid_error}"
                    if not (fallback_config or {}).get("enabled", True):
                        raise
                    fallback_used = fallback_pdf_to_tei(
                        item,
                        (fallback_config or {}).get("output_dir", text_dir.parent / "fallback"),
                        fallback_config or {},
                    )
                    fallback_used["grobid_error"] = request_error
                    tei_xml = fallback_used["tei_xml"]
                    status = f"fallback_{fallback_used['parser']}"
                tei_path.write_text(tei_xml, encoding="utf-8")
            parsed = parse_grobid_tei(tei_xml)
            text = parsed.pop("text")[:max_chars]
            text_path.write_text(text, encoding="utf-8")
            quality = text_quality(text, item.get("page_count"))
            record.update(
                {
                    **parsed,
                    "title": parsed.get("title") or Path(item["file_name"]).stem,
                    "text_path": str(text_path),
                    "grobid_text_path": str(text_path),
                    "grobid_tei_path": str(tei_path),
                    "grobid_extract_status": status,
                    "grobid_request_attempted": request_attempted,
                    "grobid_request_failed": request_failed,
                    "grobid_request_error": request_error,
                    "text_quality": quality,
                    "text_characters": len(text),
                    "metadata_source": (
                        f"{fallback_used['parser']}_fallback_tei" if fallback_used else "grobid_tei"
                    ),
                    "retrieval_sources": [
                        "local_corpus",
                        fallback_used["parser"] if fallback_used else "grobid",
                    ],
                    "grobid_fallback": (
                        {
                            key: value
                            for key, value in fallback_used.items()
                            if key not in {"text", "tei_xml"}
                        }
                        if fallback_used
                        else None
                    ),
                }
            )
        except Exception as exc:
            record.update(
                {
                    "title": Path(item["file_name"]).stem,
                    "abstract": "",
                    "authors": [],
                    "author_details": [],
                    "section_headings": [],
                    "text_path": None,
                    "grobid_text_path": None,
                    "grobid_tei_path": str(tei_path) if tei_path.exists() else None,
                    "grobid_extract_status": "failed",
                    "grobid_extract_error": str(exc),
                    "grobid_request_attempted": request_attempted,
                    "grobid_request_failed": request_failed,
                    "grobid_request_error": request_error,
                    "text_quality": {"score": 0.0, "needs_ocr": True},
                    "text_characters": 0,
                    "metadata_source": "grobid_tei",
                    "retrieval_sources": ["local_corpus", "grobid"],
                }
            )
        output.append(record)
        log_progress(
            "stage_02_grobid_extract",
            index,
            len(canonical),
            item.get("file_name", item["document_id"]),
            status=record.get("grobid_extract_status"),
        )
    return output


def parse_grobid_tei(tei_xml: str) -> dict[str, Any]:
    root = ET.fromstring(tei_xml)
    title = _clean_title(
        _first_text(
            root,
            (
                ".//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']",
                ".//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@level='a']",
                ".//tei:sourceDesc//tei:analytic/tei:title[@level='a']",
                ".//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title",
            ),
        )
    )
    abstract_element = root.find(".//tei:teiHeader/tei:profileDesc/tei:abstract", NS)
    abstract = _extract_abstract(abstract_element)
    section_headings = _section_headings(root)
    author_details = _extract_authors(root)
    publication_date = _publication_date(root)
    page_range = _bibliographic_scope(root, ("page", "pages", "pp"))
    keywords = _unique_texts(root.findall(".//tei:profileDesc//tei:keywords//tei:term", NS))
    text = _tei_document_text(root, title, abstract)
    return {
        "title": title,
        "abstract": abstract,
        "authors": [item["full_name"] for item in author_details if item.get("full_name")],
        "author_details": author_details,
        "doi": _main_identifier(root, "doi"),
        "publication_date": publication_date,
        "year": _year(publication_date),
        "venue": _first_text(
            root,
            (
                ".//tei:sourceDesc//tei:monogr/tei:title[@level='j']",
                ".//tei:sourceDesc//tei:monogr/tei:title[@level='m']",
            ),
        ),
        "volume": _bibliographic_scope(root, ("volume", "vol")),
        "issue": _bibliographic_scope(root, ("issue", "number")),
        "article_pages": page_range,
        "publisher": _first_text(
            root,
            (
                ".//tei:sourceDesc//tei:imprint/tei:publisher",
                ".//tei:publicationStmt/tei:publisher",
            ),
        ),
        "language": root.attrib.get("{http://www.w3.org/XML/1998/namespace}lang"),
        "keywords": keywords,
        "section_headings": section_headings,
        "text": text,
    }


def text_quality(text: str, page_count: int | None) -> dict[str, Any]:
    non_space = sum(1 for char in text if not char.isspace())
    alpha_numeric = sum(1 for char in text if char.isalnum())
    readable_ratio = alpha_numeric / max(1, non_space)
    chars_per_page = len(text) / max(1, page_count or 1)
    length_score = min(1.0, chars_per_page / 1200)
    score = round(100 * (0.65 * readable_ratio + 0.35 * length_score), 1)
    return {
        "score": score,
        "readable_ratio": round(readable_ratio, 3),
        "characters_per_page": round(chars_per_page, 1),
        "needs_ocr": score < 45 or len(text) < 1000,
    }


def _multipart_body(boundary: str, pdf_path: Path, fields: dict[str, str]) -> bytes:
    chunks: list[bytes] = []
    marker = boundary.encode("ascii")
    for name, value in fields.items():
        chunks.extend(
            [
                b"--" + marker + b"\r\n",
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    chunks.extend(
        [
            b"--" + marker + b"\r\n",
            (
                f'Content-Disposition: form-data; name="input"; filename="{pdf_path.name}"\r\n'
            ).encode("utf-8"),
            b"Content-Type: application/pdf\r\n\r\n",
            pdf_path.read_bytes(),
            b"\r\n--" + marker + b"--\r\n",
        ]
    )
    return b"".join(chunks)


def _extract_authors(root: ET.Element) -> list[dict[str, Any]]:
    elements = root.findall(".//tei:sourceDesc//tei:analytic/tei:author", NS)
    if not elements:
        elements = root.findall(".//tei:titleStmt/tei:author", NS)
    authors: list[dict[str, Any]] = []
    seen: set[str] = set()
    for author in elements:
        pers_name = author.find("tei:persName", NS)
        if pers_name is None:
            continue
        forenames = [
            _clean_person_part(_element_text(item))
            for item in pers_name.findall("tei:forename", NS)
        ]
        forenames = [value for value in forenames if value]
        surname = _clean_person_part(_element_text(pers_name.find("tei:surname", NS)))
        if not forenames or not surname:
            continue
        full_name = _normalize_space(" ".join([*forenames, surname]))
        if not full_name or full_name.casefold() in seen:
            continue
        seen.add(full_name.casefold())
        affiliations = []
        for affiliation in author.findall("tei:affiliation", NS):
            value = _element_text(affiliation)
            if value and value not in affiliations:
                affiliations.append(value)
        authors.append(
            {
                "full_name": full_name,
                "given_names": forenames,
                "surname": surname,
                "orcid": _identifier(author, "orcid"),
                "affiliations": affiliations,
                "corresponding": author.attrib.get("role") == "corresp",
            }
        )
    return authors


def _publication_date(root: ET.Element) -> str:
    candidates = root.findall(".//tei:sourceDesc//tei:imprint/tei:date", NS)
    candidates.extend(root.findall(".//tei:publicationStmt/tei:date", NS))
    ordered = sorted(
        candidates,
        key=lambda item: (
            0
            if item.attrib.get("type", "").casefold() in {"published", "issued", "publication"}
            else 1
        ),
    )
    for item in ordered:
        value = item.attrib.get("when") or _element_text(item)
        if value:
            return value
    return ""


def _identifier(root: ET.Element, kind: str) -> str:
    for item in root.findall(".//tei:idno", NS):
        if item.attrib.get("type", "").casefold() == kind.casefold():
            return _element_text(item)
    return ""


def _main_identifier(root: ET.Element, kind: str) -> str:
    accepted = kind.casefold()
    paths = (
        ".//tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:biblStruct/tei:idno",
        ".//tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:biblStruct/tei:analytic/tei:idno",
        ".//tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno",
    )
    for path in paths:
        for item in root.findall(path, NS):
            if item.attrib.get("type", "").casefold() == accepted:
                return _element_text(item)
    return ""


def _bibliographic_scope(root: ET.Element, units: tuple[str, ...]) -> str:
    accepted = {unit.casefold() for unit in units}
    for item in root.findall(".//tei:sourceDesc//tei:biblScope", NS):
        unit = (item.attrib.get("unit") or item.attrib.get("type") or "").casefold()
        if unit not in accepted:
            continue
        start = item.attrib.get("from")
        end = item.attrib.get("to")
        if start and end and start != end:
            return f"{start}-{end}"
        return start or end or _element_text(item)
    return ""


def _tei_document_text(root: ET.Element, title: str, abstract: str) -> str:
    parts = [value for value in (title, abstract) if value]
    body = root.find(".//tei:text/tei:body", NS)
    if body is not None:
        for element in body.iter():
            if _local_name(element.tag) not in {"head", "p", "item", "figDesc"}:
                continue
            value = _element_text(element)
            if value:
                parts.append(value)
    return "\n\n".join(dict.fromkeys(parts))


def _extract_abstract(element: ET.Element | None) -> str:
    if element is None:
        return ""
    paragraphs = element.findall(".//tei:p", NS)
    if not paragraphs:
        return _element_text(element)
    values = [_element_text(paragraph) for paragraph in paragraphs]
    values = [value for value in values if value]
    if len(values) > 1 and len(values[0]) >= 600 and _looks_like_introduction(paragraphs[1]):
        return values[0]
    return _normalize_space(" ".join(values))


def _looks_like_introduction(element: ET.Element) -> bool:
    for reference in element.findall(".//tei:ref", NS):
        if reference.attrib.get("type", "").casefold() in {"bibr", "figure", "table"}:
            return True
    text = _element_text(element)
    return bool(re.search(r"\b(?:fig(?:ure)?|table)\.?\s*\d", text, re.IGNORECASE))


def _section_headings(root: ET.Element) -> list[str]:
    divisions = root.findall(".//tei:text/tei:body//tei:div", NS)
    values = [
        _element_text(heading)
        for division in divisions
        if (heading := division.find("tei:head", NS)) is not None
        and _is_section_heading(heading, division)
    ]
    return list(dict.fromkeys(value for value in values if value))


def _is_section_heading(element: ET.Element, parent: ET.Element) -> bool:
    normalized = _element_text(element)
    if len(normalized) < 3 or sum(char.isalpha() for char in normalized) < 3:
        return False
    if re.match(r"^(?:fig(?:ure)?|table)\b", normalized, re.IGNORECASE):
        return False
    if re.match(r"^supplementary\s+(?:fig(?:ure)?|table)\b", normalized, re.IGNORECASE):
        return False
    if re.fullmatch(r"(?:s?\d+[a-z]?|[ivxlcdm]+|[a-z])[.)]?", normalized, re.IGNORECASE):
        return False
    paragraph = parent.find("tei:p", NS)
    paragraph_text = _element_text(paragraph)
    if paragraph_text and paragraph_text[0].islower():
        return False
    return True


def _first_text(root: ET.Element, paths: tuple[str, ...]) -> str:
    for path in paths:
        value = _element_text(root.find(path, NS))
        if value:
            return value
    return ""


def _unique_texts(elements: list[ET.Element]) -> list[str]:
    values = [_element_text(element) for element in elements]
    return list(dict.fromkeys(value for value in values if value))


def _element_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return _normalize_space(" ".join(element.itertext()))


def _normalize_space(value: str) -> str:
    return " ".join(value.split())


def _clean_title(value: str) -> str:
    normalized = _normalize_space(value)
    normalized = re.sub(r"^title\s*:\s*", "", normalized, flags=re.IGNORECASE)
    if normalized.casefold().endswith(" permalink"):
        normalized = normalized[: -len(" permalink")].rstrip()
    return normalized


def _clean_person_part(value: str) -> str:
    normalized = _normalize_space(value)
    normalized = re.sub(r"^[^\w]+", "", normalized)
    return re.sub(r"[^\w.'’\-]+$", "", normalized)


def _year(value: str) -> int | None:
    for token in value.replace("/", "-").split("-"):
        if len(token) == 4 and token.isdigit():
            return int(token)
    return None


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]
