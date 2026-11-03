"""A fake Anthropic client, so every test runs with no API key and no network.

Script what the "model" says, in order, with `fake.say(...)`. Both `messages.stream` and `messages.create`
take the next scripted item. Each call is recorded in `fake.calls` (with a snapshot of `messages`) so tests
can check what your app sent.
"""
from types import SimpleNamespace as NS

import pytest


class _Stream:
    def __init__(self, item):
        self.item = item

    def __enter__(self):
        if isinstance(self.item, Exception):
            raise self.item
        return self

    def __exit__(self, *exc):
        return False

    @property
    def text_stream(self):
        for word in self.item.content[0].text.split(" "):
            yield word + " "

    def get_final_message(self):
        return self.item


class _Messages:
    def __init__(self, owner):
        self.owner = owner

    def _next(self, method, kw):
        snap = dict(kw)
        snap["messages"] = list(kw["messages"])  # the app keeps appending to its list; keep what was sent
        self.owner.calls.append({"method": method, **snap})
        if not self.owner.queue:
            raise AssertionError("the app made more API calls than the test scripted")
        return self.owner.queue.pop(0)

    def stream(self, **kw):
        return _Stream(self._next("stream", kw))

    def create(self, **kw):
        item = self._next("create", kw)
        if isinstance(item, Exception):
            raise item
        return item


class FakeClient:
    def __init__(self):
        self.queue, self.calls = [], []
        self.messages = _Messages(self)

    def say(self, text, stop="end_turn", input_tokens=10, output_tokens=5):
        """Queue a reply."""
        self.queue.append(NS(content=[NS(type="text", text=text)], stop_reason=stop,
                             usage=NS(input_tokens=input_tokens, output_tokens=output_tokens)))
        return self

    def fail(self, exc):
        """Queue an error to be raised by the next call."""
        self.queue.append(exc)
        return self


@pytest.fixture
def fake():
    return FakeClient()


@pytest.fixture
def chunks():
    return []


@pytest.fixture
def make_assistant(fake, chunks):
    from assistant import Assistant

    def make(**kw):
        return Assistant(fake, write=chunks.append, **kw)

    return make


def api_error(kind):
    """Build a real anthropic error object without any network call."""
    import anthropic

    req = NS(method="POST", url="https://api.anthropic.com/v1/messages")   # stand-ins: no HTTP library needed
    if kind == "connection":
        return anthropic.APIConnectionError(request=req)
    status = {"rate_limit": 429, "bad_request": 400}[kind]
    resp = NS(status_code=status, headers={}, request=req, text="", json=lambda: {})
    cls = anthropic.RateLimitError if kind == "rate_limit" else anthropic.BadRequestError
    return cls("boom", response=resp, body=None)
