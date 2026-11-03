# Lab · Instrument, attack, fix

*90 minutes, Tue after the session to Thu · everyone · pairs for part 2 (async on Discord)*

Apply this week to your own capstone, not a toy. Tuesday's Session 1 gives you the brief; you do the lab on your own time, and Thursday's Session 2 covers the last part.

## Part 1 · Trace and price it (30 minutes)

1. Wrap your capstone's model call so it logs one JSON line per call: latency, tokens in and out, cost estimate.
   Start from `demos/week4/tracing_cost.py`. Operator track: run your workspace on 5 real tasks and note time taken
   and tokens or usage shown by your workspace, as far as it reports them.
2. Run 10 realistic inputs. Write down **cost per request**, **median latency**, and the slowest case.
3. Is anything in your prompt before the stable part changing every call (a date, an id)? Move it to the end.
   If you can see cache numbers, show reads going up on repeat calls.

Done when: you can say "one request costs about X and takes about Y seconds" and point to the lines that show it.

## Part 2 · Red-team a partner (30 minutes)

Swap capstones with a partner (agree a time on Discord on Tuesday) and work async, Tue after the session to Wed. For about 15 minutes each, try to make the other app misbehave **only through its inputs**:
a document, a tool result, user text. Ideas: hidden "ignore previous instructions", a request for another user's
data, a request to send or delete something, a request to print the system prompt.

Write down, for each attempt: what you tried, what happened, whether it worked. Post the list in your pair's Discord thread (no keys, no private data).

## Part 3 · Fix what you found (20 minutes)

For each attempt that worked, add a guardrail from reading 3 (remove the tool, gate it, scope the data, add an output
check) and rerun the same attack. Keep the before and after: that is your "Safety: excellent" evidence.

## Part 4 · Decide on fine-tuning (10 minutes, after Thursday's session)

Read reading 5 before Thursday, decide it together in Session 2, then write the one line, with a number from your eval set.

## Hand in

A short note (5 lines is fine): cost per request, median latency, the injection you tried, the fix, the fine-tune
decision. Never include API keys or private data.
