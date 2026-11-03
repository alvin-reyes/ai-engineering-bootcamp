# Week 2 starter: an agent with three tools

Your Week 2 build starts here. The code is a skeleton: signatures, docstrings and `# TODO:` markers. There is no
solution in this folder, and the tests fail until you write it. That is the plan.

Python 3.11 or newer. You need **no API key** to build and test: the tests use a scripted fake model.

## What to build (Builder track)

An agent that answers order questions with three tools you design: look up an order (`get_order`), search the help
docs (`search_help`) and draft a refund request for a human to approve (`draft_refund`). The data is fake and
local. The point is the loop, the schemas and the guardrails. Change the shop or the data if you like, but you
must be able to explain every line.

### Acceptance criteria (from `readings/week2/build.md`)

- [ ] Three tools with strict schemas (required fields, no extras)
- [ ] Inputs validated in your code before any tool runs
- [ ] A refund waits for a human "yes" (the write tool only drafts)
- [ ] A step limit, and every tool call logged (inputs, result, time)
- [ ] Bad tool input returns a useful error the model can act on
- [ ] Five scripted test conversations pass, including one where the human says no and one where a tool fails
- [ ] A short README of your own: how to run it, and one paragraph on why you chose these tools

`tests/test_agent.py` checks each of the first six, one section per criterion. The seventh is yours: write your own
README (replace this one when you hand in).

## Files

| File | What it is |
|---|---|
| `agent.py` | The build: tool definitions, handlers, validation, approval gate, logging, the loop. Fill in the TODOs |
| `tests/conftest.py` | The scripted fake model and helpers. Do not edit |
| `tests/test_agent.py` | The acceptance tests |
| `mcp_server.py` | **Stretch, optional.** Your tools over MCP. Do it only after the tests pass |
| `tests/test_mcp_stretch.py` | Stretch tests. Skipped if `mcp` is not installed |
| `lab/` | The lab: exact commands (`README.md`), your notes, and `my_tool.py` for Part 3 |

## Run and test

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                                  # all tests
pytest tests/test_agent.py -x -q        # stop at the first failure; fix it; repeat
```

Suggested order: tool definitions, then `get_order`, `validate_input`, `run_tool`, `run_agent`, then the rest.
Each failing test says which criterion it checks.

Against the real model (needs a key; never put it in a file you hand in):

```bash
export ANTHROPIC_API_KEY=...            # from your own shell, not from code
python3 agent.py "Where is ORD-1002? It arrived broken, can I get a refund?"
python3 agent.py --no "Refund ORD-1002, it arrived broken"     # watch the "human declined" path
```

The fake model proves your plumbing, not the model's judgement. Before you hand in, run it once with a key
and see whether your tool descriptions make the real model pick the right tool.

## Stretch: tools over MCP (optional)

```bash
pip install mcp
pytest tests/test_mcp_stretch.py
```

Fill in `mcp_server.py` (the pattern is `demos/week2/mcp_server.py`). Keep the refund tool draft-only, and say in
your README what the server can and cannot do.

## Builder or Operator?

This starter is the **Builder** track. **Operator** track: you do not write this code. Your build is connected
apps (read-only first, with your employer's OK) plus one subagent, a real run and a one-page write-up; see
`readings/week2/build.md`. You can still read `agent.py`'s docstrings: the ideas (strict inputs, a human yes
for anything that writes, a step limit, a log) are the same ones you write into your subagent's instructions.
You can switch tracks until the end of Week 2.

## Capstone canvas and pitch (everyone)

- Canvas: `modules/12-capstone-role-agent/role-agent-canvas.md`. Fill in as much as you can by Friday; a Role
  row is enough. You draft the Tools, Guardrails and Verify rows in Thursday's session.
- Pitch template (3 minutes: Role 30 s, Shape 30 s, Tools and guardrails 1 min, Verify 45 s, Risk and one question
  15 s): `readings/week2/build.md`, section "Everyone: the capstone pitch".

## Hand in

Friday [time] [VERIFY], before the showcase [where to submit]: a repo link or zip with `agent.py`, your tests, and
your own README. No keys in any file. Plus your canvas.
