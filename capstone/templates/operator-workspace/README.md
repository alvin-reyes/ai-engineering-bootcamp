# Operator track: role agent workspace

A folder you open with Claude Code (or use as a project in Claude Cowork). Claude reads `CLAUDE.md` every time, uses
the skills for your repeatable jobs, and hands specialist steps to subagents. This sample is for an operations lead
whose job is the weekly status update. Rename and rewrite everything for your role.

```
operator-workspace/
  CLAUDE.md                                # who you are, your role, the rules your agent follows
  .claude/skills/weekly-status-draft/SKILL.md   # one repeatable job, step by step
  .claude/agents/status-checker.md         # a specialist that checks the draft before you see it
  knowledge/                               # style guides, templates, examples of good past outputs
  evals/cases.md                           # your eval sheet: real past inputs and what good looks like
```

## How to use it

1. Copy this folder, rename `dot-claude/` to `.claude/`, and open it in Claude Code (or add it to a Cowork project).
   (It ships as `dot-claude/` so the sample skill doesn't switch on inside the course materials.)
2. Rewrite `CLAUDE.md` for your role (keep the rules section).
3. Rename the skill for your job and rewrite its steps from your job spec.
4. Connect the apps it needs to read (for example Drive, Gmail, Slack, your ticket tool) through Claude's connectors.
   Start read-only.
5. Run it on last week's real inputs and grade the result in `evals/cases.md`.

VERIFY: connector names and availability depend on your Claude plan and your company's settings.
