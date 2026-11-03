# Lab: build the loop, then break it

*About 90 minutes before Thursday, plus about 30 minutes of extras and a second pass after Thursday's session (see below) · everyone (Operator track: the last part of each step is done in your workspace)*

Do the lab after Tuesday's session and before Thursday's (Tuesday afternoon and Wednesday, at your own pace; Discord for questions), and finish the second pass after Thursday's session. Work in pairs if you like; explain every line to your partner as you write
it. You can use Claude Code to write code, but you must be able to say what each part does and why.

## Part 1: run and read (15 min)

```bash
cd demos
python3 week2/support_agent.py "Where is ORD-1002? It arrived broken, can I get a refund?"
```

No key yet? Add `DEMO_OFFLINE=1` in front. Write down the order of tool calls and where it stopped for you.

## Part 2: break it on purpose (30 min)

Open `week2/support_agent.py`. For each change, predict what happens, then run it.

1. Set `MAX_STEPS = 2`. What does the agent say, and is that a good failure?
2. Change the `draft_refund` description to "Refund the customer." Does the model behave differently? (Offline
   cannot show this; it needs your key.)
3. In `run_tool`, return `"Error."` for every failure. Ask about `ORD-9999`.
4. Remove the `is_error` flag from the tool result. Does it still work? What did you lose?

## Part 3: design a tool (30 min)

Pick one task from your capstone canvas that needs a tool. Write:

- the tool name, a three-line description (when to use it, what it returns, what it is not for), and its
  input schema;
- one bad input and the error message your tool should return;
- whether it is read or write, and if it writes, the approval step.

Test the description: ask a partner (or Claude) "given only this description, when would you call this tool, and
what would you pass?" If the answer is wrong, the description is the bug.

## Part 4: place it (15 min)

Write one sentence: "My agent is a single call / workflow / agent because ___." Then run
`week2/agent_vs_workflow.py` and note one thing in the output that supports your choice.

## Optional: tools over MCP (20 min)

Install the SDK (`pip install mcp`), then run `python3 week2/mcp_client.py` from the demos folder. Open
`week2/mcp_server.py` and answer: which tool is read-only, which only drafts, and where does the tool description
come from? Then add the server to Claude Code with `claude mcp add support -- python3 /full/path/to/week2/mcp_server.py`,
ask Claude to check `ORD-1002`, and remove it afterwards (`claude mcp remove support`). Operator track: look at
the connectors you can add in your workspace and write down which would be read-only.

## Hand in

Post in the cohort channel: your tool definition from Part 3, and your one-sentence shape choice. Do not post
keys, passwords or real customer data.

## Also in the lab: extras and the second pass (about 30 min)

Before Thursday (with Parts 3 and 4):

- **Tool design reading** (about 10 min): skim `02-tool-design.md` and bring your Part 3 tool to Thursday's session; we run `tool_design.py` and fix tools in pairs there.
- **Workflow or agent demo** (about 15 min): run `python3 week2/agent_vs_workflow.py` and read the verdict before you write your shape sentence.
- **MCP server** (optional): `03-tools-over-mcp.md` and `python3 week2/mcp_server.py`.

After Thursday's session (second pass):

- **Terse errors** (about 10 min): run `python3 week2/tool_design.py --errors --terse` and fix your own tool's error messages.
- **Skip the gate** (about 10 min): run `python3 week2/verify_gate.py --skip-verify`. Add one line to your canvas: what is your command or checker?

Your build and canvas are due Friday [time] [VERIFY the time], before the showcase.
