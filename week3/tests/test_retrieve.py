"""Acceptance: keyword (TF-IDF) search, deterministic, with an optional embedding hook."""
from docsqa.retrieve import Retriever, tokenize


def test_tokenize_lowercases_and_drops_stop_words():
    assert tokenize("The Return-Policy: 30 days!") == ["return-policy", "30", "days"]


def test_best_chunk_first(retriever):
    cases = {
        "How many days do customers have to return an unused bike?": "returns.md#returns",
        "How much does express delivery cost?": "shipping.md#delivery-times",
        "How long is the battery warranty?": "warranty.md#battery-warranty",
        "When is the workshop open on Saturday?": "repairs.md#opening-hours",
        "How many days of annual leave do full-time staff get?": "staff-handbook.md#annual-leave",
    }
    for question, expected in cases.items():
        hits = retriever.search(question, k=3)
        assert hits[0].chunk.id == expected, question


def test_k_limits_results_and_scores_descend(retriever):
    hits = retriever.search("return refund shipping warranty", k=2)
    assert len(hits) == 2
    assert hits[0].score >= hits[1].score > 0


def test_no_overlap_means_no_hits(retriever):
    assert retriever.search("zzzz qqqq", k=5) == []


def test_rare_word_beats_common_word(chunks):
    # "norway" appears in one chunk only, "days" in many: the rare word must decide.
    top = Retriever(chunks).search("days norway", k=1)[0]
    assert top.chunk.id == "shipping.md#international-orders"


def test_deterministic(chunks):
    a = [h.chunk.id for h in Retriever(chunks).search("return a bike", 5)]
    b = [h.chunk.id for h in Retriever(chunks).search("return a bike", 5)]
    assert a == b


def test_embedding_hook_is_used(chunks):
    vocab = ["bike", "battery", "leave", "delivery"]
    calls = []

    def embed(texts):
        calls.append(len(texts))
        return [[t.lower().count(w) for w in vocab] for t in texts]

    r = Retriever(chunks, embed_fn=embed)
    hits = r.search("battery battery", k=2)
    assert calls == [len(chunks), 1]  # chunks embedded once at build, the query once per search
    assert "battery" in hits[0].chunk.text.lower()
    assert all(h.score > 0 for h in hits)
