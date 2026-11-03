"""Week 2 demo: the SAME support tools as support_agent.py, served over MCP (Model Context Protocol).

    python mcp_server.py        # speaks MCP over stdio; you normally do NOT run it by hand: a client launches it
    python mcp_client.py        # launches this server, lists its tools, calls them (no model, no API key)

Write the tools once; any MCP client (Claude Code, Claude Desktop, your own agent) can use them. Add it to
Claude Code with (run from the demos folder; VERIFY the path on your machine):

    claude mcp add support -- python3 /full/path/to/demos/week2/mcp_server.py

The tools here are read-only except draft_refund, which only DRAFTS: it never refunds anything. Real refunds
stay behind a human, as in support_agent.py. All data is made up.

Install: pip install mcp   (optional; not in requirements.txt). Tested with mcp 2.3.0, where the server class
is mcp.server.mcpserver.MCPServer. In mcp 1.x the same class is mcp.server.fastmcp.FastMCP; the fallback import
below covers it. VERIFY the 1.x path if your install is 1.x (not tested here).

Never print to stdout in this file: over stdio, stdout IS the protocol channel.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # the demos/ folder

try:
    from mcp.server.mcpserver import MCPServer          # mcp 2.x
    from mcp.server.mcpserver.exceptions import ToolError
except ImportError:                                      # mcp 1.x  (VERIFY: not run here)
    from mcp.server.fastmcp import FastMCP as MCPServer
    from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations

import support_agent as sa  # noqa: E402  (reuse the same fake data, so the two demos agree)

mcp = MCPServer("support-tools", log_level="WARNING")  # quiet: stderr shows in the client's terminal
READ_ONLY = ToolAnnotations(read_only_hint=True)  # a hint to clients; your code still enforces what is allowed


@mcp.tool(annotations=READ_ONLY)
def get_order(order_id: str) -> str:
    """Look up one order by id. Use for any question about an order's status or contents.
    Order ids look like ORD-1234. Read-only."""
    content, is_error = sa.get_order(order_id)
    if is_error:
        raise ToolError(content)           # becomes an is_error result the model can read
    return content


@mcp.tool(annotations=READ_ONLY)
def search_help(query: str) -> str:
    """Search the help center for policy questions (refunds, shipping, returns).
    Not for questions about a specific order. Read-only."""
    content, is_error = sa.search_help(query)
    if is_error:
        raise ToolError(content)
    return content


@mcp.tool()
def draft_refund(order_id: str, reason: str) -> str:
    """Draft a refund request for a human to approve. Only after checking the order and the refund policy.
    This tool never refunds anything: it only records a draft."""
    if sa.ORDERS.get(order_id.strip().upper()) is None:
        raise ToolError(f"No order {order_id!r}. Order ids look like ORD-1001.")
    return json.dumps({"draft": f"REFUND-DRAFT-{order_id.strip().upper()}", "reason": reason,
                       "status": "DRAFT: nothing refunded; waiting for a human to approve"})


if __name__ == "__main__":
    mcp.run(transport="stdio")
