# Weekly build: docs Q&A with an eval set

*Due Friday, before the showcase (check the channel for the exact time) · the one-page design is due Thursday · about 4 to 6 hours · both tracks*

Answer questions over **your role's own documents** with citations, and prove it with an eval set you wrote.
This is also the working slice for your capstone design review. On Friday you show the build to the group (about 3 minutes).

## Builder track

Build a docs Q&A program in Python. Acceptance criteria:

- [ ] Ingests, chunks, embeds (or keyword-indexes) and searches a doc set of at least 5 documents
- [ ] Answers cite their sources
- [ ] Says "I don't know" when the documents lack the answer
- [ ] An eval set of **30 cases, 5 of them unanswerable**
- [ ] Recall@5 and answer accuracy are reported
- [ ] **One change** is made, measured (before and after) and explained

Hand in a repo with the program, the eval set file, an eval script and a README with your numbers.

## Operator track

- [ ] Knowledge files added to your workspace (approved or made-up documents only)
- [ ] An eval sheet with **20 real past cases**, at least 3 the documents cannot answer
- [ ] For each case: expected answer, source, and your grade of the agent's answer (correct, cited)
- [ ] One change to your instructions or knowledge files, with the score before and after

Hand in your workspace folder, the eval sheet and a short write-up (half a page).

## Capstone design review (everyone)

Submit a **one-page written design** by Thursday (check the channel for the exact time), a day before the build. It is read before Friday. On Friday you get
about 5 minutes live: your three biggest decisions and the one you are least sure about, a working slice, then
feedback. The page covers:

- [ ] **Role and definition of done:** one job, what a finished run looks like, who checks it
- [ ] **Architecture:** the persona contract (Role, Context, Tools, Guardrails, Verify) on one page or diagram
- [ ] **Data:** what documents or systems it reads, and whether they are allowed to go to the model you chose
- [ ] **A working slice:** one real run, shown live or as a recording
- [ ] **First 20 eval cases:** real past cases with expected results
- [ ] **Biggest risk** and what you will do about it
- [ ] **Guardrails:** what it drafts for a human to send, what needs approval

You leave Friday with agreed next steps for Week 4: go ahead, go ahead with changes, or narrow the scope.

## How it is graded

- Weekly build: correctness at **solid** or above on the module rubric, plus engagement. Builder and Operator builds
  are graded on the criteria above.
- The last criterion matters most: show a before and after number for one change, and explain **why** it moved.
- Design review: spoken feedback on Friday, written feedback afterwards. It is checked against the capstone rubric, not ranked against anyone.
- You must be able to explain every line and every instruction you hand in.
