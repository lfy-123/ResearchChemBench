from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from src.core.io import merge_dict, read_json, sha256_file
from src.core.models import validate_scientific_record

METHOD_TERMS = (
    "Gaussian",
    "ORCA",
    "VASP",
    "Quantum ESPRESSO",
    "CP2K",
    "LAMMPS",
    "GROMACS",
    "RDKit",
    "Open Babel",
    "ASE",
    "Multiwfn",
    "DFT",
    "TD-DFT",
    "molecular dynamics",
    "metadynamics",
    "NEB",
    "IRC",
    "frequency calculation",
)

EVIDENCE_TERMS = (
    "barrier",
    "free energy",
    "activation energy",
    "transition state",
    "spectrum",
    "yield",
    "selectivity",
    "control experiment",
    "oscillator strength",
    "frequency",
    "reaction coordinate",
    "rate",
    "binding energy",
    "formation energy",
)


def extract_records(
    papers: list[dict[str, Any]],
    asset_manifest: list[dict[str, Any]] | None = None,
    include_review: bool = False,
) -> list[dict[str, Any]]:
    assets = {item["paper_id"]: item for item in asset_manifest or []}
    output: list[dict[str, Any]] = []
    for paper in papers:
        decision = (paper.get("screening") or {}).get("decision")
        if decision != "pass" and not include_review:
            continue
        asset = assets.get(paper["paper_id"], {})
        text, provenance = collect_text(paper, asset)
        record = heuristic_extract(paper, text)
        record["assets"] = _asset_metadata(asset)
        record["extraction"] = {
            "method": "heuristic+curator_override" if asset.get("curation") else "heuristic",
            "text_sources": provenance,
            "requires_expert_review": not bool(asset.get("curation")),
        }
        if asset.get("curation"):
            record = merge_dict(record, read_json(asset["curation"]))
        errors = validate_scientific_record(record, require_task_selection=False)
        record["schema_validation"] = {"passed": not errors, "errors": errors}
        output.append(record)
    return output


def collect_text(paper: dict[str, Any], asset: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    chunks = [paper.get("title", ""), paper.get("abstract", "")]
    provenance: list[dict[str, Any]] = [
        {"kind": "metadata", "source": paper.get("retrieval_sources", [])}
    ]
    paths = []
    if asset.get("paper"):
        paper_path = Path(asset["paper"])
        if asset.get("prefer_text_assets"):
            provenance.append(_source_reference("paper", paper_path))
        else:
            paths.append(("paper", asset["paper"]))
    for path in asset.get("supplementary", []):
        paths.append(("supplementary", path))
    for path in asset.get("text", []):
        paths.append(("text", path))

    for kind, raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            provenance.append({"kind": kind, "path": str(path), "status": "missing"})
            continue
        if path.suffix.casefold() == ".pdf":
            content = pdf_to_text(path)
        else:
            content = path.read_text(encoding="utf-8", errors="replace")
        chunks.append(content)
        provenance.append(
            {
                "kind": kind,
                "path": str(path.resolve()),
                "sha256": sha256_file(path),
                "status": "read",
            }
        )
    return "\n\n".join(chunk for chunk in chunks if chunk), provenance


def _source_reference(kind: str, path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"kind": kind, "path": str(path), "status": "missing"}
    return {
        "kind": kind,
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "status": "referenced",
    }


def pdf_to_text(path: str | Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return result.stdout


def heuristic_extract(paper: dict[str, Any], text: str) -> dict[str, Any]:
    sentences = _sentences(text)
    classification = paper.get("corpus_classification") or {}
    coverage = paper.get("software_coverage") or {}
    covered_software = [
        item.get("raw_name") or item.get("normalized_name")
        for item in coverage.get("core_software", [])
        if item.get("raw_name") or item.get("normalized_name")
    ]
    classified_methods = (
        covered_software
        or classification.get("software", []) + classification.get("methods", [])
    )
    methods = list(dict.fromkeys(classified_methods))
    if not methods:
        methods = [
            term
            for term in METHOD_TERMS
            if re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text, re.I)
        ]
    evidence_sentences = _sentences_with_terms(sentences, EVIDENCE_TERMS)[:20]
    evidence = [
        {
            "evidence_id": f"ev_{index:03d}",
            "statement": sentence,
            "source": "paper_text",
            "source_locator": {"sentence_index": sentences.index(sentence)},
            "verification_status": "described",
        }
        for index, sentence in enumerate(evidence_sentences, start=1)
    ]
    controls = _sentences_with_terms(sentences, ("without", "dark", "control", "absence", "TEMPO"))[
        :8
    ]
    hypotheses = _sentences_with_terms(
        sentences, ("hypothesis", "mechanism", "pathway", "propose", "suggest", "may involve")
    )[:8]
    information_richness = dict(classification.get("information_richness") or {})
    information_richness.update(
        {
            "extracted_method_count": len(methods),
            "extracted_evidence_count": len(evidence),
            "extracted_control_count": len(controls),
            "extracted_hypothesis_count": len(hypotheses),
        }
    )
    return {
        "paper_id": paper["paper_id"],
        "paper": {
            key: paper.get(key)
            for key in ("title", "doi", "authors", "year", "venue", "url", "pdf_url")
        },
        "central_problem": paper.get("abstract") or paper.get("title", ""),
        "inputs": [],
        "expected_outputs": [],
        "methods": methods,
        "tools": methods,
        "evidence": evidence,
        "controls": controls,
        "hypotheses": hypotheses,
        "workflow": [],
        "reference_results": [],
        "runtime": {"estimated_walltime_hours": None, "runtime_tier": "unknown"},
        "information_richness": information_richness,
        "preliminary_task_suitability": classification.get("task_suitability_scores", {}),
        "source_classification": classification,
        "software_coverage": coverage,
        "computation_completeness": paper.get("computation_completeness", {}),
        "resource_limits": paper.get("resource_limits", {}),
        "study_bundle": paper.get("study_bundle", {}),
        "curation": {"status": "machine_draft", "reviewers": [], "notes": []},
    }


def _sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text)
    return [
        item.strip() for item in re.split(r"(?<=[.!?])\s+", normalized) if len(item.strip()) > 30
    ]


def _sentences_with_terms(sentences: list[str], terms: tuple[str, ...]) -> list[str]:
    lowered = tuple(term.casefold() for term in terms)
    return [
        sentence for sentence in sentences if any(term in sentence.casefold() for term in lowered)
    ]


def _asset_metadata(asset: dict[str, Any]) -> dict[str, Any]:
    output = {key: value for key, value in asset.items() if key != "curation"}
    if asset.get("curation"):
        output["curation"] = str(Path(asset["curation"]).resolve())
    return output
