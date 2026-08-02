from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI_NAMESPACE}


def read_tei_paragraphs(path: str | Path) -> list[dict[str, Any]]:
    return parse_tei_paragraphs(Path(path).read_text(encoding="utf-8", errors="replace"))


def parse_tei_paragraphs(tei_xml: str) -> list[dict[str, Any]]:
    root = ET.fromstring(tei_xml)
    output: list[dict[str, Any]] = []
    for div in root.findall(".//tei:text/tei:body//tei:div", NS):
        section = _text(div.find("tei:head", NS))
        for paragraph in div.findall("tei:p", NS):
            text = _text(paragraph)
            if len(text) < 20:
                continue
            output.append(
                {
                    "paragraph_index": len(output),
                    "section": section,
                    "text": text,
                    "xml_id": paragraph.attrib.get(
                        "{http://www.w3.org/XML/1998/namespace}id"
                    ),
                }
            )
    if output:
        return output
    for paragraph in root.findall(".//tei:text/tei:body//tei:p", NS):
        text = _text(paragraph)
        if len(text) >= 20:
            output.append(
                {
                    "paragraph_index": len(output),
                    "section": "",
                    "text": text,
                    "xml_id": paragraph.attrib.get(
                        "{http://www.w3.org/XML/1998/namespace}id"
                    ),
                }
            )
    return output


def sentence_windows(paragraph: dict[str, Any]) -> list[dict[str, Any]]:
    sentences = [
        value.strip()
        for value in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", paragraph["text"])
        if len(value.strip()) >= 15
    ]
    return [
        {
            **paragraph,
            "sentence_index": index,
            "text": sentence,
        }
        for index, sentence in enumerate(sentences)
    ] or [dict(paragraph, sentence_index=0)]


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return re.sub(r"\s+", " ", " ".join(element.itertext())).strip()
