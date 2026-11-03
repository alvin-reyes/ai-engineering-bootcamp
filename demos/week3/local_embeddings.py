"""Week 3 demo: private, local embeddings. Nothing leaves your machine.

    python local_embeddings.py                    # uses sentence-transformers if installed, else TF-IDF
    EMBED_BACKEND=tfidf python local_embeddings.py   # force the pure-Python fallback (no install, no network)

Backend 'st' = sentence-transformers with a small open model (default all-MiniLM-L6-v2, set EMBED_MODEL to change).
The first run downloads the model once from Hugging Face; after that it runs with no network.
Optional install (not in requirements.txt):  pip install sentence-transformers
The same 13 answerable eval questions from rag_eval.py are used, so the numbers are comparable.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag_eval import CASES, chunks, recall_at_k, tfidf_retriever  # noqa: E402

MODEL = os.environ.get("EMBED_MODEL", "all-MiniLM-L6-v2")


def st_retriever(chunks_):
    """Meaning search with a local open-weight embedding model. Raises ImportError / OSError if unavailable."""
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer(MODEL)
    ids = list(chunks_)
    chunk_vecs = model.encode([chunks_[c] for c in ids], convert_to_tensor=True, normalize_embeddings=True)

    def retrieve(q, k):
        qv = model.encode(q, convert_to_tensor=True, normalize_embeddings=True)
        sims = util.cos_sim(qv, chunk_vecs)[0].tolist()
        return [c for _, c in sorted(zip(sims, ids), reverse=True)][:k]
    return retrieve


def pick_backend(chunks_):
    """Returns (name, retriever). EMBED_BACKEND=tfidf skips the model entirely."""
    if os.environ.get("EMBED_BACKEND", "auto") != "tfidf":
        try:
            return f"sentence-transformers ({MODEL})", st_retriever(chunks_)
        except Exception as e:  # not installed, or no network for the first download
            print(f"[local model unavailable: {type(e).__name__}; falling back to TF-IDF]")
    return "tfidf (pure Python)", tfidf_retriever(chunks_)


if __name__ == "__main__":
    cs = chunks()
    baseline = tfidf_retriever(cs)
    name, retriever = pick_backend(cs)
    print(f"Backend that ran: {name}")
    print("Your documents and questions are embedded on this machine; nothing is sent to any API.\n")
    for label, r in (("tf-idf (keywords)", baseline), (f"this backend", retriever)):
        print(f"{label:18s} recall@1 = {recall_at_k(CASES, r, 1):.0%}   recall@2 = {recall_at_k(CASES, r, 2):.0%}")
    print("\nThe three paraphrase questions (same meaning, different words):")
    for q, c in CASES[10:13]:
        print(f"  {q!r}\n    expected {c}   tf-idf -> {baseline(q, 1)[0]}   backend -> {retriever(q, 1)[0]}")
