# Week 2 lab: exact commands

Source: `readings/week2/lab.md` (the instructions). This page only gives the commands. Do not post keys, passwords
or real customer data. The course demos live in the course repo's `demos/` folder; commands below start there.

```bash
cd demos
```

## Part 1: run and read (15 min)

```bash
python3 week2/support_agent.py "Where is ORD-1002? It arrived broken, can I get a refund?"
DEMO_OFFLINE=1 python3 week2/support_agent.py "Where is ORD-1002? It arrived broken, can I get a refund?"   # no key
```

Write down the order of tool calls and where it stopped for you.

## Part 2: break it on purpose (30 min)

Never edit the demo itself. Work on a copy (it still finds `offline.py` one folder up):

```bash
cp week2/support_agent.py week2/support_agent_lab.py
```

For each change below, write your prediction first, then run, then write what happened in `lab/notes.md`
(copy the table from this folder). Run each with:

```bash
DEMO_OFFLINE=1 python3 week2/support_agent_lab.py --yes "Where is ORD-9999?"
```

1. Set `MAX_STEPS = 2`. What does the agent say, and is that a good failure?
2. Change the `draft_refund` description to "Refund the customer." (needs your key to see a difference).
3. In `run_tool`, return `"Error."` for every failure. Ask about `ORD-9999`.
4. Remove the `is_error` flag from the tool result. Does it still work? What did you lose?

Remove the copy when done: `rm week2/support_agent_lab.py`.

## Part 3: design a tool (30 min)

Edit `lab/my_tool.py` in this starter folder (TOOL, WRITES, APPROVAL, EXAMPLE_GOOD, EXAMPLE_BAD, validate), then:

```bash
pytest tests/test_lab_tool.py
```

Post your TOOL dict and one bad input with its error message in the cohort channel.

## Part 4: place it (15 min)

```bash
python3 week2/agent_vs_workflow.py    # from demos/ ; add DEMO_OFFLINE=1 with no key
```

Write one sentence in `lab/notes.md`: "My agent is a single call / workflow / agent because ___."

## Second pass, after Thursday (about 30 min)

```bash
python3 week2/tool_design.py --errors --terse
python3 week2/verify_gate.py --skip-verify
```

Add one line to your canvas: what is your command or checker?

## Optional: tools over MCP (20 min)

```bash
pip install mcp
python3 week2/mcp_client.py
claude mcp add support -- python3 /full/path/to/demos/week2/mcp_server.py
claude mcp remove support      # when you are done
```
