# Weekly build · due Friday, before the showcase

*3 to 5 hours, Tuesday to Friday · due Friday [time], before the showcase, where all four of you present (about 5 minutes each)*

## Builder track: a streaming CLI assistant

A terminal chat app on an LLM API that remembers the conversation and can turn any reply into a structured summary.
Python, tests with pytest. Start from the starter repo (link in the channel) or from `demos/week1/stream_chat.py`,
but the code you hand in must be code you can explain.

### Acceptance criteria

- Streams replies token by token
- Keeps multi-turn history
- `/summary` returns JSON valid against a schema
- Handles a cut-off reply (`stop_reason` is `max_tokens`) and API errors cleanly
- Key from the environment; never in the repo
- Three tests, including one failure case

### Hints for the tests

Test your own functions without calling the real API: pass in a fake client, as `demos/offline.py` does. A good
failure test: the model's reply is cut off, and your app says so instead of printing half a JSON object.

## Operator track: your first role setup

1. Set up your Claude workspace for your role.
2. Write your role's `CLAUDE.md`: role, context, tools it may use, guardrails (drafts only), how to verify.
3. Build your first skill: one repeatable task, with a defined output format and two worked examples.
4. Run it on three real (or made-up) cases and write what it got right and wrong.

## Everyone

Your role map from Week 0, updated. Shortlist two capstone ideas for Week 2.

## How it is graded

Four things, from the rubric: **correctness** (does it do what the criteria say), **design** (clear structure, no
secrets in code), **testing** (Builder) or **evidence** (Operator: the three cases), and **explanation**. In the review
you explain how you handle a `max_tokens` stop, and what is in the history on turn three.

Grading is mostly pass or fail on engagement plus the rubric. "Solid" or above on correctness every week is what passes
the course.

## Before you submit

- [ ] No key, token or private data in the repo or the workspace
- [ ] You can explain every line, instruction and decision
- [ ] Tests (Builder) or the three cases (Operator) are included
