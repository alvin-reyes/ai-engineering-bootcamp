# Week 3 starter: docs Q&A with an eval set

Your weekly build (Builder track). You answer questions over a set of documents, with citations, and prove how
good it is with an eval set. Full brief: `readings/week3/build.md`. Do the lab first (`lab/README.md`).

The skeleton has function signatures, docstrings and `# TODO:` markers. Fill them in, one file at a time, in this
order. Run the tests after each step. They need no API key and no network.

| Step | File | What you write |
|---|---|---|
| 1 | `docsqa/ingest.py` | load documents, cut them into chunks |
| 2 | `docsqa/retrieve.py` | TF-IDF search in pure Python (plus the optional embedding hook) |
| 3 | `docsqa/answer.py` | prompt, call the model, citations, "I don't know" |
| 4 | `docsqa/evalrun.py` | read the eval set, recall@k, answer accuracy |

## Run it

```
pip install -r requirements.txt
pytest                      # all red at the start: that is the plan
pytest tests/test_ingest.py # one step at a time
python -m docsqa ask "How many days do customers have to return an unused bike?"   # needs ANTHROPIC_API_KEY
python -m docsqa eval --retrieval-only                                               # recall@5, no key needed
python -m docsqa eval                                                                # recall and answer accuracy, needs a key
```

The sample documents (made-up, safe) are in `docs/`. The eval-set template is `evalset/eval_set.jsonl`: one JSON
object per line.

```
{"id": "q01", "question": "...", "answerable": true, "source": "returns.md", "must_contain": "30 days"}
{"id": "q09", "question": "...", "answerable": false, "source": null, "must_contain": null}
```

`source` is the document that holds the answer. `must_contain` is a phrase a correct answer must include. For an
unanswerable case the right reply is "I don't know".

## Acceptance criteria (from the build brief)

The tests check the first four on a fixed set of test documents in `tests/fixtures/`, so your own changes to
`docs/` never break them.

- [ ] Ingests, chunks and keyword-indexes (or embeds) a doc set of at least 5 documents
- [ ] Answers cite their sources
- [ ] Says "I don't know" when the documents lack the answer
- [ ] Recall@5 and answer accuracy are reported (`python -m docsqa eval`)
- [ ] Your eval set has **30 cases, 5 of them unanswerable**, over your own role's documents
- [ ] **One change** is made, measured (before and after) and explained in your README

Check the last two yourself with `CHECK_FINAL=1 pytest tests/test_final_checklist.py`. It reads your `docs/` and
your `evalset/eval_set.jsonl`.

## Optional: local embeddings

`Retriever(chunks, embed_fn=...)` takes any function that turns a list of texts into a list of vectors.
`sentence_transformers_embed_fn()` in `retrieve.py` is one (`pip install sentence-transformers`; it downloads a
small model once, then runs with no network). Compare its recall with TF-IDF on your own questions. Nothing is sent
to an API. Hand-in tip: the tests use a tiny fake `embed_fn`, so you never need the install to pass them.

## Builder vs Operator

This repo is the **Builder** build. If you are on the **Operator** track you do not write this code: add knowledge
files to your Claude workspace, write an eval sheet of 20 real past cases (3 or more the documents cannot answer),
and make one change to your instructions or knowledge files with the score before and after. The same thinking
applies: expected answer, source, and a grade per case. You can still copy `evalset/eval_set.jsonl` as a model for
your sheet.

## Capstone design review

Everyone, both tracks, hands in a one-page written design by Thursday. Use `design_review_template.md`. It is
read before the Friday showcase, where you get about 5 minutes live.

## What to hand in

A repo with the program, your eval-set file, the eval script and a README with your numbers: recall@5, answer
accuracy, and the before and after of your one change with a sentence on why it moved. No keys or tokens in the
repo (`.env` is ignored). You must be able to explain every line.

Tips: change one thing at a time and re-run the eval after each change. When an answer is wrong, first ask:
was the right chunk retrieved? If not, it is a retrieval problem (chunking, search). If yes, it is a generation
problem (prompt, context).
