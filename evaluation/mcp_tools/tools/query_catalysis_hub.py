"""MCP tool: query reaction energetics from Catalysis-Hub GraphQL."""

from __future__ import annotations

import json

from ..adapters.http import post_json
from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="query_catalysis_hub",
    description="Query bounded Catalysis-Hub reaction records by reactants and/or products.",
    category="external_data",
    backend="Catalysis-Hub GraphQL API",
    tags=("catalysis", "reaction_energy", "surface"),
    requires_network=True,
    side_effects=("external Catalysis-Hub request",),
)


def query_catalysis_hub_core(
    reactants: str = "",
    products: str = "",
    limit: int = 10,
) -> dict:
    if not reactants.strip() and not products.strip():
        raise ValueError("provide reactants and/or products")
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    filters = []
    if reactants:
        filters.append(f"reactants: {json.dumps(reactants)}")
    if products:
        filters.append(f"products: {json.dumps(products)}")
    filters.append(f"first: {limit}")
    query = """
    { reactions(%s) {
        totalCount
        edges { node {
            id Equation chemicalComposition surfaceComposition facet
            reactants products reactionEnergy activationEnergy dftCode dftFunctional
        } }
    } }
    """ % ", ".join(filters)
    response = post_json("https://api.catalysis-hub.org/graphql", {"query": query})
    if response.get("errors"):
        raise RuntimeError(f"Catalysis-Hub GraphQL error: {response['errors']}")
    value = response.get("data", {}).get("reactions", {})
    return {
        "status": "success",
        "backend": "Catalysis-Hub GraphQL API",
        "total_count": value.get("totalCount"),
        "records": [edge.get("node", {}) for edge in value.get("edges", [])],
    }


def register(mcp) -> None:
    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def query_catalysis_hub(reactants: str = "", products: str = "", limit: int = 10) -> dict:
        arguments = {"reactants": reactants, "products": products, "limit": limit}
        return execute_traced(TOOL_SPEC.name, arguments, lambda: query_catalysis_hub_core(**arguments))

