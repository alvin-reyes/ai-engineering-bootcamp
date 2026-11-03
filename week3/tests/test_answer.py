"""Acceptance: answers cite their sources, and say "I don't know" when the documents lack the answer."""
from docsqa.answer import Answer, answer_question, build_prompt, extract_citations
from conftest import FakeClient


def test_answer_cites_retrieved_chunk(retriever, fake_client):
    ans = answer_question("How many days do customers have to return an unused bike?", retriever, fake_client)
    assert isinstance(ans, Answer) and ans.answered
    assert "30 days" in ans.text
    assert "returns.md#returns" in ans.citations
    assert len(fake_client.calls) == 1


def test_prompt_wraps_chunks_with_ids_and_question(retriever):
    hits = retriever.search("express delivery", 2)
    prompt = build_prompt("How much is express?", hits)
    assert f'<chunk id="{hits[0].chunk.id}">' in prompt
    assert "</chunk>" in prompt
    assert prompt.rstrip().endswith("Question: How much is express?")


def test_call_uses_a_system_prompt_that_demands_citations(retriever, fake_client):
    answer_question("How much does express delivery cost?", retriever, fake_client)
    kw = fake_client.calls[0]
    assert kw["system"] and "cite" in kw["system"].lower() and "know" in kw["system"].lower()
    assert kw["max_tokens"] > 0 and kw["model"]


def test_no_retrieval_hits_means_idk_without_calling_the_model(retriever, fake_client):
    ans = answer_question("zzzz qqqq", retriever, fake_client)
    assert not ans.answered and ans.citations == []
    assert "don't know" in ans.text.lower()
    assert fake_client.calls == []


def test_model_says_idk(retriever, fake_client):
    ans = answer_question("Does Brightwater offer a trade-in programme for old bikes?", retriever, fake_client)
    assert not ans.answered and ans.citations == []
    assert "don't know" in ans.text.lower()


def test_uncited_answer_is_not_accepted(retriever):
    client = FakeClient(lambda prompt: "Customers have 30 days to return a bike.")
    ans = answer_question("How many days to return an unused bike?", retriever, client)
    assert not ans.answered
    assert "don't know" in ans.text.lower()


def test_invented_citation_is_ignored(retriever):
    client = FakeClient(lambda prompt: "30 days. [made-up.md#nothing]")
    ans = answer_question("How many days to return an unused bike?", retriever, client)
    assert not ans.answered


def test_extract_citations():
    text = "A [a.md#x]. B [b.md#y] and again [a.md#x]. C [ghost]."
    assert extract_citations(text, {"a.md#x", "b.md#y"}) == ["a.md#x", "b.md#y"]
