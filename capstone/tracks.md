# Your capstone: an AI agent for your own role

Over the next four weeks you will build an agent that does one real, recurring part of your job. You pick the
track that fits how you work. Both tracks follow the same method, are graded on the same rubric, and end with a
live demo.

## Pick your track

| | Builder track | Operator track |
|---|---|---|
| For | People who write code | Everyone else (ops, sales, marketing, support, PM, finance…) |
| You build with | Python and the Claude API: tools, retrieval, evals in code | A Claude workspace: instructions, skills, subagents, connectors |
| You need | Python 3.11+, Git, an API key | Claude with Claude Code or Cowork, and access to the apps your job uses |
| You hand in | A repo: agent, tools, eval script, README | A workspace folder, an eval sheet, a short write-up |

Not sure? If you have never written a Python function, choose Operator. You can switch tracks until the end of
week 2.

## The method: build your own agent persona

A role contract, not a costume. Your agent's persona is five things, written down:

1. **Role:** one job, one definition of done. Map the tasks you repeat, pick one with the canvas
   (`role-agent-canvas.md`), and write its spec: trigger, inputs, steps, output, what "done" means, who checks it.
2. **Context:** load what it needs, hide what it doesn't. Instructions, the documents and examples for this job,
   and nothing else.
3. **Tools:** least privilege, read-only by default. Each tool or connected app has one job; anything that writes
   needs your approval.
4. **Guardrails:** the workflow gates every next step. It drafts; you send. Step limits, approvals, no secrets in
   prompts.
5. **Verify:** no proof, no handoff. 20+ real past cases, and another agent (or an eval script) grades the output
   before you see it. Measure minutes saved per run.

## Week by week

| Week | Everyone | Builder track | Operator track |
|---|---|---|---|
| 1 | Role map | Weekly build: streaming assistant | Set up your workspace; write your role's `CLAUDE.md`; build your first skill |
| 2 | Canvas + pitch (due end of week) | Weekly build: an agent with three tools | Connect your apps (read-only first); add one subagent |
| 3 | Design review; eval set started | Weekly build: answers from your role's documents, with evals | Knowledge files; eval sheet with 20 cases |
| 4 | Demo day | Tracing, cost per task, injection test | Approval steps, injection test, time-saved numbers |

## Starting points

- Builder: `templates/builder/README.md`. Reuse your week 1 and week 2 builds; your capstone grows from them.
- Operator: copy `templates/operator-workspace/` and rename things for your role. It contains a sample `CLAUDE.md`,
  one skill, one subagent and an eval sheet.

## Rules that apply to every role agent

- Anything that leaves your hands (emails, messages, posts, tickets) is a **draft you send**.
- Use only data your employer allows you to use with AI tools. When in doubt, use redacted or made-up examples.
- Never put passwords, API keys or tokens in instructions or files.
- Be ready to explain every instruction, tool and decision in your agent.
