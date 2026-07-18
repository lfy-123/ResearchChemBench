"""External chemistry data actions."""

from __future__ import annotations

import os
from typing import Any

import httpx

from .common import module_version, request_parts, success, unavailable, unsupported


ACTIONS = {
    "search_compounds", "search_protein_structures", "search_materials",
    "search_catalysis_records",
}


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
    from mp_api.client import MPRester

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
    with MPRester(api_key) as client:
        documents = client.materials.summary.search(fields=fields, **criteria)[:limit]
    records = []
    for document in documents:
        if hasattr(document, "model_dump"):
            record = document.model_dump(mode="json")
        else:
            record = {field: getattr(document, field, None) for field in fields}
        if hasattr(document, "material_id"):
            record["material_id"] = str(document.material_id)
        records.append(record)
    return success(
        {"query": criteria, "count": len(records), "records": records},
        backend_version=module_version("mp-api"),
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
    graphql = """
    query Search($reactants: String, $products: String, $first: Int!) {
      reactions(reactants: $reactants, products: $products, first: $first) {
        totalCount
        edges { node { id reactants products reactionEnergy activationEnergy chemicalComposition surfaceComposition facet } }
      }
    }
    """
    response = httpx.post(
        "https://api.catalysis-hub.org/graphql",
        json={
            "query": graphql,
            "variables": {
                "reactants": reactants or None,
                "products": products or None,
                "first": first,
            },
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
    return unsupported(f"Unsupported data action/backend combination: {action_id}/{backend_id}")
