"""Offline replay client for the live demos: same shape as anthropic.Anthropic() for the calls the demos use.

Every demo calls `get_client(responder)`. With ANTHROPIC_API_KEY set (and DEMO_OFFLINE unset) you get the real
client. Otherwise you get a ReplayClient that answers from a scripted `responder` so the demo still runs on stage
with no key or no Wi-Fi. Offline output is canned: it shows the *mechanics* (loop, tools, JSON, tokens), not a
real model. Every offline run prints a banner saying so.

    DEMO_OFFLINE=1 python week2/support_agent.py "..."   # force offline even with a key

A responder is `fn(kwargs, call_no) -> dict` built with text(...) / tool(...) / reply(...).
"""
import itertools
import json
import os
import sys
import time
from types import SimpleNamespace as NS

_ids = itertools.count(1)


def offline_mode():
    return os.environ.get("DEMO_OFFLINE") == "1" or not os.environ.get("ANTHROPIC_API_KEY")


def text(t):
    return {"type": "text", "text": t}


def tool(name, input_):
    return {"type": "tool_use", "name": name, "input": input_}


def reply(*blocks, stop=None):
    stop = stop or ("tool_use" if any(b["type"] == "tool_use" for b in blocks) else "end_turn")
    return {"content": list(blocks), "stop_reason": stop}


def approx_tokens(obj):
    """Rough count (about 4 characters a token) for offline /tokens. Real counts come from the API."""
    return max(1, len(json.dumps(obj, default=str)) // 4)


def _block(b):
    if b["type"] == "tool_use":
        return NS(type="tool_use", id=f"toolu_offline_{next(_ids):03d}", name=b["name"], input=b["input"])
    return NS(type="text", text=b["text"])


class _Messages:
    def __init__(self, responder, usage):
        self._responder, self._usage, self.calls = responder, usage, 0

    def create(self, **kw):
        self.calls += 1
        spec = self._responder(kw, self.calls)
        content = [_block(b) for b in spec["content"]]
        inp = approx_tokens([kw.get("system"), kw.get("messages"), kw.get("tools")])
        usage = self._usage(kw, self.calls, inp, spec)
        return NS(id=f"msg_offline_{self.calls:03d}", content=content, stop_reason=spec["stop_reason"],
                  model=kw.get("model"), usage=usage)

    def stream(self, **kw):
        return _Stream(self.create(**kw))

    def count_tokens(self, **kw):
        return NS(input_tokens=approx_tokens([kw.get("system"), kw.get("messages"), kw.get("tools")]))


class _Stream:
    def __init__(self, msg):
        self._msg = msg

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    @property
    def text_stream(self):
        for b in self._msg.content:
            if b.type == "text":
                for word in b.text.split(" "):
                    time.sleep(0.03)
                    yield word + " "

    def get_final_message(self):
        return self._msg


def _default_usage(kw, call_no, inp, spec):
    out = approx_tokens(spec["content"])
    return NS(input_tokens=inp, output_tokens=out, cache_creation_input_tokens=0, cache_read_input_tokens=0)


class ReplayClient:
    def __init__(self, responder, usage=_default_usage):
        self.messages = _Messages(responder, usage)


def get_client(responder, usage=_default_usage):
    if offline_mode():
        print("[OFFLINE replay: canned responses, no API call. Set ANTHROPIC_API_KEY for the live model.]",
              file=sys.stderr)
        return ReplayClient(responder, usage)
    import anthropic
    return anthropic.Anthropic()
