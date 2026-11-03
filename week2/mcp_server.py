"""STRETCH (optional): serve your three tools over MCP. Skip this until the main build passes.

    pip install mcp
    python mcp_server.py          # speaks MCP over stdio; a client launches it. See ../../demos/week2/mcp_client.py
    pytest tests/test_mcp_stretch.py

Rules for this file:
  - Reuse your handlers from agent.py, so the agent and the server cannot disagree.
  - Read tools are read-only. draft_refund only DRAFTS: nothing is ever refunded, and the result says so.
  - Never print to stdout: over stdio, stdout IS the protocol. Errors become ToolError (the client sees is_error).
  - In your README say what this server can and cannot do.
Reference pattern: demos/week2/mcp_server.py (tested with mcp 2.3.0; in mcp 1.x the class is FastMCP).
"""
import agent


def build_server():
    """Return an MCP server with the three tools registered. Imports mcp here so this file imports without it."""
    try:
        from mcp.server.mcpserver import MCPServer                 # mcp 2.x
        from mcp.server.mcpserver.exceptions import ToolError
    except ImportError:                                             # mcp 1.x  (VERIFY)
        from mcp.server.fastmcp import FastMCP as MCPServer
        from mcp.server.fastmcp.exceptions import ToolError
    from mcp.types import ToolAnnotations

    server = MCPServer("my-support-tools", log_level="WARNING")
    read_only = ToolAnnotations(read_only_hint=True)
    # TODO: register get_order and search_help (annotations=read_only) and draft_refund with @server.tool().
    # The docstring becomes the tool description, so write it like your agent.py descriptions.
    # A handler error (is_error True) -> raise ToolError(content).
    # draft_refund returns text containing the word DRAFT and says nothing was refunded.
    _ = (agent, ToolError, read_only)
    return server


if __name__ == "__main__":
    build_server().run(transport="stdio")
