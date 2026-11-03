"""Week 3 demo: retrieval, recall@k, and a grounded answer with citations.

    python rag_eval.py                 # offline: compare two retrievers with recall@k (no API key needed)
    python rag_eval.py --ask "How fast must I report a stolen laptop?"   # retrieve + answer with citations

Retrievers: plain word overlap vs TF-IDF (keyword weighting). In real systems you would add an embedding
(vector) retriever and combine them (hybrid search); the eval works the same way.
"""
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos folder, for offline.py
from offline import get_client, reply, text  # noqa: E402

DOCS = Path(__file__).parent / "docs"
STOP = set("a an the is are to of for in on at and or how what when do i my must be by with within".split())

# Eval set: real questions with the chunk that answers them. "unanswerable" cases have no chunk.
CASES = [
    ("How long do I have to submit expenses?", "Expenses"),
    ("What is the daily meal allowance when travelling?", "Expenses"),
    ("Do I need a receipt for a 40 EUR taxi?", "Expenses"),
    ("How far ahead should I book flights?", "Travel"),
    ("Can I fly business class to Berlin?", "Travel"),
    ("Where do I order an XK-2041?", "Equipment"),
    ("How fast must I report a stolen laptop?", "Equipment"),
    ("How many vacation days do I get?", "Leave"),
    ("I was sick for 5 days, what do I need?", "Leave"),
    ("Should I turn on 2FA for the VPN?", "Security"),
    # paraphrases: same meaning, different words. Keyword retrievers miss these; embeddings (vectors) catch them.
    ("What do I do if my computer gets stolen?", "Equipment"),
    ("Can I take the train to Lyon instead?", "Travel"),
    ("How much holiday do I have per year?", "Leave"),
    ("What is the company's parental leave policy?", None),  # not in the docs: should say so
]


def chunks():
    text = "\n".join(p.read_text() for p in sorted(DOCS.glob("*.md")))
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", text, re.S | re.M)}


def words(text):
    return [w for w in re.findall(r"[a-z0-9-]+", text.lower()) if w not in STOP]


def overlap_retriever(chunks_):
    def retrieve(q, k):
        qs = set(words(q))
        return sorted(chunks_, key=lambda c: -len(qs & set(words(chunks_[c]))))[:k]
    return retrieve


def tfidf_retriever(chunks_):
    tfs = {c: Counter(words(t)) for c, t in chunks_.items()}
    df = Counter(w for tf in tfs.values() for w in tf)
    idf = {w: math.log(len(tfs) / n) + 1 for w, n in df.items()}
    def retrieve(q, k):
        qs = words(q)
        score = lambda c: sum(tfs[c][w] * idf.get(w, 0) for w in qs) / (1 + sum(tfs[c].values())) ** 0.5
        return sorted(tfs, key=lambda c: -score(c))[:k]
    return retrieve


def recall_at_k(cases, retrieve, k):
    """Share of answerable questions whose expected chunk is in the top k results."""
    answerable = [(q, c) for q, c in cases if c]
    hits = sum(c in retrieve(q, k) for q, c in answerable)
    return hits / len(answerable)


SYSTEM = ("Answer only from the chunks. Cite the chunk id in brackets after each claim, like [Travel]. "
          "If the chunks don't answer the question, say you don't know.")


def offline_responder(kwargs, call_no):
    """Canned stand-in for the model: answers from the retrieved chunks and cites them (mechanics only)."""
    prompt = kwargs["messages"][0]["content"]
    found = re.findall(r'<chunk id="([^"]+)">\n(.*?)\n</chunk>', prompt, re.S)
    question = prompt.rsplit("Question:", 1)[1]
    qs = {w for w in words(question) if len(w) > 2}
    best = []
    for cid, body in found:
        for sentence in re.split(r"(?<=\.)\s+", body.replace("\n", " ")):
            overlap = len(qs & {w for w in words(sentence) if len(w) > 2})
            if overlap:
                best.append((overlap, cid, sentence.strip()))
    best.sort(key=lambda t: -t[0])
    if not best or best[0][0] < 2:
        return reply(text("I don't know: the retrieved chunks do not answer this question."))
    top = [b for b in best if b[0] == best[0][0]][:2]
    return reply(text(" ".join(f"{sent} [{cid}]" for _, cid, sent in top)))


def answer(question, retrieve, chunks_, k=2):
    context = "\n\n".join(f'<chunk id="{c}">\n{chunks_[c]}\n</chunk>' for c in retrieve(question, k))
    client = get_client(offline_responder)
    response = client.messages.create(
        model=os.environ.get("DEMO_MODEL", "claude-opus-5-5"),
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"{context}\n\nQuestion: {question}"}],
    )
    return next((b.text for b in response.content if b.type == "text"), "")


if __name__ == "__main__":
    cs = chunks()
    retrievers = {"word overlap": overlap_retriever(cs), "tf-idf": tfidf_retriever(cs)}
    if "--ask" in sys.argv:
        print(answer(" ".join(sys.argv[sys.argv.index("--ask") + 1:]), retrievers["tf-idf"], cs))
    else:
        for name, r in retrievers.items():
            print(f"{name:13s} recall@1 = {recall_at_k(CASES, r, 1):.0%}   recall@2 = {recall_at_k(CASES, r, 2):.0%}")
        for name, r in retrievers.items():
            misses = [(q, c, r(q, 1)[0]) for q, c in CASES if c and c not in r(q, 1)]
            print(f"\nMisses at k=1 ({name}):" + ("" if misses else " none"))
            for q, c, got in misses:
                print(f"  {q!r}: expected {c}, got {got}")
