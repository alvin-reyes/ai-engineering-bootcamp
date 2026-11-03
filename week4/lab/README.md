# Lab starter: instrument, attack, fix

Four parts, matching `readings/week4/lab.md`. This folder holds the files for parts 2 and 3. Parts 1 and 4 use
`ops/` (see the top-level README).

## Part 1 · Trace and price it (Tue)

```bash
# after you finish ops/tracing.py and ops/summary.py:
python -m ops.summary traces.jsonl --per-day 1000
```

Write down: cost per request, median latency, slowest case. Prices are example constants: VERIFY them.

## Part 2 · Red-team a partner (Tue to Wed, async on Discord)

1. Agree a swap time with your partner on Tuesday.
2. Open `redteam_worksheet.md` and fill one block per attempt. Attack **only through the inputs**.
3. Add each attack you try to `attacks.json` (the file starts with 4 ideas; the tests need at least 8 in total,
   using all three channels: `document`, `tool_result`, `user_text`).
4. Post your worksheet in your pair's Discord thread.

## Part 3 · Fix what worked and rerun (Wed)

Write a small function that feeds one input to your agent with **fake tool handlers** (nothing real is sent) and
returns what happened:

```python
# my_agent.py
def handle(payload, channel):
    # TODO: run your agent on `payload` (as a document / tool result / user text) with fake tools
    return {"tool_calls": [{"name": "send_email", "args": {}, "executed": False, "approved": False}],
            "output": "the agent's answer text"}
```

Run all attacks, fix what worked, run again:

```bash
python -m lab.run_attacks my_agent:handle --secret CANARY-7f3a91
```

The command exits with 1 while any attack still works. Keep the before and after output for your demo.

Operator track: use the worksheet only. Run each attack by hand in your workspace and write the result down. Your fix
is an instruction or an approval step.

## Part 4 · Fine-tune decision (Thu, after Session 2)

One line, with a number from your eval set. Example shape: "No fine-tune: prompt and examples already reach 92% on
my 24 cases; the 2 misses are retrieval problems." Put it in your lab note.

## Hand in

The 5-line note: cost per request, median latency, the injection you tried, the fix, the fine-tune decision.
