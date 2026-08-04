from __future__ import annotations

import html
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)


def fallback_pdf_to_tei(
    item: dict[str, Any],
    output_dir: str | Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    root = Path(output_dir).expanduser().resolve() / str(item["document_id"])
    root.mkdir(parents=True, exist_ok=True)
    if not config.get("pdftotext_enabled", True):
        raise RuntimeError("Stage 02 pdftotext fallback is disabled")
    text_path = root / "pdftotext.txt"
    completed = subprocess.run(
        ["pdftotext", "-layout", str(item["source_path"]), str(text_path)],
        capture_output=True,
        text=True,
        timeout=int(config.get("pdftotext_timeout_seconds", 300)),
        check=False,
    )
    if completed.returncode != 0 or not text_path.is_file():
        error = completed.stderr[-1000:] or f"pdftotext exited {completed.returncode}"
        raise RuntimeError(error)
    text = text_path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise RuntimeError("pdftotext produced empty output")
    return _result(item, text, "pdftotext", root, {"return_code": 0})


def text_to_minimal_tei(text: str, *, title: str, abstract: str = "") -> str:
    ET.register_namespace("", TEI_NAMESPACE)
    tei = ET.Element(f"{{{TEI_NAMESPACE}}}TEI")
    header = ET.SubElement(tei, f"{{{TEI_NAMESPACE}}}teiHeader")
    file_desc = ET.SubElement(header, f"{{{TEI_NAMESPACE}}}fileDesc")
    title_stmt = ET.SubElement(file_desc, f"{{{TEI_NAMESPACE}}}titleStmt")
    ET.SubElement(title_stmt, f"{{{TEI_NAMESPACE}}}title", {"type": "main"}).text = title
    ET.SubElement(file_desc, f"{{{TEI_NAMESPACE}}}publicationStmt")
    source_desc = ET.SubElement(file_desc, f"{{{TEI_NAMESPACE}}}sourceDesc")
    bibl = ET.SubElement(source_desc, f"{{{TEI_NAMESPACE}}}biblStruct")
    analytic = ET.SubElement(bibl, f"{{{TEI_NAMESPACE}}}analytic")
    ET.SubElement(analytic, f"{{{TEI_NAMESPACE}}}title", {"level": "a"}).text = title
    profile = ET.SubElement(header, f"{{{TEI_NAMESPACE}}}profileDesc")
    abstract_node = ET.SubElement(profile, f"{{{TEI_NAMESPACE}}}abstract")
    ET.SubElement(abstract_node, f"{{{TEI_NAMESPACE}}}p").text = abstract

    body = ET.SubElement(ET.SubElement(tei, f"{{{TEI_NAMESPACE}}}text"), f"{{{TEI_NAMESPACE}}}body")
    current = ET.SubElement(body, f"{{{TEI_NAMESPACE}}}div")
    for kind, value in _blocks(text):
        if kind == "head":
            current = ET.SubElement(body, f"{{{TEI_NAMESPACE}}}div")
            ET.SubElement(current, f"{{{TEI_NAMESPACE}}}head").text = value
        else:
            ET.SubElement(current, f"{{{TEI_NAMESPACE}}}p").text = value
    return ET.tostring(tei, encoding="unicode", xml_declaration=True)


def _result(
    item: dict[str, Any], text: str, parser: str, root: Path, details: dict[str, Any]
) -> dict[str, Any]:
    metadata = _plain_metadata(text)
    title = metadata.get("title") or Path(str(item.get("file_name") or item["source_path"])).stem
    abstract = metadata.get("abstract") or ""
    tei_xml = text_to_minimal_tei(text, title=title, abstract=abstract)
    (root / "fallback_source.txt").write_text(text, encoding="utf-8")
    (root / "fallback.tei.xml").write_text(tei_xml, encoding="utf-8")
    return {
        "parser": parser,
        "text": text,
        "tei_xml": tei_xml,
        "title": title,
        "abstract": abstract,
        "details": details,
    }


def _plain_metadata(text: str) -> dict[str, str]:
    lines = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
    title = next((line for line in lines[:20] if 5 <= len(line.split()) <= 30), "")
    abstract = ""
    match = re.search(
        r"\babstract\b\s*[:.-]?\s*(.{100,4000}?)(?=\n\s*(?:keywords?|introduction)\b)",
        text,
        re.I | re.S,
    )
    if match:
        abstract = " ".join(match.group(1).split())
    return {"title": title, "abstract": abstract}


def _blocks(text: str) -> list[tuple[str, str]]:
    output: list[tuple[str, str]] = []
    for raw in re.split(r"\n\s*\n", html.unescape(text)):
        value = " ".join(raw.split()).strip()
        if not value:
            continue
        heading = re.match(r"^#{1,6}\s+(.+)$", value)
        if heading:
            output.append(("head", heading.group(1).strip()))
        else:
            output.append(("p", value[:20000]))
    return output
