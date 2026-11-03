# Weekly build: an agent with three tools, and your capstone pitch

*Due Friday [time] [VERIFY the time], before the showcase · everyone · Builder and Operator tracks*

Two things this week: the **weekly build** (your track) and the **capstone canvas and pitch** (everyone). Build and canvas are handed in on Friday, before the showcase starts; at the Friday showcase (up to 60 minutes [VERIFY]) you show the build for 3 minutes and give the pitch. Session 2 on Thursday helps with both.

## Builder track: a support agent with three tools

Build an agent that answers order questions using three tools you design: look up an order, search the help
docs, and draft a refund request for human approval. The data can be fake and local. The point is the loop, the
schemas and the guardrails, not the integrations. You may start from `week2/support_agent.py`, but your tools,
descriptions and tests must be your own and you must be able to explain every line.

### Acceptance criteria

- [ ] Three tools with strict schemas (required fields, no extras)
- [ ] Inputs validated in your code before any tool runs
- [ ] A refund waits for a human "yes" (the write tool only drafts)
- [ ] A step limit, and every tool call logged (inputs, result, time)
- [ ] Bad tool input returns a useful error the model can act on
- [ ] Five scripted test conversations pass, including one where the human says no and one where the tool fails
- [ ] A short README: how to run it, and one paragraph on why you chose these tools

**Stretch (optional):** expose your three tools as an MCP server (`week2/mcp_server.py` is the pattern), call it
with a small client, and keep the refund tool draft-only. Say in your README what the server can and cannot do.

Hand in a repo link (no keys in it) or a zip.

## Operator track: connect your apps and add a subagent

In your Claude workspace:

1. Connect the apps your job uses, **read-only first**, only after your employer allows it (see the onboarding
   guide, section 7).
2. Add **one subagent** with one job (for example a checker that reviews your drafts against your definition of
   done) and write its instructions.
3. Run your role's job once end to end and keep the result.

### Acceptance criteria

- [ ] Only read access to apps; any write is a draft you send
- [ ] The subagent has one job and its instructions say what to do when inputs are missing
- [ ] One real run with its output, and a note on what you changed after seeing it
- [ ] A one-page write-up: tools and apps used, read or write, where a human approves, what it refuses to do

**Stretch (optional):** connect **one approved MCP server or connector, read-only**, and write two lines on what it
can see and why that is the least it needs. (Check with your employer first; see the onboarding guide, section 7.)

Hand in your workspace folder and the write-up (no passwords or tokens in any file).

## Everyone: the capstone pitch

Fill in your role-agent canvas (`modules/12-capstone-role-agent/role-agent-canvas.md`) and submit it with your build on Friday, and pitch it at the showcase. You draft your Tools, Guardrails and Verify rows in session 2 on Thursday.
**Three minutes (Role 30 s, Shape 30 s, Tools and guardrails 1 min, Verify 45 s, Risk and one question 15 s), then about a minute of feedback.**

### Pitch template

1. **Role.** Who you are and the one job. What does "done" mean in a way you could check in two minutes?
2. **Why this job.** Your top three candidates and why this one scored highest.
3. **Shape.** Single call, workflow or agent, and why.
4. **Context and tools.** What it reads. A short table: tool or app, read or write, approval needed?
5. **Guardrails.** What it drafts but never sends, its limits, what it refuses or hands back to you.
6. **Verify.** What checks its output, where your 20+ real past cases will come from, and your honest
   minutes-per-run today (from last week's actual runs) times runs per week.
7. **Risks.** One thing that could go wrong, and one question for the room.

### How the room gives feedback

After each pitch, one classmate asks one of these and I give a next step (the rest go to Discord):  Is it **one** job? Can I tell what done means? What is the riskiest tool?
What would you check first, and how? Be kind and specific: "your job has three tasks in it, which one first?" is
useful; "good idea" is not.

You can switch tracks until the end of this week.

## How it is graded

- The weekly build is checked against the acceptance criteria above and your explanation of it. Be ready to
  walk through it.
- The pitch is not graded alone. It starts your capstone, which is graded at demo day on the capstone rubric
  (`modules/12-capstone-role-agent/rubric.md`): role fit, correctness, design, evals, safety, explanation.
- Pass or fail on engagement counts too: showing up, doing the lab, giving the others feedback.
