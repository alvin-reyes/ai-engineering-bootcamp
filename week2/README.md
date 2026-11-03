# Week 2 activities

*Your week at a glance · about 10 hours · both tracks*

Two live sessions of 60 minutes (**Tuesday and Thursday**), a self-paced lab and build around them, and a separate
**Friday showcase** day where you show your build and pitch your capstone. Your build and canvas are due on
**Friday [time]** [VERIFY the time], before the showcase starts. Exact times are in Discord: where you see [time],
that is where it goes.

## Day by day

| Day | Activity | Time | Track | Output / what you hand in |
|---|---|---|---|---|
| Before Day 1 | Read `00-overview.md`, skim readings 1 and 2, run the first demo (offline is fine) | about 1 h | Both | Nothing to hand in. Note one question for the session |
| Day 1 (Tue) | **Live session 1:** tool use and the agent loop, live demo, tools over MCP (5-min demo), workflow or agent, lab and build brief | 60 min, [time] | Both | One sentence: "My idea is a single call / workflow / agent because..." |
| Day 1-2 (Tue after the session, Wed) | **Lab:** run it, break it, design a tool from your canvas, place it (`lab.md`) | about 90 min | Both. Operator: the last part of each step is done in your workspace | Your tool definition and your one-sentence shape choice, posted in the cohort channel by Wednesday evening |
| Day 1-2 (Tue, Wed) | **Lab, extras:** skim the tool-design reading (`02-tool-design.md`) before Thursday; the workflow-or-agent demo (`agent_vs_workflow.py`); MCP server (optional) | about 30 min | Both. Operator: read the ideas, run what you can | Notes on one thing that surprised you |
| Day 2 (Wed) | Fill in your capstone canvas as far as you can | about 1 h | Both | Your canvas, submitted with the build on Friday |
| Day 3 (Thu) | **Live session 2:** tool design (demo and pairs), guardrails, Verify (live demo), and a canvas workshop where you draft your Tools, Guardrails and Verify rows | 60 min, [time] | Both | Three canvas rows drafted |
| Day 3-4 (Thu after the session, Fri morning) | **Lab, second pass:** `tool_design.py --errors --terse`, `verify_gate.py --skip-verify`, fix your own tools, write your Verify command | about 30 min | Both | One line in your canvas: what is your command or checker? |
| Day 1-4 (Tue-Fri morning) | Weekly build, in the gaps | about 3 h in all | Builder: an agent with three tools. Operator: connected apps plus one subagent | See the Friday row |
| Day 4 (Fri) | **Build and canvas due [time]** [VERIFY the time], before the showcase | [where to submit] | Both | Build, README or write-up, and canvas (details below) |
| Day 4 (Fri) | **Showcase:** build showcase (3 min each), then **capstone pitches** (3 min pitch plus a minute of feedback each) | up to 60 min [VERIFY], [time] | Both | Your showcase and your pitch, given live, and one question for each classmate |
| Any time | Self-check quiz (`quiz.md`, eight questions, no grade); Discord Q&A | about 15 min | Both | Nothing |

Total: about 10.5 hours (1 + 1 + 1.5 + 0.5 + 1 + 1 + 0.5 + 3 + 0.75 + 0.25). The Friday showcase is about 45 minutes
for four learners and never more than an hour [VERIFY the length].

## What is where

- **Tool design** (the six rules, fixing a bad tool with a partner, `tool_design.py`): live in Thursday's session. Before it, skim `02-tool-design.md` and bring the tool from lab Part 3. After it, run `--errors --terse` in the lab.
- **Workflow-or-agent demo** (`agent_vs_workflow.py`): in the lab, with Part 4. Reading `04-workflow-or-agent.md`. The explanation and your shape sentence are in Tuesday's session.
- **Verify demo** (`verify_gate.py`): live in Thursday's session; `--skip-verify` is in the lab. Reading `06-verify-gates.md`.
- **MCP**: Tuesday has a 5-minute demo (`mcp_client.py`); the server set-up (`claude mcp add`) is in `03-tools-over-mcp.md` and the optional lab stretch.
- **Quiz**: self-check in your own time.

## Checklist

- [ ] **Before Day 1:** read `00-overview.md`, skim readings 1 and 2, run the first demo (add `DEMO_OFFLINE=1` if you have no key)
- [ ] **Day 1 (Tue):** attend session 1; say your one-sentence shape choice
- [ ] **Day 1-2 (Tue-Wed):** do the lab (`lab.md`, parts 1 to 4) and skim `02-tool-design.md`
- [ ] **By Day 2 (Wed):** post your tool definition (Part 3) and shape sentence (Part 4) in the cohort channel. No keys, passwords or real customer data
- [ ] **Day 3 (Thu), [time]:** attend session 2. Bring your Part 3 tool and your canvas; you draft three rows in the session
- [ ] **By Day 4 (Fri [time]) [VERIFY the time]:** weekly build handed in, before the showcase:
  - Builder: a repo link (no keys in it) or a zip: three tools, strict schemas, validated inputs, a refund that waits for a human "yes", a step limit and a log, useful errors, five scripted test conversations (one where the human says no, one where a tool fails), and a short README. [where to submit]
  - Operator: your workspace folder and a one-page write-up (tools and apps used, read or write, where a human approves, what it refuses to do). Apps connected read-only, one subagent with one job, one real run with its output. No passwords or tokens in any file. [where to submit]
- [ ] **By Day 4 (Fri [time]) [VERIFY the time]:** capstone canvas submitted with the build (as far as you can: a Role row is enough). [where to submit]
- [ ] **Day 4 (Fri), [date], [time]:** attend the showcase. Show your build for 3 minutes (be ready to explain every tool, guard and line), pitch your canvas (3 minutes), answer a question, and ask each classmate one
- [ ] **After the showcase:** revise your canvas with the pitch feedback (one page) before Week 3 [VERIFY the date and where to post]

## Capstone milestone

This week your capstone starts. By Friday you have a role-agent canvas (you draft three rows of it in Thursday's session), and at the Friday showcase you give a pitch of three minutes (Role 30 seconds, Shape 30 seconds, Tools and guardrails 1 minute, Verify 45 seconds, Risk and one question 15 seconds):

1. Role: who you are, the one job, and what "done" means in a way you could check in two minutes
2. Why this job: your top three candidates and why this one scored highest
3. Shape: single call, workflow or agent, and why
4. Context and tools: what it reads; tool or app, read or write, approval needed
5. Guardrails: what it drafts but never sends, its limits, what it refuses
6. Verify: what checks its output, where your 20+ real past cases will come from, your honest minutes per run today times runs per week
7. Risks: one thing that could go wrong, and one question for the room

The pitch is not graded alone. It starts your capstone, which is graded at demo day. You can switch tracks until the end of this week.

## Optional stretch

- **Builder:** expose your three tools as an MCP server (`week2/mcp_server.py` is the pattern), call it with a small client, keep the refund tool draft-only, and say in your README what the server can and cannot do.
- **Operator:** connect one approved MCP server or connector, read-only, and write two lines on what it can see and why that is the least it needs. Check with your employer first (onboarding guide, section 7).
- **Both (lab, optional, about 20 min):** run `python3 week2/mcp_client.py` and read `week2/mcp_server.py`.

## If you're stuck

- Post in Discord what you tried and what you saw (error text, not keys). Written questions help everyone, and any time is fine.
- No API key? Every demo runs offline with `DEMO_OFFLINE=1`; it shows the mechanics, not real model behaviour.
- Stuck on the build? Start from `week2/support_agent.py`, then change the tools and tests until they are yours.
- Canvas feels too big? Pitch from the Role row only: one job you could check in two minutes.
- Short on time? Do the lab and the pitch first; the stretch can wait.
- Remember: AI can help you write code, but you must be able to explain every line.
