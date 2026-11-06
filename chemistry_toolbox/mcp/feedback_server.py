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
        from .call_provenance import CALL_PROVENANCE, request_provenance
        try:
            context = self.get_context()
            request_id = str(context.request_id)
            meta = context.request_context.meta
            meta = meta.model_dump() if meta is not None else None
        except (ValueError, LookupError, RuntimeError):
            request_id = None
            meta = None
        token = MCP_REQUEST_ID.set(request_id)
        origin_token = CALL_PROVENANCE.set(request_provenance(meta, request_id))
        try:
            result = await super().call_tool(name, arguments)
            from .response_policy import compact_enabled, MAX_RESPONSE_BYTES, response_bytes
            if compact_enabled():
                import json
                from mcp.types import TextContent
                from .response_projection import bounded_projection
                # After FastMCP normalization, including validation/extra metadata.
                content = result[0] if isinstance(result, tuple) else result
                if isinstance(content, list) and len(content) == 1 and isinstance(content[0], TextContent):
                    try:
                        value = json.loads(content[0].text)
                    except (ValueError, TypeError):
                        value = {"status": "success", "content": content[0].text}
                    if isinstance(value, dict) and response_bytes(value) > MAX_RESPONSE_BYTES:
                        value = bounded_projection(value, name)
                        return [TextContent(type="text", text=json.dumps(value, ensure_ascii=False))]
            return result
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
            CALL_PROVENANCE.reset(origin_token)
            MCP_REQUEST_ID.reset(token)
