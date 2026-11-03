"""Acceptance: ingests and chunks a doc set of at least 5 documents."""
from docsqa.ingest import Document, chunk_document, ingest, load_documents


def test_loads_five_documents_sorted(docs_dir):
    docs = load_documents(docs_dir)
    assert len(docs) >= 5
    assert [d.name for d in docs] == sorted(d.name for d in docs)
    assert all(isinstance(d, Document) and d.text.strip() for d in docs)


def test_ignores_other_file_types(tmp_path):
    (tmp_path / "a.md").write_text("## A\nhello")
    (tmp_path / "b.txt").write_text("## B\nworld")
    (tmp_path / "c.png").write_bytes(b"\x89PNG")
    assert [d.name for d in load_documents(tmp_path)] == ["a.md", "b.txt"]


def test_one_chunk_per_heading_and_heading_kept_in_text():
    doc = Document("t.md", "# Title\n\n## Alpha\nfirst fact.\n\n## Beta Two\nsecond fact.\n")
    chunks = chunk_document(doc)
    assert [c.id for c in chunks] == ["t.md#alpha", "t.md#beta-two"]
    assert [c.heading for c in chunks] == ["Alpha", "Beta Two"]
    assert chunks[0].source == "t.md"
    assert chunks[0].text.startswith("Alpha")
    assert "first fact." in chunks[0].text
    assert "second fact." not in chunks[0].text
    assert "Title" not in chunks[0].text  # the text before the first ## is not a chunk


def test_long_section_is_split_on_paragraphs_with_unique_ids():
    paras = [f"Paragraph {i} " + "word " * 30 for i in range(4)]
    doc = Document("long.md", "## Big\n" + "\n\n".join(paras))
    chunks = chunk_document(doc, max_chars=400)
    assert len(chunks) > 1
    assert len({c.id for c in chunks}) == len(chunks)
    assert chunks[0].id == "long.md#big"
    assert all(c.text.startswith("Big") for c in chunks)  # every part keeps its heading
    assert all(len(c.text) <= 400 + len("Big\n") for c in chunks)
    assert "Paragraph 3" in "".join(c.text for c in chunks)  # nothing is lost


def test_ingest_whole_folder(docs_dir):
    chunks = ingest(docs_dir)
    assert len(chunks) >= 10
    assert len({c.id for c in chunks}) == len(chunks)
    assert {c.source for c in chunks} >= {"returns.md", "shipping.md", "warranty.md", "repairs.md", "staff-handbook.md"}
