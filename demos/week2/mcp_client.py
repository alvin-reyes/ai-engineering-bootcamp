"""Week 2 demo: connect to an MCP server over stdio, list its tools and call them. No model, no API key.

    python mcp_client.py                 # starts mcp_server.py as a subprocess and talks to it

This is what Claude Code or Claude Desktop does when you add a server: start it, ask "what tools do you have?"
(tools/list), and call a tool when the model asks for one (tools/call). Here a few lines of Python play the client.
Tested with mcp 2.3.0 (`Client`). VERIFY the 1.x fallback below if your install is 1.x (not run here).
"""
import asyncio
import json
import os
import sys

SERVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")


def show(result):
    text = " ".join(getattr(c, "text", str(c)) for c in result.content)
    return ("ERROR " if result.is_error else "") + text


async def main_v2():
    from mcp import Client, StdioServerParameters
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    async with Client(params) as client:
        tools = (await client.list_tools()).tools
        print(f"server offers {len(tools)} tools:")
        for t in tools:
            print(f"  - {t.name}: {(t.description or '').splitlines()[0]}")
            args = ", ".join(k + ("*" if k in t.input_schema.get("required", []) else "")
                             for k in t.input_schema["properties"])
            print(f"      arguments: {args}   (* = required)")
        print("\ncall get_order(ORD-1002):\n  " + show(await client.call_tool("get_order", {"order_id": "ORD-1002"})))
        print("\ncall get_order(ORD-9999):\n  " + show(await client.call_tool("get_order", {"order_id": "ORD-9999"})))
        print("\ncall draft_refund(ORD-1002):\n  " + show(await client.call_tool(
            "draft_refund", {"order_id": "ORD-1002", "reason": "Arrived damaged"})))


async def main_v1():  # mcp 1.x  (VERIFY: not run here)
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            print(f"server offers {len(tools)} tools:")
            for t in tools:
                print(f"  - {t.name}: {(t.description or '').splitlines()[0]}")
            r = await session.call_tool("get_order", {"order_id": "ORD-1002"})
            print("\ncall get_order(ORD-1002):\n  " + " ".join(c.text for c in r.content))


if __name__ == "__main__":
    try:
        import mcp  # noqa: F401
    except ImportError:
        sys.exit("The MCP SDK is not installed. Optional: pip install mcp")
    try:
        from mcp import Client  # noqa: F401  (mcp 2.x)
        asyncio.run(main_v2())
    except ImportError:
        asyncio.run(main_v1())
