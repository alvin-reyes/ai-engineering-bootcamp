# Week 3 lab: exact commands

The lab works in the course `demos/` folder, not in this repo. Nothing here needs an API key until the last
optional step. Full text: `readings/week3/lab.md`. All commands run from `demos/`.

```
cd demos
```

1. Baseline: `python3 week3/rag_eval.py`. Write down recall@1 and recall@2 and the two questions it misses.
2. Add a question: open `week3/rag_eval.py`, add a line to `CASES`, in the form `("your question", "Leave")`. The
   second item is the `## Heading` of the section that answers it. Re-run.
3. Add a document: create `week3/docs/<name>.md` with two or three `## Heading` sections from your role (made up
   if sensitive). Add three questions for it to `CASES`. Re-run.
4. Chunking: `python3 week3/chunking.py`. Change a size in the sweep, or add a fourth strategy. A function takes
   the whole text and returns a dict `{chunk_id: chunk_text}` (see `by_heading`). Start from `my_chunker.py`
   next to this file, paste your function into `chunking.py`, and add it to the strategies it compares.
5. Citations: `DEMO_OFFLINE=1 python3 week3/rag_eval.py --ask "your question"`, then one the docs cannot answer.
6. Optional, local embeddings: `pip install sentence-transformers`, then `python3 week3/local_embeddings.py`.
   No install: `EMBED_BACKEND=tfidf python3 week3/local_embeddings.py`.
7. After Thursday's session: `DEMO_OFFLINE=1 python3 week3/evals.py`. For each failing case decide: retrieval
   problem or generation problem? (Offline answers are canned: it shows mechanics, not model quality.)

Keep your numbers: they are the start of your weekly build (the repo in the folder above).
