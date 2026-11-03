# Lab: a docs Q&A pipeline

*Tuesday after Session 1 through Wednesday, self-paced, about 2 hours (Tuesday's live session gives the brief); step 7 after Thursday's session · Builders do all steps; Operators do the Operator version below*

You will run the pipeline on the sample handbook, break it on purpose, fix it, and prove the fix with a number.
Work in the `demos/` folder. No API key is needed for steps 1 to 5 (use `DEMO_OFFLINE=1` for step 5).

## Builder steps

1. **Baseline.** Run `python3 week3/rag_eval.py`. Write down recall@1 and recall@2, and the two questions it misses.
2. **Add your own question.** In `week3/rag_eval.py`, add one question to `CASES` with the chunk that answers it
   (use the headings in `week3/docs/handbook.md`, for example "Leave"). Re-run. Did recall change?
3. **Add a document.** Put a new `.md` file in `week3/docs/` with two or three `## Heading` sections from your own
   role (made-up if sensitive). Add three questions for it to `CASES`. Re-run.
4. **Chunking.** Run `python3 week3/chunking.py`. Change a fixed size in the sweep, or add a fourth strategy of
   your own (for example chunks of two sentences). Which one wins on *your* document?
5. **Ask with citations.** `DEMO_OFFLINE=1 python3 week3/rag_eval.py --ask "<one of your questions>"`. Does the
   answer cite a chunk? Ask a question the docs cannot answer. Does it say it does not know?
6. **Optional, local embeddings.** `pip install sentence-transformers`, then `python3 week3/local_embeddings.py`.
   Compare recall with keywords on your questions. (No install? `EMBED_BACKEND=tfidf python3 week3/local_embeddings.py`
   runs the keyword fallback.)
7. **Thursday, after Session 2 (it shows this demo live): run the evals demo on your own set.** `DEMO_OFFLINE=1 python3 week3/evals.py` (offline answers are canned:
   it shows the mechanics, not model quality). Compare prompt v1 and v2, then read the failing cases by hand. For each
   one, decide: retrieval problem or generation problem?

Steps 4, 6 and 7 are demos you run yourself. Alvin runs chunking.py (with a short look at local_embeddings.py) and evals.py
live in Thursday's session, so do step 4 first and bring your numbers. Bring what you find to Discord or to Thursday's session.

## Operator version

1. Put 3 to 5 of your role's documents into your workspace as knowledge files (made-up or approved ones only).
2. Write 10 questions a colleague would ask. For each, note the document and section that answers it.
3. Ask your agent each question. For each answer, mark: correct? cites its source? Add 2 questions the documents
   cannot answer and check that it says so.
4. Count how many of the 10 it got right with a source. That is your starting score.

## Stop and check

- Can you say, for each wrong answer, whether the right passage was retrieved or not?
- Do you have a number you can compare against later?

Keep your notes: they are the start of your weekly build, which is due Friday, before the showcase (check the channel for the exact time); the one-page design is due Thursday.
