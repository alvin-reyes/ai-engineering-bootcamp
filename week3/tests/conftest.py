"""Shared test helpers. No API key and no network: a fake client stands in for the model.

The fake mimics the shape of anthropic.Anthropic().messages.create(...) and answers from the chunks it is
given (like a well-behaved model would): it quotes the best matching sentence and cites the chunk id, or says
"I don't know" when no sentence shares at least two question words. It is NOT a quality model: it only lets
the tests check your wiring (prompt, citations, "I don't know", eval maths).
"""
import re
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
STOP = set("a an the is are to of for in on at and or how what when do does i my must be by with within it "
           "you your we our can".split())


def _words(text):
    return {w for w in re.findall(r"[a-z0-9-]+", text.lower()) if w not in STOP and len(w) > 2}


def fake_model_reply(prompt: str) -> str:
    chunks = re.findall(r'<chunk id="([^"]+)">\n(.*?)\n</chunk>', prompt, re.S)
    question = prompt.rsplit("Question:", 1)[1]
    qwords = _words(question)
    best = []
    for cid, body in chunks:
        for sentence in re.split(r"(?<=\.)\s+", body.replace("\n", " ")):
            overlap = len(qwords & _words(sentence))
            if overlap >= 2:
                best.append((overlap, cid, sentence.strip()))
    if not best:
        return "I don't know: the chunks do not answer this question."
    best.sort(key=lambda t: -t[0])
    top = [b for b in best if b[0] == best[0][0]][:2]
    return " ".join(f"{sent} [{cid}]" for _, cid, sent in top)


class FakeClient:
    """Records every call in .calls; reply defaults to fake_model_reply."""

    def __init__(self, reply_fn=fake_model_reply):
        self.calls = []
        self._reply_fn = reply_fn
        self.messages = NS(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        text = self._reply_fn(kwargs["messages"][0]["content"])
        return NS(content=[NS(type="text", text=text)], stop_reason="end_turn")


@pytest.fixture
def fake_client():
    return FakeClient()


@pytest.fixture
def docs_dir():
    return FIXTURES / "docs"


@pytest.fixture
def eval_path():
    return FIXTURES / "eval_set.jsonl"


@pytest.fixture
def chunks(docs_dir):
    from docsqa.ingest import ingest
    return ingest(docs_dir)


@pytest.fixture
def retriever(chunks):
    from docsqa.retrieve import Retriever
    return Retriever(chunks)
