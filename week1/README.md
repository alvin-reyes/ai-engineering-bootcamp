# Week 1 activities

*Your week at a glance · about 10 to 12 hours: 2 live, the rest on your own · both tracks*

Week 1 is LLM Foundations (Tue 2026-11-10 to Fri 2026-11-13): what the model sees, how to prompt it, how to call it
reliably, and how to get structured output. There are two live sessions of 60 minutes, on Tuesday and Thursday. Friday is a
separate showcase day: you show the weekly build. In between you work on your own: readings, lab and build, with Discord Q&A.
The build is due Friday before the showcase. Times marked [time] are confirmed in the channel. Builder-only items are marked;
Operators skip them.

## Day by day

| Day | Activity | Time | Track | Output / what you hand in |
|---|---|---|---|---|
| Before Tue | Check before you arrive: Week 0 readings done, role map handed in, your environment works, one piece of your own work text (private details removed) | 15 min | Both | Role map handed in |
| Day 1 (Tue 11-10) | Live session 1: How LLMs work (tokens, context, cost), one live demo of a streaming call, the lab and build briefs | 60 min, [time] | Both | A streaming call seen; one thing the model does not remember |
| Day 1 (Tue) | After the session: readings 1 (tokens, context, cost) and 5 (calling the API) | 20 min + 25 min | 1: Both; 5: Builder | Self-checks tried |
| Day 1 (Tue) | Lab steps 1 to 3 (setup, run the chat, break it on purpose). Operator: step 1 (workspace and `CLAUDE.md`) | about 40 min (Operator 20 min) | Both | Notes: what broke and why |
| Day 2 (Wed 11-11) | Lab steps 4 and 5 (change something, the five-pass comparison). Operator: step 2 (five-pass prompt ladder) | about 30 min (Operator 25 min) | Both | Your change; which pass helped most |
| Day 2 (Wed) | Readings 2, 3, 4 (prompting: clear and structured; examples, thinking, chaining; untrusted input and evals). Not taught live in full | 30 + 30 + 30 min | Both | Self-checks tried |
| Day 2 (Wed) | Readings 6 (structured output) and 7 (errors, retries, stop reasons) | 20 min + 15 min | 6: Both; 7: Builder | Self-checks tried; one question posted in the channel |
| Day 3 (Thu 11-12) | Live session 2: debrief of the lab (the API call, the five common mistakes), then prompt engineering essentials (the brief, structure, the prompt lab demo), quiz questions, next week | 60 min, [time] | Both | Questions about your lab; prompts you would change |
| Day 3 (Thu) | After the session: lab step 6, prompt iteration against an eval set. Operator: steps 3 and 4 (eval by hand on 8 cases, notes) | about 30 min (Operator 25 min) | Both | Scores per prompt version; 3 lines on your change |
| Day 3 (Thu) | The weekly quiz (10 questions), for your own check | 10 min | Both | Quiz answers, for your own check |
| Day 1 to 4 (Tue to Fri) | Weekly build, Builder: a streaming CLI assistant with tests. Start on Tuesday or Wednesday | 3 to 5 h | Builder | Repo with the code, three tests (one failure case) |
| Day 1 to 4 (Tue to Fri) | Weekly build, Operator: your first role setup | 3 to 5 h | Operator | Workspace folder with your role `CLAUDE.md`, one skill, and a write-up of three cases |
| Day 4 (Fri 11-13) | **Weekly build due, [time], before the showcase** (hand in the lab notes with it) | | Both | Your build and lab notes handed in |
| Day 4 (Fri 11-13) | Showcase: all four of you show the build (about 5 minutes each), then feedback together. Up to 60 min, [time] | up to 60 min | Both | Your build shown and explained; feedback |
| Day 4 (Fri 11-13) | Update your role map and shortlist two capstone ideas for Week 2 | 20 min | Both | Updated role map; two ideas |

Hours: live sessions 2 h; Friday showcase up to 1 h; readings about 2 h 50 (Operators about 2 h 10); lab about 1 h 40 (Operators about 1 h 10); build 3 to 5 h;
quiz 10 min; role map and capstone ideas 20 min. Most of the week is on your own: start the build by Wednesday, not Thursday night or Friday morning.

## Checklist

- [ ] Environment works (Builder: Python 3.11+, `pip install -r requirements.txt`, `ANTHROPIC_API_KEY` in your shell. Operator: workspace open) (before session 1, Tue 11-10)
- [ ] Role map handed in (before session 1, Tue 11-10)
- [ ] Live session 1 attended (Tue 11-10)
- [ ] Reading 1: tokens, context and cost (Tue 11-10)
- [ ] Reading 5: calling the API, Builder (Tue 11-10)
- [ ] Lab steps 1 to 3 (Tue 11-10); steps 4 and 5 (Wed 11-11)
- [ ] Readings 2, 3, 4 (Wed 11-11)
- [ ] Reading 6: structured output (Wed 11-11)
- [ ] Reading 7: errors, retries, stop reasons, Builder (Wed 11-11)
- [ ] One question posted in the channel (Wed 11-11)
- [ ] Live session 2 attended (Thu 11-12)
- [ ] Lab step 6 done, with your lab notes complete (Thu 11-12)
- [ ] Weekly quiz done (Thu 11-12, before the showcase)
- [ ] Weekly build finished and checked against "Before you submit", handed in with your lab notes (Fri 11-13, [time], before the showcase)
- [ ] Showcase: your build shown (Fri 11-13, [time])
- [ ] Role map updated, and two capstone ideas shortlisted for Week 2 (Fri 11-13)

## What you hand in

| Deliverable | Due | How |
|---|---|---|
| Role map (from Week 0) | Tue 11-10, before session 1 | [where to submit] |
| Lab notes | Fri 11-13, [time], with the build, before the showcase | [where to submit] |
| Weekly build, Builder: repo with code and three tests | Fri 11-13, [time], before the showcase | Start from the starter repo (link in the channel); [where to submit] |
| Weekly build, Operator: workspace folder, role `CLAUDE.md`, one skill, write-up of three cases | Fri 11-13, [time], before the showcase | [where to submit] |
| Updated role map and two capstone ideas | Fri 11-13 | [where to submit] |

Before you submit: no key, token or private data in the repo or workspace; you can explain every line, instruction
and decision; tests (Builder) or the three cases (Operator) are included. In the review (at the Friday showcase) you will be asked how you
handle a `max_tokens` stop, and what is in the history on turn three.

## Capstone milestone

Your role map is updated, and you have shortlisted two capstone ideas for Week 2, when the canvas and pitch are
due. The Operator build (role `CLAUDE.md` and first skill) and the Builder build are the first pieces your capstone
grows from.

## Optional stretch

- Add a field to the summary schema, or print the cost of each turn (Builder).
- Add two tickets of your own to the eval set, one tricky and one that tries to give an instruction.
- Try the prompt ladder on a second task from your role map.
- Write down one thing you will always put in the instructions from now on.

## If you're stuck

Post in the channel (Discord) with what you tried and what you saw, at any time. Ask early, especially if your
environment does not work: before Tuesday, not on Thursday night or Friday morning. No API key yet? Every demo also runs offline with
`DEMO_OFFLINE=1`. Keep your key and any private text out of what you post.
