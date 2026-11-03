"""Prompt caching helpers: stable prefix first, anything that changes last.

    req = build_request(STABLE_RULES_AND_DOCS, question, dynamic=f"Today is {date}")
    tracer.call("ask", **req)

The request carries top-level cache_control (as in demos/week4/caching_demo.py), so the API caches the stable prefix.
The minimum cacheable length depends on the model: VERIFY on the caching docs. Real cache numbers come from the API.
"""
import os
import re  # noqa: F401

MODEL = os.environ.get("MODEL", "claude-opus-5-5")  # VERIFY the model id you will really use
CACHE_CONTROL = {"type": "ephemeral"}


def build_request(stable, question, dynamic="", *, model=MODEL, max_tokens=512, **extra) -> dict:
    """Keyword arguments for client.messages.create.

    `stable` (rules, tools text, documents) is the system prompt, byte for byte, and the request gets
    cache_control=CACHE_CONTROL. `dynamic` (date, user id, request id) must NOT go into `stable`: put it after the
    question in the user message, so it never changes the cached prefix. `extra` (tools=..., temperature=...) is
    passed through into the returned dict. The user message is {"role": "user", "content": ...} and starts with the question.
    """
    # TODO: implement
    raise NotImplementedError("build_request")


def find_volatile(text) -> list:
    """Things in `text` that probably change between calls: dates and timestamps (2026-12-01T10:00:00), clock times
    (14:35) and uuids. Returns the matched strings; [] means the text looks stable. Use it on your stable prefix."""
    # TODO: implement with re
    raise NotImplementedError("find_volatile")


def cache_hit_rate(rows) -> float:
    """Share of input tokens served from the cache over trace rows:
    cache_read / (cache_read + cache_write + input_tokens). 0 if there are no tokens."""
    # TODO: implement
    raise NotImplementedError("cache_hit_rate")
