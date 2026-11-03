"""Shared test helpers. No API key and no network: every model call goes to FakeClient.

FakeClient mimics the part of `anthropic.Anthropic().messages.create` that this week's code uses, including the
usage fields and a simple prompt-cache accounting (a system prompt seen before is a cache read). It is a test
double, not the real API: real token counts come from the API.
"""
import time
from types import SimpleNamespace as NS

import pytest


def approx_tokens(obj) -> int:
    return max(1, len(str(obj)) // 4)


def text_block(t):
    return NS(type="text", text=t)


def tool_block(name, input_, id_="toolu_fake_1"):
    return NS(type="tool_use", id=id_, name=name, input=input_)


class FakeMessages:
    def __init__(self, replies, delay, fail):
        self.replies, self.delay, self.fail = list(replies or []), delay, fail
        self.calls, self._seen = [], set()

    def create(self, **kw):
        self.calls.append(kw)
        if self.delay:
            time.sleep(self.delay)
        if self.fail is not None:
            raise self.fail
        content = self.replies.pop(0) if self.replies else [text_block("ok")]
        stop = "tool_use" if any(b.type == "tool_use" for b in content) else "end_turn"
        system, msgs = kw.get("system", ""), kw.get("messages", [])
        if "cache_control" in kw:
            prefix, hit = approx_tokens(system), str(system) in self._seen
            self._seen.add(str(system))
            usage = NS(input_tokens=approx_tokens(msgs), output_tokens=20,
                       cache_creation_input_tokens=0 if hit else prefix,
                       cache_read_input_tokens=prefix if hit else 0)
        else:
            usage = NS(input_tokens=approx_tokens(system) + approx_tokens(msgs), output_tokens=20,
                       cache_creation_input_tokens=0, cache_read_input_tokens=0)
        return NS(id="msg_fake", content=content, stop_reason=stop, model=kw.get("model"), usage=usage)


class FakeClient:
    def __init__(self, replies=None, delay=0.0, fail=None):
        self.messages = FakeMessages(replies, delay, fail)

    @property
    def calls(self):
        return self.messages.calls


@pytest.fixture
def make_client():
    """make_client(replies=[[blocks], ...], delay=0.0, fail=None) -> FakeClient"""
    return FakeClient


@pytest.fixture
def blocks():
    return NS(text=text_block, tool=tool_block)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Every test starts with no key, no token and no offline flag set."""
    for name in ("ANTHROPIC_API_KEY", "ASK_TOKEN", "DEMO_OFFLINE", "APP_VERSION", "MODEL"):
        monkeypatch.delenv(name, raising=False)
