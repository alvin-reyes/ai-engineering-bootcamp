"""Week 3 demo: the same document, chunked three ways. How does retrieval change?

    python chunking.py          # no API key, no network

A question counts as a HIT when the top-ranked chunk contains the fact that answers it (a short phrase from the
handbook). Same retriever (TF-IDF from rag_eval.py), same questions; only the chunking changes.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag_eval import DOCS, tfidf_retriever  # noqa: E402

# question -> the phrase a chunk must contain to be useful
FACTS = [
    ("How long do I have to submit expenses?", "within 30 days"),
    ("What is the daily meal allowance when travelling?", "50 EUR per day"),
    ("Do I need a receipt for a 40 EUR taxi?", "over 25 EUR"),
    ("How far ahead should I book flights?", "14 days ahead"),
    ("How fast must I report a stolen laptop?", "within 24 hours"),
    ("Where do I order an XK-2041?", "IT catalogue"),
    ("How many vacation days do I get?", "25 days"),
    ("I was sick for 5 days, what do I need?", "doctor's note"),
    ("Should I turn on 2FA for the VPN?", "two-factor authentication"),
]


def whole_text():
    return "\n".join(p.read_text() for p in sorted(DOCS.glob("*.md")))


def fixed(text, size):
    """Cut every `size` characters, ignoring meaning."""
    return {f"f{i}": text[i:i + size] for i in range(0, len(text), size)}


def overlapping(text, size, overlap):
    """Like fixed, but each chunk starts `overlap` characters before the previous one ended."""
    step = size - overlap
    return {f"o{i}": text[i:i + size] for i in range(0, len(text), step) if text[i:i + size].strip()}


def by_heading(text):
    """One chunk per '## Heading' section, with the heading kept in the chunk (the title is a strong signal)."""
    return {m.group(1): m.group(1) + ". " + m.group(2).strip()
            for m in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", text, re.S | re.M)}


def score(chunks_, k=1):
    retrieve = tfidf_retriever(chunks_)
    hits, misses = 0, []
    for q, fact in FACTS:
        got = retrieve(q, k)
        if any(fact in chunks_[c] for c in got):
            hits += 1
        else:
            misses.append((q, fact, got[0]))
    return hits, misses


def show(name, chunks_):
    hits, misses = score(chunks_)
    sizes = [len(c) for c in chunks_.values()]
    print(f"{name:24s} chunks={len(chunks_):3d}  avg {sum(sizes)//len(sizes):3d} chars  "
          f"recall@1 = {hits}/{len(FACTS)} = {hits/len(FACTS):.0%}")
    return misses


if __name__ == "__main__":
    text = whole_text()
    print(f"Document: {len(text)} characters, {len(FACTS)} questions\n")
    results = {
        "fixed 150 chars": fixed(text, 150),
        "fixed 400 chars": fixed(text, 400),
        "fixed 150 + overlap 50": overlapping(text, 150, 50),
        "by heading": by_heading(text),
    }
    all_misses = {name: show(name, c) for name, c in results.items()}

    print("\nSweep: chunk size vs recall@1 (overlap = a quarter of the size)")
    print("  size  fixed  overlap")
    for size in (60, 100, 150, 200, 300, 400):
        a, _ = score(fixed(text, size))
        b, _ = score(overlapping(text, size, size // 4))
        print(f"  {size:4d}  {a}/{len(FACTS)}    {b}/{len(FACTS)}")
    print("Big chunks look good on a 905-character toy doc because there are only 3 of them; on a real doc they")
    print("also send more text to the model per question. That is why we measure on YOUR documents.")
    print("\nWhy fixed 150 breaks: facts get cut in half. Example boundary:")
    f = results["fixed 150 chars"]
    for q, fact in FACTS:
        if not any(fact in c for c in f.values()):
            print(f"  {fact!r} is split across two chunks, so no single chunk holds it")
            break
    print("\nMisses with fixed 150 chars:")
    for q, fact, got in all_misses["fixed 150 chars"]:
        print(f"  {q!r}: needs {fact!r}, top chunk was {got}")
    print("\nChunk by heading, first two:")
    for k_, v in list(results["by heading"].items())[:2]:
        print(f"  [{k_}] {v[:70]}...")
