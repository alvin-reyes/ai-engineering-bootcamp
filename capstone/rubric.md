# Capstone rubric: role agent (both tracks)

Each criterion scores missing (0) · partial (1) · solid (2) · excellent (3). To pass: **solid or above on Role fit,
Correctness, Evals and Safety**, and no criterion missing. Grade against the learner's own job spec.

| Criterion | Solid (2) | Excellent (3) | Builder evidence | Operator evidence |
|---|---|---|---|---|
| **Role fit** | One recurring task from the learner's real role, clearly scoped; canvas complete | Scored against alternatives; time saved measured from real runs | Canvas + README | Canvas + write-up |
| **Correctness** | Works live on real (or realistic redacted) inputs; failures handled without crashing or inventing | Handles edge cases from the eval set; says when it cannot do the job | Live demo, tests | Live demo |
| **Design** | Simplest design that fits (single call / workflow / agent); clear instructions and tools | Each tool, skill or subagent has one job; easy for someone else to pick up | Code structure, tool schemas | `CLAUDE.md`, skills, subagents |
| **Evals** | 20+ real past cases incl. 3+ that should be refused or escalated; results reported | One change made and measured before/after | Eval script + results | Eval sheet with grades |
| **Safety** | Outbound is draft-only; read-only by default; no secrets in files; data use allowed | Prompt-injection test done and a fix shown | Code + test | Instructions + test notes |
| **Explanation** | Explains why this job, why this design, what it cannot do | Clear next steps and honest limits | Demo Q&A | Demo Q&A |

## Grader notes

- Do not mark down the Operator track for not writing code, or the Builder track for a plain UI. Judge the agent
  against the job spec.
- "Time saved" must come from the learner's own before/after runs. An estimate with no runs behind it caps Role fit
  at partial.
- Any secret found in a submission: Safety is missing, and tell the learner privately to rotate it.
