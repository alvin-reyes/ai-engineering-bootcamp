"""STRETCH tests for mcp_server.py. Skipped if the `mcp` package is not installed (pip install mcp)."""
import asyncio
import os
import sys

import pytest

pytest.importorskip("mcp")
try:
    from mcp import Client, StdioServerParameters
except ImportError:
    pytest.skip("these tests use the mcp 2.x Client", allow_module_level=True)

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def _session(coro_fn):
    async def go():
        params = StdioServerParameters(command=sys.executable, args=[os.path.join(HERE, "mcp_server.py")], cwd=HERE)
        async with Client(params) as client:
            return await coro_fn(client)
    return asyncio.run(go())


def _text(result):
    return " ".join(getattr(c, "text", str(c)) for c in result.content)


def test_server_offers_the_three_tools():
    async def go(c):
        return {t.name for t in (await c.list_tools()).tools}
    assert _session(go) == {"get_order", "search_help", "draft_refund"}


def test_read_tool_works_and_errors_are_flagged():
    async def go(c):
        return (await c.call_tool("get_order", {"order_id": "ORD-1002"}),
                await c.call_tool("get_order", {"order_id": "ORD-9999"}))
    ok, bad = _session(go)
    assert not ok.is_error and "monitor" in _text(ok)
    assert bad.is_error and "ORD-9999" in _text(bad)


def test_refund_only_drafts():
    async def go(c):
        return await c.call_tool("draft_refund", {"order_id": "ORD-1002", "reason": "Arrived damaged"})
    result = _session(go)
    assert not result.is_error
    assert "DRAFT" in _text(result) and "nothing refunded" in _text(result).lower()
