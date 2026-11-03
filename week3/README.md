# Week 3 activities

*Your week at a glance · about 10 to 12 hours · two 60-minute live sessions and a Friday showcase day · both tracks*

This week you make your agent answer from your own documents, with sources, and you build the tests that prove it.
Two live sessions of 60 minutes (Tuesday and Thursday), then a Friday showcase day; in between it is self-paced. Exact times are set by Alvin: where you see **[time]**, check the channel.

## Day by day

| Day | Activity | Time | Track | Output / what you hand in |
|---|---|---|---|---|
| Before Day 1 | Read lessons 1 to 3 and run the demos once (Builders). Gather 5 to 20 documents from your role (made-up or redacted if sensitive) and write down 20 real questions | about 1.5 hours | Both (demos: Builder) | Your document folder and your 20 questions |
| Day 1 (Tue) | **Live session 1 (60 min):** the RAG pipeline, retrieval decisions, a live recall demo, private and local AI, then the lab and build brief. **Then start the lab (self-paced):** `lab.md`. Builders: steps 1 to 6, including `chunking.py` (step 4) and, optionally, `local_embeddings.py` (step 6). Operators: 10 questions, 2 unanswerable | 60 min, [time], then about 2 to 2.5 hours | Both; lab: Builder / Operator versions | Lab notes, with a baseline number to compare against later |
| Day 2 (Wed) | **Build work session (self-paced):** finish the lab, read lesson 4 (evals). Builders: docs Q&A program and eval set. Operators: knowledge files and eval sheet. Start your one-page capstone design | about 3 to 4 hours | Builder / Operator versions | A build in progress; your design started; a working slice you can show |
| Day 3 (Thu) | **Live session 2 (60 min):** evals essentials, `evals.py` and `chunking.py` run live, measure retrieval and answers separately, a build and design clinic. **Then:** run `evals.py` on your own set (step 7 of the lab), read the failing cases, finish your design. **One-page design due [VERIFY time].** | 60 min, [time], then about 1.5 to 2 hours | Both | Your design submitted (see the checklist); your eval cases |
| Day 4 (Fri) | **Weekly build due [time], before the showcase [VERIFY].** Showcase day (up to 60 min [VERIFY]): build showcase (about 3 minutes each), capstone design reviews (5 minutes each, live) | [time] | Both | Build submitted and shown; design reviewed; agreed next steps for Week 4 |
| Any time | **Discord Q&A:** ask when you are stuck. The self-check quiz (10 minutes) fits any time after lesson 4 | as needed | Both | Nothing to hand in |

Hours: reading and prep 1.5, session 1 1, lab 2 to 2.5, build work 3 to 4, Thursday session 1 and finish plus design 1.5 to
2, quiz 0.2, Friday showcase about 0.7 to 1. That is about 10 to 12 hours in total, as before: the time saved in the
live sessions moved into the lab and the written design.

## Your checklist

**Before Day 1 (Tue)**
- [ ] Read lessons 1 to 3 (about 30 minutes)
- [ ] Builders: run the four demos once (see the overview)
- [ ] A folder of 5 to 20 documents from your role (made-up or redacted if sensitive)
- [ ] 20 real questions a person in your role would ask those documents
- [ ] Your capstone canvas and pitch from Week 2

**Day 1 (Tue) to Day 2 (Wed)**
- [ ] Lab done (`lab.md` steps 1 to 6): Builders have recall numbers and a chunking comparison; Operators have a starting score
- [ ] Lesson 4 read (evals)

**Day 3 (Thu), after the session**
- [ ] `evals.py` run on your own set (offline is fine) and its failing cases read: retrieval or generation?

**Day 3 (Thu), by [VERIFY time]: one-page capstone design (reviewed live on Friday)**
- [ ] Role and definition of done: one job, what a finished run looks like, who checks it
- [ ] Architecture: the persona contract (Role, Context, Tools, Guardrails, Verify) on one page
- [ ] Data: what it reads, and whether that data may go to the model you chose
- [ ] A working slice: one real run, live or recorded
- [ ] First 20 eval cases: real past cases with expected results
- [ ] Biggest risk and what you will do about it
- [ ] Guardrails: what it drafts for a human to send, what needs approval

**Day 4 (Fri), by [time], before the showcase [VERIFY]: weekly build due**
- [ ] Builders: a repo with the docs Q&A program (5 or more documents, answers cite sources, says "I don't know"), an eval set of 30 cases (5 unanswerable), an eval script, and a README with recall@5 and answer accuracy
- [ ] Builders: one change, measured before and after, and explained
- [ ] Operators: knowledge files in your workspace, an eval sheet of 20 real past cases (at least 3 the documents cannot answer) with expected answer, source and your grade for each
- [ ] Operators: one change to your instructions or knowledge files, with the score before and after, in a half-page write-up
- [ ] No keys, passwords or tokens in anything you hand in
- [ ] You can explain every line and every instruction you hand in
- [ ] Self-check quiz done (10 minutes, any time after lesson 4)

**Day 4 (Fri): showcase day**
- [ ] Be ready to run your build live for about 3 minutes: one real question, one the documents cannot answer, your before and after number
- [ ] Be ready for 5 minutes on your design: your three biggest decisions and the one you are least sure about, a working slice, feedback

**Where and how to submit:** [where to submit]. Builders hand in a repo link or a zip; Operators hand in the workspace folder, the eval sheet and the write-up.

## The capstone milestone

This week is the **capstone design review**. Your weekly build is also the working slice for it. By Thursday [VERIFY time] you
submit a one-page written design, and have one real run and your **first 20 eval cases**. On Friday you get 5 live
minutes. You are checked against the capstone rubric, not ranked against anyone, and you leave with agreed next steps for Week 4.

## Optional stretch

- Local embeddings (lab step 6): `pip install sentence-transformers`, then `python3 week3/local_embeddings.py`. Compare its recall with keyword search on your own questions (Builders).
- Add a fourth chunking strategy of your own and compare it on your documents.
- Operators: add a second set of knowledge files and see whether your score moves.

## If you're stuck

- Post in Discord: what you tried, what you expected, what happened. Written questions help everyone.
- For a wrong answer, first print what was retrieved. Right passage missing: fix retrieval. Right passage present: fix the prompt.
- Change one thing at a time, so you know what moved the number.
- Behind by Day 2 (Wednesday)? Say so early. A smaller build with a real before and after number beats a big one with none.

*Dates this week: Tuesday 24 November to Friday 27 November. VERIFY: holidays for the cohort's location (Thursday 26 November is US Thanksgiving; the cohort is likely in the Philippines, where it is not a holiday). A public holiday can move a live session or a deadline.*
