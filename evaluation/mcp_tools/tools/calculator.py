"""MCP tool: evaluate reaction-energy arithmetic."""

from __future__ import annotations

from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="calculator",
    description="Safely evaluate numerical arithmetic expressions for reaction energies.",
    category="utility",
    backend="NumExpr",
    dependencies=("numexpr",),
    tags=("arithmetic", "reaction_energy"),
)


def register(mcp) -> None:
    # Keep optional/runtime imports out of module scope. The registry can then
    # inspect TOOL_SPEC even in an environment where the backend is not installed.
    import numexpr

    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def calculator(expression: str) -> str:
        def call() -> str:
            cleaned = expression.strip()
            if not cleaned:
                raise ValueError("Expression must not be empty")
            value = numexpr.evaluate(cleaned, global_dict={}, local_dict={})
            return str(value.item() if hasattr(value, "item") else value)

        return execute_traced(TOOL_SPEC.name, {"expression": expression}, call)
