"""Feedback for pre-dispatch schema errors as well as tool-body exceptions."""
from mcp.server.fastmcp import FastMCP

from chemistry_toolbox.src.execution_feedback import exception_feedback, feedback_schema_version


class FeedbackFastMCP(FastMCP):
    def tool(self, *args, **kwargs):
        if feedback_schema_version() == 2:
            # MCP's text+structured duplication doubles dense JSON when a host
            # renders the whole reply. The input contract stays fully typed.
            kwargs.setdefault("structured_output", False)
        return super().tool(*args, **kwargs)

    async def call_tool(self, name, arguments):
        from .tracing import MCP_REQUEST_ID
        try:
            request_id = str(self.get_context().request_id)
        except (ValueError, LookupError, RuntimeError):
            request_id = None
        token = MCP_REQUEST_ID.set(request_id)
        try:
            return await super().call_tool(name, arguments)
        except Exception as exc:
            if feedback_schema_version() != 2:
                raise
            # FastMCP wraps validation failures; preserve the actual origin.
            cause = exc.__cause__ or exc
            from .tracing import execute_traced
            value = execute_traced(name, arguments,
                lambda: exception_feedback(cause, tool=name, stage="dispatch"), capture_artifacts=False)
            import json
            from mcp.types import TextContent
            return [TextContent(type="text", text=json.dumps(value, ensure_ascii=False))]
        finally:
            MCP_REQUEST_ID.reset(token)
