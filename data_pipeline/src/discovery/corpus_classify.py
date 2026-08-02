from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

SOFTWARE_PATTERNS = {
    "Gaussian": (
        r"\bgaussian\s*(?:0[39]|1[6])\b",
        r"\bgaussian\s+(?:program|software|package|suite)\b",
    ),
    "ORCA": (r"\borca\b",),
    "VASP": (r"\bvasp\b", r"vienna ab[- ]initio simulation package"),
    "Quantum ESPRESSO": (r"quantum espresso", r"\bpwscf\b"),
    "CP2K": (r"\bcp2k\b",),
    "GROMACS": (r"\bgromacs\b",),
    "LAMMPS": (r"\blammps\b",),
    "AMBER": (r"\bamber(?:\s*\d+)?\b",),
    "NAMD": (r"\bnamd\b",),
    "OpenMM": (r"\bopenmm\b",),
    "CASTEP": (r"\bcastep\b",),
    "SIESTA": (r"\bsiesta\b",),
    "CRYSTAL": (
        r"\bcrystal(?:09|14|17|23)\b",
        r"\bcrystal\s+(?:program|code|package|suite)\b",
    ),
    "Q-Chem": (r"\bq-?chem\b",),
    "Turbomole": (r"\bturbomole\b",),
    "Multiwfn": (r"\bmultiwfn\b",),
    "RDKit": (r"\brdkit\b",),
    "Psi4": (r"\bpsi4\b",),
    "pymatgen": (r"\bpymatgen\b",),
}

METHOD_PATTERNS = {
    "DFT": (r"density functional theory", r"\bdft\b"),
    "TD-DFT": (r"time[- ]dependent density functional", r"\btd[- ]?dft\b"),
    "wavefunction": (r"coupled[- ]cluster", r"\bccsd(?:\(t\))?\b", r"\bmp2\b", r"multireference"),
    "molecular_dynamics": (r"molecular dynamics", r"\bmd simulations?\b"),
    "metadynamics": (r"metadynamics", r"well[- ]tempered metadynamics"),
    "transition_state": (r"transition state", r"intrinsic reaction coordinate", r"\birc\b"),
    "microkinetics": (r"microkinetic", r"reaction network"),
    "machine_learning_potential": (
        r"machine learning potential",
        r"neural force field",
        r"interatomic potential",
    ),
    "docking": (r"molecular docking", r"docking simulation"),
    "monte_carlo": (r"monte carlo",),
}

DOMAIN_PATTERNS = {
    "reaction_mechanism": (
        r"reaction mechanism",
        r"mechanistic",
        r"reaction pathway",
        r"activation barrier",
    ),
    "catalysis_surface": (
        r"heterogeneous catalysis",
        r"catalyst surface",
        r"adsorption energ",
        r"surface reaction",
    ),
    "materials_solid_state": (
        r"band structure",
        r"crystal structure",
        r"solid state",
        r"materials design",
        r"formation energy",
    ),
    "photochemistry_excited_state": (
        r"photochemical",
        r"excited state",
        r"photoinduced",
        r"oscillator strength",
    ),
    "biomolecular_simulation": (
        r"protein[- ]ligand",
        r"biomolecular",
        r"binding free energy",
        r"force field",
    ),
    "molecular_dataset_ml": (
        r"dataset",
        r"machine learning",
        r"data[- ]driven",
        r"benchmark dataset",
    ),
    "spectroscopy_properties": (
        r"spectroscop",
        r"nmr chemical shift",
        r"vibrational frequenc",
        r"electronic propert",
    ),
}


def classify_corpus_documents(
    documents: list[dict[str, Any]],
    relevance_pass: float = 45.0,
    relevance_review: float = 22.0,
    constructability_threshold: float = 55.0,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for document in documents:
        if document.get("duplicate_of"):
            duplicate = dict(document)
            duplicate["corpus_classification"] = {
                "decision": "duplicate",
                "relevance_score": 0.0,
                "eligible_task_types": [],
                "deep_parse_decision": "skip",
            }
            output.append(duplicate)
            continue

        text = _load_text(document)
        front = " ".join(
            [document.get("title", ""), document.get("abstract", ""), text[:30000]]
        ).casefold()
        full = text.casefold()
        headings = " ".join(document.get("section_headings", [])).casefold()

        software = _match_groups(full, SOFTWARE_PATTERNS)
        methods = _match_groups(full, METHOD_PATTERNS)
        domains = _match_groups(front, DOMAIN_PATTERNS)
        relevance, relevance_features = _relevance_score(front, full, headings, software, methods)
        article_type = _article_type(front, headings)
        computational_role = _computational_role(
            relevance, front, full, headings, software, methods
        )
        information_richness = _information_richness(front, full, headings)
        constructability = _constructability_scores(
            front,
            full,
            headings,
            software,
            methods,
            domains,
            article_type,
            computational_role,
            information_richness,
        )
        eligible_task_types = [
            task_type
            for task_type, score in constructability.items()
            if score >= constructability_threshold
        ]

        pending_ocr = (document.get("text_quality") or {}).get(
            "needs_ocr", False
        ) and not document.get("deep_text_path")
        if relevance >= relevance_pass:
            relevance_decision = "pass"
        elif relevance >= relevance_review:
            relevance_decision = "review"
        elif pending_ocr:
            relevance_decision = "review"
        else:
            relevance_decision = "reject"

        text_needs_ocr = pending_ocr
        max_constructability = max(constructability.values(), default=0.0)
        if document.get("deep_text_path"):
            deep_parse = "complete"
        elif text_needs_ocr:
            deep_parse = "required"
        elif relevance_decision == "reject":
            deep_parse = "skip"
        elif relevance_decision == "pass" and max_constructability >= constructability_threshold:
            deep_parse = "required"
        else:
            deep_parse = "optional"

        task_decision = "pass" if relevance_decision == "pass" and eligible_task_types else "review"
        record = dict(document)
        record["screening"] = {
            "decision": task_decision,
            "overall_score": max_constructability,
            "eligible_task_types": eligible_task_types,
            "task_type_scores": constructability,
            "review_required": True,
            "hard_failures": []
            if relevance_decision != "reject"
            else ["low computational chemistry relevance"],
        }
        record["corpus_classification"] = {
            "relevance_decision": relevance_decision,
            "relevance_score": relevance,
            "relevance_features": relevance_features,
            "computational_role": computational_role,
            "article_type": article_type,
            "software": software,
            "methods": methods,
            "domains": domains,
            "task_suitability_scores": constructability,
            "constructability_scores": constructability,
            "eligible_task_types": eligible_task_types,
            "eligible_modes": eligible_task_types,
            "information_richness": information_richness,
            "deep_parse_decision": deep_parse,
            "expert_review_required": True,
            "pending_ocr": pending_ocr,
        }
        output.append(record)
    return output


def classification_summary(documents: list[dict[str, Any]]) -> dict[str, Any]:
    relevance = Counter()
    deep_parse = Counter()
    roles = Counter()
    modes = Counter()
    domains = Counter()
    software = Counter()
    for document in documents:
        item = document.get("corpus_classification") or {}
        relevance[item.get("relevance_decision", item.get("decision", "unknown"))] += 1
        deep_parse[item.get("deep_parse_decision", "unknown")] += 1
        roles[item.get("computational_role", "unknown")] += 1
        modes.update(item.get("eligible_task_types", item.get("eligible_modes", [])))
        domains.update(item.get("domains", []))
        software.update(item.get("software", []))
    return {
        "documents": len(documents),
        "relevance": dict(relevance),
        "deep_parse": dict(deep_parse),
        "computational_roles": dict(roles),
        "eligible_task_types": dict(modes),
        "domains": dict(domains),
        "software": dict(software),
    }


def _load_text(document: dict[str, Any]) -> str:
    path = document.get("deep_text_path") or document.get("text_path")
    if not path or not Path(path).exists():
        return ""
    return Path(path).read_text(encoding="utf-8", errors="replace")


def _match_groups(text: str, groups: dict[str, tuple[str, ...]]) -> list[str]:
    return [
        name
        for name, patterns in groups.items()
        if any(re.search(pattern, text, re.I) for pattern in patterns)
    ]


def _relevance_score(
    front: str,
    full: str,
    headings: str,
    software: list[str],
    methods: list[str],
) -> tuple[float, dict[str, float]]:
    computational_section = bool(
        re.search(
            r"computational (?:methods|details)|theoretical methods|dft calculations|molecular dynamics simulations",
            headings,
        )
    )
    front_method_hits = sum(
        1
        for patterns in METHOD_PATTERNS.values()
        if any(re.search(pattern, front, re.I) for pattern in patterns)
    )
    repeated_method_hits = sum(
        1
        for patterns in METHOD_PATTERNS.values()
        if sum(len(re.findall(pattern, full, re.I)) for pattern in patterns) >= 3
    )
    primary_signals = _primary_computation_signals(front, full, headings)
    features = {
        "software": min(24.0, len(software) * 8.0),
        "method_diversity": min(20.0, len(methods) * 5.0),
        "front_matter_signal": min(24.0, front_method_hits * 8.0),
        "computational_section": 20.0 if computational_section else 0.0,
        "repeated_method_signal": min(12.0, repeated_method_hits * 4.0),
        "primary_computation_signal": min(24.0, primary_signals * 12.0),
    }
    return round(min(100.0, sum(features.values())), 1), features


def _article_type(front: str, headings: str) -> str:
    if re.search(r"\b(review|perspective|tutorial)\b", front[:5000]):
        return "review"
    if re.search(r"\b(dataset|database|data descriptor|data note)\b", front[:8000]):
        return "dataset"
    if re.search(r"\b(software|toolkit|package|platform|workflow engine)\b", front[:8000]):
        return "software_or_platform"
    if "materials and methods" in headings or "results" in headings:
        return "research_article"
    return "unknown"


def _computational_role(
    relevance: float,
    front: str,
    full: str,
    headings: str,
    software: list[str],
    methods: list[str],
) -> str:
    central = _primary_computation_signals(front, full, headings) > 0
    has_section = bool(re.search(r"computational|theoretical|molecular dynamics", headings))
    if relevance >= 55 and (central or has_section) and methods:
        return "primary"
    if relevance >= 35 and methods:
        return "secondary"
    if relevance >= 20:
        return "incidental"
    return "none"


def _constructability_scores(
    front: str,
    full: str,
    headings: str,
    software: list[str],
    methods: list[str],
    domains: list[str],
    article_type: str,
    role: str,
    richness: dict[str, Any],
) -> dict[str, float]:
    method_parameters = _count_terms(
        full,
        (
            "basis set",
            "functional",
            "force field",
            "k-point",
            "cutoff energy",
            "solvation model",
            "temperature",
            "time step",
        ),
    )
    availability = _count_terms(
        full,
        (
            "data availability",
            "code availability",
            "supporting information",
            "repository",
            "zenodo",
            "github",
        ),
    )
    process_signals = _count_terms(
        full,
        (
            "workflow",
            "optimization",
            "frequency",
            "sampling",
            "equilibration",
            "validation",
            "benchmark",
        ),
    )
    mechanism_signals = _count_terms(
        front + " " + headings,
        (
            "mechanism",
            "pathway",
            "transition state",
            "activation barrier",
            "intermediate",
            "radical",
            "control experiment",
            "kinetic",
        ),
    )
    evidence_signals = _count_terms(
        full,
        (
            "free energy",
            "barrier",
            "spectrum",
            "selectivity",
            "rate",
            "formation energy",
            "binding energy",
            "rmsd",
        ),
    )
    autonomy_signals = _count_terms(
        front,
        (
            "autonomous",
            "active-learning workflow",
            "active learning workflow",
            "simulation agent",
            "closed-loop",
        ),
    )
    primary_bonus = 18 if role == "primary" else 8 if role == "secondary" else 0
    type_penalty = (
        25 if article_type == "review" else 15 if article_type == "software_or_platform" else 0
    )

    reproduction = (
        primary_bonus
        + min(18, len(software) * 6)
        + min(22, method_parameters * 4)
        + min(18, availability * 6)
        + min(12, process_signals * 2)
        - type_penalty
    )
    autonomous = (
        primary_bonus
        + min(15, len(methods) * 4)
        + min(15, len(domains) * 5)
        + min(20, process_signals * 3)
        + min(20, evidence_signals * 3)
        + (
            10
            if re.search(r"we (?:identify|discover|demonstrate|investigate|predict)", front)
            else 0
        )
        + min(15, autonomy_signals * 8)
        - type_penalty
    )
    conclusion_guided = (
        primary_bonus
        + min(22, evidence_signals * 3)
        + min(18, richness["quantitative_result_signals"] * 3)
        + min(18, richness["conclusion_signals"] * 4)
        + min(18, mechanism_signals * 3)
        + min(12, availability * 4)
        - type_penalty
    )
    rule_discovery = (
        primary_bonus
        + min(25, richness["multi_system_signals"] * 5)
        + min(20, richness["trend_descriptor_signals"] * 4)
        + min(20, richness["quantitative_result_signals"] * 3)
        + min(15, richness["heldout_prediction_signals"] * 7)
        - type_penalty
    )
    return {
        "paper_reproduction": round(max(0.0, min(100.0, reproduction)), 1),
        "conclusion_guided_reconstruction": round(max(0.0, min(100.0, conclusion_guided)), 1),
        "autonomous_research": round(max(0.0, min(100.0, autonomous)), 1),
        "mechanistic_rule_discovery": round(max(0.0, min(100.0, rule_discovery)), 1),
    }


def _information_richness(front: str, full: str, headings: str) -> dict[str, Any]:
    return {
        "method_parameter_signals": _count_terms(
            full,
            (
                "basis set",
                "functional",
                "dispersion correction",
                "solvation model",
                "force field",
                "cutoff",
                "k-point",
                "time step",
                "convergence criterion",
            ),
        ),
        "input_asset_signals": _count_terms(
            full,
            (
                "input file",
                "coordinates",
                "geometry",
                "cif",
                "xyz",
                "trajectory",
                "initial structure",
                "source data",
                "repository",
            ),
        ),
        "conclusion_signals": _count_terms(
            front,
            (
                "we conclude",
                "we demonstrate",
                "we identify",
                "we reveal",
                "our results show",
                "we find that",
                "supports a mechanism",
            ),
        ),
        "quantitative_result_signals": _count_terms(
            full,
            (
                "kcal mol",
                "kj mol",
                "electronvolt",
                " ev",
                "angstrom",
                "barrier",
                "free energy",
                "selectivity",
                "rate constant",
                "binding energy",
            ),
        ),
        "competing_hypothesis_signals": _count_terms(
            full,
            (
                "alternative mechanism",
                "competing pathway",
                "ruled out",
                "excluded",
                "inconsistent with",
                "control experiment",
                "hypothesis",
            ),
        ),
        "multi_system_signals": _count_terms(
            full,
            (
                "series of",
                "across the",
                "multiple systems",
                "set of catalysts",
                "substrate scope",
                "materials series",
                "data set",
                "dataset",
            ),
        ),
        "trend_descriptor_signals": _count_terms(
            full,
            (
                "descriptor",
                "correlation",
                "scaling relation",
                "linear relationship",
                "trend",
                "structure-property",
                "structure activity",
            ),
        ),
        "heldout_prediction_signals": _count_terms(
            full + " " + headings,
            (
                "held-out",
                "holdout",
                "test set",
                "external validation",
                "prospective prediction",
                "blind prediction",
                "leave-one-out",
            ),
        ),
        "comparable_system_count": _estimate_comparable_system_count(full),
    }


def _estimate_comparable_system_count(text: str) -> int:
    matches = [
        int(value)
        for value in re.findall(
            r"\b(\d{1,3})\s+(?:molecules|compounds|catalysts|materials|systems|complexes|substrates)\b",
            text,
            re.I,
        )
        if int(value) <= 500
    ]
    return max(matches, default=0)


def _count_terms(text: str, terms: tuple[str, ...]) -> int:
    return sum(1 for term in terms if term in text)


def _primary_computation_signals(front: str, full: str, headings: str) -> int:
    search_text = front + " " + full[:80000]
    patterns = (
        r"(?:all|the|our|these)?\s*(?:dft|density functional theory|first[- ]principles|ab initio|quantum chemistry) calculations?\s+(?:were|was|are|is)\s+(?:performed|carried out|conducted|used)",
        r"(?:dataset|database).{0,240}(?:prepared|generated|constructed|computed).{0,160}(?:dft|density functional theory|first[- ]principles|quantum chemistry)",
        r"(?:dft|density functional theory|first[- ]principles).{0,160}(?:dataset|database).{0,160}(?:prepared|generated|constructed|computed)",
        r"workflow.{0,140}(?:dft|density functional theory|first[- ]principles|electronic structure|simulation)",
        r"we (?:performed|used|carried out|report|present).{0,120}(?:dft|molecular dynamics|simulation|calculations)",
        r"(?:forces|energies|properties).{0,160}(?:were|are).{0,40}calculated using (?:dft|density functional theory|coupled[- ]cluster|quantum chemistry)",
        r"(?:electronic structure|quantum chemistry) (?:code|calculations).{0,180}(?:psi4|q-?chem|gaussian|orca|dft|forces|energies)",
    )
    hits = sum(1 for pattern in patterns if re.search(pattern, search_text, re.I | re.S))
    if re.search(
        r"computational|theoretical|density functional theory calculations", headings, re.I
    ):
        hits += 1
    return hits
