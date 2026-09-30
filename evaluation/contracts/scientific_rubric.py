"""Optional flat scientific weighting: structure only, no scientific gates."""
import math


def scientific_rubric(document):
    """Validate optional flat weights, never rule applicability or dependencies."""
    rubric = document.get("scientific_rubric")
    if rubric is None:
        return None
    if not isinstance(rubric, list) or not rubric:
        raise ValueError("scientific_rubric must be a nonempty list")
    known = {r["rule_id"] for r in document["rules"]}
    ids, total = set(), 0
    for item in rubric:
        if not isinstance(item, dict) or set(item) - {"id", "max_score", "description", "rule_ids"}:
            raise ValueError("scientific_rubric supports only id/max_score/description/rule_ids")
        identifier, maximum = item.get("id"), item.get("max_score")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in ids:
            raise ValueError("scientific_rubric ids must be nonempty and unique")
        if (isinstance(maximum, bool) or not isinstance(maximum, (int, float)) or not math.isfinite(maximum)) or maximum <= 0:
            raise ValueError("scientific_rubric max_score must be finite and positive")
        if not isinstance(item.get("description"), str) or not item["description"].strip():
            raise ValueError("scientific_rubric description is required")
        links = item.get("rule_ids")
        if not isinstance(links, list) or not links or any(not isinstance(r, str) or r not in known for r in links) or len(set(links)) != len(links):
            raise ValueError("scientific_rubric rule_ids must name existing rules without duplicates")
        ids.add(identifier)
        total += maximum
    if abs(total - 100) > 1e-9:
        raise ValueError("scientific_rubric max_score must sum to 100")
    return rubric
